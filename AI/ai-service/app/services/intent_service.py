# app/services/intent_service.py
"""
few-shot 의도 인식 서비스
"""
# app/services/intent_service.py
import json
import re
from fastapi import FastAPI, HTTPException, Depends
from typing import Dict, List, Any, Optional, Union
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI

from app.models.schemas import IntentType, ScreenState, Language, ResponseStatus
from app.services.menu_service import MenuService
from app.services.response_service import ResponseService
from app.services.redis_session_manager import RedisSessionManager

class IntentService:
    """Few-shot 기반 의도 인식 서비스"""
    
    def __init__(self, api_key: str, menu_service: MenuService, response_service: ResponseService, session_manager: RedisSessionManager):
        """서비스 초기화"""
        self.menu_service = menu_service
        self.response_service = response_service
        self.session_manager = session_manager
        
        # LLM 초기화
        self.llm = ChatOpenAI(
            model_kwargs={"api_key": api_key},
            model_name="gpt-4.1",  # 또는 "gpt-4" 등 필요에 따라 변경
            temperature=0.3  # 낮은 temperature로 일관된 결과 유도
        )
        
        # Few-shot 학습 예제
        self.examples = self._load_examples()
    
    def process_request(self, text: str, language: str, screen_state: str, store_id: int, session_id: Optional[str] = None) -> Dict[str, Any]:
        """사용자 요청 처리 메인 함수"""
        print(f"[요청 처리] 세션 ID: {session_id}, 텍스트: '{text}', 화면 상태: {screen_state}")

        # 1. 세션 확보
        if not session_id:
            # 세션 ID가 없으면 새로 생성
            session_id = self.session_manager.create_session()
            print(f"[요청 처리] 새 세션 생성: {session_id}")
        else:
            # 기존 세션이 없으면 외부 ID로 생성
            if not self.session_manager.get_session(session_id):
                self.session_manager.create_session_with_id(session_id)
        
        # 세션을 다시 가져오기
        session = self.session_manager.get_session(session_id)
        
        if not session:
            raise HTTPException(status_code=500, detail="세션 생성 실패")
        
        # ✅ 방어 코드 추가
        if not isinstance(session, dict):
            raise HTTPException(status_code=500, detail="세션 정보가 유효하지 않습니다.")

        # 2. 컨텍스트 기반 옵션 선택 흐름

        # 2. ✅ 이전 대화 기반 옵션 선택 처리 우선
        if session.get("last_state") and session["last_state"].get("pending_option"):
            print("[요청 처리] 이전 대화 기반 옵션 선택 흐름 진입")
            response = self._process_context_based_option_selection(text, language, screen_state, store_id, session)
            self.session_manager.add_to_history(session_id, text, response)
            return response

        # 3. 일반 의도 인식 및 처리
        intent_data = self._recognize_intent(text, language, screen_state, store_id, session)

        if intent_data["intent_type"] == IntentType.ORDER:
            response = self._process_order_intent(intent_data, text, language, screen_state, store_id, session)
        elif intent_data["intent_type"] == IntentType.SEARCH:
            response = self._process_search_intent(intent_data, text, language, screen_state, store_id, session)
        elif intent_data["intent_type"] == IntentType.PAYMENT:
            response = self._process_payment_intent(intent_data, text, language, screen_state, store_id, session)
        else:
            response = self._process_unknown_intent(text, language, screen_state, store_id, session)

        # 4. 대화 기록 저장
        self.session_manager.add_to_history(session_id, text, response)

        return response
    
    def _recognize_intent(self, text: str, language: str, screen_state: str, store_id: int, session: Dict[str, Any]) -> Dict[str, Any]:
        """Few-shot 학습을 통한 의도 인식"""
        # 1. 메뉴 정보 로드
        store_menus = self.menu_service.get_store_menus(store_id)
        
        # 2. 화면 상태에 따른 컨텍스트 구성
        context = self._build_context(screen_state, store_id, store_menus, session)
        
        # 3. Few-shot 예제 선택
        examples = self._select_examples(screen_state, language)
        
        # 4. 프롬프트 구성
        prompt_template = PromptTemplate(
            template="""
            당신은 음성 키오스크 시스템의 일부입니다. 사용자의 발화를 분석하여 의도와 메뉴, 옵션 정보를 인식해야 합니다.

            # 현재 시스템 상태
            - 현재 화면: {screen_state}
            - 사용자 언어: {language}

            # 사용 가능한 메뉴 정보
            {context}

            # 대화 기록
            {history}

            1. 메뉴명 교정 규칙을 최우선으로 적용하세요:
            - "버닐라라떼/버닐라 라떼/버닐라라테/버닐라 라테/아바라" → "바닐라 라떼"
            - "아아/아이스아메리카노/아아메리카노" → "아메리카노"
            - "따아/따듯한 아메리카노/핫아메리카노" → "아메리카노"
            - "카페라떼/카페라테/라떼/라테" → "카페 라떼"
            - "헤이즐넛 라떼/헤이즐넛라떼/헤이즐 라떼" → "헤이즐넛 라떼"
            - "딸기스무디/딸기 스무디" → "딸기 스무디"
            - "블루베리 요거트/블루베리요거트스무디" → "블루베리 요거트 스무디"
            - "초콜릿라떼떼 어이스 한개 줘" → "초코라떼"
            - "어메리카노 어이스 한개 줘" → "아메리카노"
            - "아샷추" → "아이스티"
            - "아바라" → "바닐라 라떼"

            2. 다음과 같은 옵션 매핑 규칙을 적용하세요:
            - "아이스/아이스아메리카노/차가운/아아" → 온도 옵션의 "ICE" 값
            - "따뜻한/뜨거운/따아/뜨아" → 온도 옵션의 "HOT" 값
            - "작은/스몰/S" → 사이즈 옵션의 "S" 값
            - "중간/미디엄/M" → 사이즈 옵션의 "M" 값
            - "큰/라지/L" → 사이즈 옵션의 "L" 값
            - "아바라" → 온도 옵션의 "ICE" 값
            - "아샷추" → 샷추가 옵션의 "샷 1개 추가" 값

            # 분석 예제
            다음은 사용자 발화 분석 예제입니다:
            {examples}

            # 현재 입력
            사용자: "{text}"

            # 분석 지침
            사용자의 발화를 분석하여 다음 정보를 추출해주세요:
            1. 의도 (주문, 검색, 결제 등)
            2. 메뉴 이름과 수량
            3. 옵션 정보 (사이즈, 온도 등)

            "아아 하나 줘"와 같은 입력에서는 반드시 아메리카노 메뉴에 ICE 옵션을 추가해야 합니다.
            "따아 한잔이요"와 같은 입력에서는 반드시 아메리카노 메뉴에 HOT 옵션을 추가해야 합니다.


            결과는 다음 JSON 형식으로 반환해주세요:
            ```json
            {{
              "intent_type": "ORDER 또는 SEARCH 또는 PAYMENT 또는 UNKNOWN",
              "menus": [
                {{
                  "menu_id": "메뉴 아이디디",
                  "menu_name": "메뉴 이름",
                  "quantity": 수량,
                  "options": [
                    {{
                      "option_id": "옵션 id"
                      "option_name": "옵션 이름 (예: 온도, 사이즈)",
                      "option_value": "옵션 값 (예: ICE, HOT, S, M, L)"
                    }}
                  ]
                }}
              ],
              "search_query": "검색어 (SEARCH 의도인 경우에만)",
              "payment_method": "결제 방법 (PAYMENT 의도인 경우에만)"
            }}
            ```

            # 분석 결과
            """,
            input_variables=["screen_state", "language", "context", "history", "examples", "text"]
        )
        
        # 5. LLM 체인 실행
        chain = LLMChain(llm=self.llm, prompt=prompt_template)
        response = chain.run(
            screen_state=screen_state,
            language=language,
            context=context,
            history=self._format_history(session),
            examples=examples,
            text=text
        )
        
        # 6. LLM 응답 파싱
        result = self._parse_llm_response(response)
        
        # 7. 디버깅 정보
        print(f"[의도 인식] 입력: '{text}', 인식 결과: {result}")
        
        return result
    
    def _process_order_intent(self, intent_data: Dict[str, Any], text: str, language: str, screen_state: str, store_id: int, session: Dict[str, Any]) -> Dict[str, Any]:
        """주문 의도 처리"""
        # 1. 인식된 메뉴 정보 추출
        recognized_menus = intent_data.get("menus", [])
        
        if not recognized_menus:
            # 메뉴 인식 실패
            return {
                "intent_type": IntentType.UNKNOWN,
                "confidence": 0.3,
                "raw_text": text,
                "screen_state": screen_state,
                "data": {
                    "pre_text": text,
                    "post_text": text,
                    "reply": self.response_service.get_response("menu_not_found", language),
                    "status": ResponseStatus.UNKNOWN,
                    "language": language,
                    "session_id": session.get("id", ""),
                    "cart": session.get("cart", []),
                    "contents": [],
                    "store_id": store_id
                }
            }
        
        # 2. 메뉴 정보 보강
        enriched_menus = []

        for menu_info in recognized_menus:
            menu_name = menu_info.get("menu_name")
            if not menu_name:
                print(f"[오류] menu_name이 비어있습니다. 입력 텍스트: {text}")
                continue  # 또는 return self._process_unknown_intent(...)
            
            # 메뉴 찾기
            menu_match = self.menu_service.find_menu_by_name(menu_name, store_id)
            
            if menu_match:
                # 중복 옵션 제거
                unique_options = []
                option_ids_seen = set()

                for option in menu_match["options"]:
                    option_id = option.get("option_id")
                    if option_id not in option_ids_seen:
                        option_ids_seen.add(option_id)
                        unique_options.append(option)
                
                # 중복 제거된 옵션 목록으로 업데이트
                menu_match["options"] = unique_options
                

                # 메뉴 기본 정보
                enriched_menu = {
                    "menu_id": menu_match["id"],
                    "quantity": menu_info.get("quantity", 1),
                    "name": menu_match["name_kr"],
                    "name_en": menu_match["name_en"],
                    "description": menu_match["description"],
                    "base_price": menu_match["price"],
                    "total_price": menu_match["price"],
                    "image_url": menu_match.get("image_url", ""),
                    #"options": menu_match["options"],
                    "options": menu_match["options"].copy(),
                    "selected_options": [],
                    "is_corrected": menu_name.lower() != menu_match["name_kr"].lower(),
                    "original_name": menu_name if menu_name.lower() != menu_match["name_kr"].lower() else None
                }
                
                # 옵션 처리
                recognized_options = menu_info.get("options", [])
                for option_info in recognized_options:
                    option_name = option_info.get("option_name", "").lower()
                    option_value = option_info.get("option_value", "").lower()
                    
                    # 옵션 매핑
                    matched_option = self._match_option(menu_match["options"], option_name, option_value)
                    if matched_option:
                        # 이미 추가된 옵션인지 확인
                        option_already_added = False
                        for existing_option in enriched_menu["selected_options"]:
                            if existing_option["option_id"] == matched_option["option_id"]:
                                option_already_added = True
                                break
                        
                        # 중복되지 않은 경우에만 추가
                        if not option_already_added:
                            enriched_menu["selected_options"].append(matched_option)
                            
                            # options 배열에서 해당 옵션 업데이트
                            for i, option in enumerate(enriched_menu["options"]):
                                if option["option_id"] == matched_option["option_id"]:
                                    enriched_menu["options"][i]["is_selected"] = True
                                    enriched_menu["options"][i]["selected_id"] = matched_option["option_details"][0]["id"]
                                    break  # 일치하는 옵션을 찾으면 루프 종료

                # 총 가격 계산
                enriched_menu["total_price"] = self._calculate_total_price(enriched_menu)
                
                enriched_menus.append(enriched_menu)
        
        # 3. 메뉴 상태 확인
        status = ResponseStatus.UNKNOWN
        if enriched_menus:
            status = self._determine_menu_status(enriched_menus[0])
        
        # 여기에서 필수 옵션 누락 상태 처리 (status 변수가 설정된 후에 처리)
        if status == ResponseStatus.MISSING_REQUIRED_OPTIONS and enriched_menus:
            menu = enriched_menus[0]  # 첫 번째 메뉴 사용
            menu_name = menu.get("name")
            
            # 첫 번째 누락된 필수 옵션 찾기
            missing_option = None
            for option in menu.get("options", []):
                if option.get("required", True) and not option.get("is_selected", False):
                    missing_option = option
                    break
            
            if missing_option:
                # 세션에 현재 상태 저장 (메뉴와 대기 중인 옵션)
                session["last_state"] = {
                    "menu": menu,
                    "pending_option": missing_option
                }
                
                # Redis에 세션 상태 즉시 업데이트 (중요!)
                self.session_manager._save_session(session["id"], session)
                
                print(f"[세션 업데이트] 세션 ID: {session['id']}, last_state 설정됨: menu={menu_name}, option={missing_option.get('option_name')}")
            
                
                # 필수 옵션 선택 요청 응답
                option_name = missing_option.get("option_name")
                option_values = [detail.get("value") for detail in missing_option.get("option_details", [])]
                options_str = ", ".join(option_values)
                
                reply = self.response_service.get_response("select_option", language, {
                    "menu_name": menu_name,
                    "option_name": option_name,
                    "options": options_str
                })
                
                return {
                    "intent_type": IntentType.OPTION_SELECT,  # 옵션 선택 의도로 변경
                    "confidence": 0.8,
                    "raw_text": text,
                    "screen_state": ScreenState.ORDER,  # 주문 화면으로 설정
                    "data": {
                        "pre_text": text,
                        "post_text": text,
                        "reply": reply,
                        "status": ResponseStatus.MISSING_REQUIRED_OPTIONS,
                        "language": language,
                        "session_id": session.get("id", ""),
                        "cart": session.get("cart", []),
                        "contents": enriched_menus,
                        "store_id": store_id
                    }
                }
        
        # 4. 응답 메시지 생성
        reply = self.response_service.generate_order_reply(enriched_menus, language, status)
        
        # 5. 장바구니 처리 (READY_TO_ADD_CART 상태인 경우)
        cart = session.get("cart", [])
        if status == ResponseStatus.READY_TO_ADD_CART:
            for menu in enriched_menus:
                cart = self.session_manager.add_to_cart(session["id"], menu)
        
        # 6. 응답 구성
        response = {
            "intent_type": IntentType.ORDER,
            "confidence": 0.8,
            "raw_text": text,
            "screen_state": screen_state,
            "data": {
                "pre_text": text,
                "post_text": text,
                "reply": reply,
                "status": status,
                "language": language,
                "session_id": session.get("id", ""),
                "cart": cart,
                "contents": enriched_menus,
                "store_id": store_id
            }
        }
        
        return response
    
    def _process_search_intent(self, intent_data: Dict[str, Any], text: str, language: str, screen_state: str, store_id: int, session: Dict[str, Any]) -> Dict[str, Any]:
        """검색 의도 처리"""
        # 임시 구현
        search_query = intent_data.get("search_query", text)
        
        # 검색 결과 (임시)
        search_results = []
        store_menus = self.menu_service.get_store_menus(store_id)
        
        for menu_id, menu in store_menus.items():
            if search_query.lower() in menu["name_kr"].lower() or (menu["name_en"] and search_query.lower() in menu["name_en"].lower()):
                search_results.append(menu)
        
        # 응답 메시지
        if search_results:
            reply = self.response_service.get_response("search_results", language, {
                "query": search_query,
                "count": len(search_results)
            })
            status = ResponseStatus.SEARCH_RESULTS
        else:
            reply = self.response_service.get_response("no_search_results", language, {
                "query": search_query
            })
            status = ResponseStatus.UNKNOWN
        
        # 응답 구성
        return {
            "intent_type": IntentType.SEARCH,
            "confidence": 0.7,
            "search_query": search_query,
            "raw_text": text,
            "screen_state": ScreenState.SEARCH,
            "search_results": search_results,
            "data": {
                "pre_text": text,
                "post_text": text,
                "reply": reply,
                "status": status,
                "language": language,
                "session_id": session.get("id", ""),
                "cart": session.get("cart", []),
                "contents": search_results,
                "store_id": store_id
            }
        }
    
    def _process_payment_intent(self, intent_data: Dict[str, Any], text: str, language: str, screen_state: str, store_id: int, session: Dict[str, Any]) -> Dict[str, Any]:
        """결제 의도 처리"""
        # 임시 구현 - 화면 상태에 따라 다른 처리
        if screen_state == ScreenState.MAIN or screen_state == ScreenState.ORDER:
            # 장바구니에 물건이 있는지 확인
            cart = session.get("cart", [])
            
            if not cart:
                # 장바구니가 비어있는 경우
                reply = self.response_service.get_response("empty_cart", language, {})
                return {
                    "intent_type": IntentType.PAYMENT,
                    "confidence": 0.7,
                    "raw_text": text,
                    "screen_state": screen_state,  # 화면 유지
                    "data": {
                        "pre_text": text,
                        "post_text": text,
                        "reply": reply,
                        "status": ResponseStatus.UNKNOWN,
                        "language": language,
                        "session_id": session.get("id", ""),
                        "cart": cart,
                        "contents": [],
                        "store_id": store_id
                    }
                }
            else:
                # 결제 확인 화면으로 이동
                reply = self.response_service.get_response("confirm_order", language, {})
                return {
                    "intent_type": IntentType.PAYMENT,
                    "confidence": 0.8,
                    "raw_text": text,
                    "screen_state": ScreenState.CONFIRM,  # 결제 확인 화면으로 변경
                    "data": {
                        "pre_text": text,
                        "post_text": text,
                        "reply": reply,
                        "status": ResponseStatus.PAYMENT_CONFIRM,
                        "language": language,
                        "session_id": session.get("id", ""),
                        "cart": cart,
                        "contents": cart,
                        "store_id": store_id
                    }
                }
        
        elif screen_state == ScreenState.CONFIRM:
            # 결제 수단 선택 화면으로 이동
            reply = self.response_service.get_response("select_payment", language, {})
            return {
                "intent_type": IntentType.PAYMENT,
                "confidence": 0.9,
                "raw_text": text,
                "screen_state": ScreenState.SELECT_PAY,  # 결제 수단 선택 화면으로 변경
                "data": {
                    "pre_text": text,
                    "post_text": text,
                    "reply": reply,
                    "status": ResponseStatus.PAYMENT_CONFIRM,
                    "language": language,
                    "session_id": session.get("id", ""),
                    "cart": session.get("cart", []),
                    "contents": session.get("cart", []),
                    "store_id": store_id
                }
            }
        
        elif screen_state == ScreenState.SELECT_PAY:
            # 결제 진행 화면으로 이동
            payment_method = intent_data.get("payment_method", "card")  # 기본값: 카드
            
            # 결제 성공 가정 (실제로는 결제 처리 로직 필요)
            reply = self.response_service.get_response("payment_success", language, {})
            
            # 장바구니 비우기
            self.session_manager.clear_cart(session["id"])
            
            return {
                "intent_type": IntentType.PAYMENT,
                "confidence": 0.95,
                "payment_method": payment_method,
                "raw_text": text,
                "screen_state": ScreenState.PAY,  # 결제 진행 화면으로 변경
                "data": {
                    "pre_text": text,
                    "post_text": text,
                    "reply": reply,
                    "status": ResponseStatus.PAYMENT_SUCCESS,
                    "language": language,
                    "session_id": session.get("id", ""),
                    "cart": [],  # 장바구니 비움
                    "contents": [],
                    "store_id": store_id
                }
            }
        
        else:
            # 기타 상태에서의 기본 응답
            reply = self.response_service.get_response("unknown", language, {})
            return {
                "intent_type": IntentType.UNKNOWN,
                "confidence": 0.3,
                "raw_text": text,
                "screen_state": screen_state,
                "data": {
                    "pre_text": text,
                    "post_text": text,
                    "reply": reply,
                    "status": ResponseStatus.UNKNOWN,
                    "language": language,
                    "session_id": session.get("id", ""),
                    "cart": session.get("cart", []),
                    "contents": [],
                    "store_id": store_id
                }
            }
    
    def _process_unknown_intent(self, text: str, language: str, screen_state: str, store_id: int, session: Dict[str, Any]) -> Dict[str, Any]:
        """알 수 없는 의도 처리"""
        reply = self.response_service.get_response("unknown", language, {})
        return {
            "intent_type": IntentType.UNKNOWN,
            "confidence": 0.3,
            "raw_text": text,
            "screen_state": screen_state,
            "data": {
                "pre_text": text,
                "post_text": text,
                "reply": reply,
                "status": ResponseStatus.UNKNOWN,
                "language": language,
                "session_id": session.get("id", ""),
                "cart": session.get("cart", []),
                "contents": [],
                "store_id": store_id
            }
        }
    
    def _load_examples(self) -> Dict[str, List[Dict[str, Any]]]:
        """Few-shot 학습 예제 로드"""
        return {
            # 일반 주문 예제
            "order": [
                {
                    "input": "아샷추 하나 주세요",  # 특수 케이스 추가
                    "output": {
                        "intent_type": "ORDER",
                        "menus": [
                            {
                                "menu_name": "아이스티",
                                "quantity": 1,
                                "options": [
                                    {
                                        "option_name": "온도",
                                        "option_value": "ICE"
                                    },
                                    {
                                        "option_name": "샷추가",
                                        "option_value": "샷1개 추가"
                                    }
                                ]
                            }
                        ]
                    }
                },
                {
                    "input": "아바라 하나 주세요",  # 특수 케이스 추가
                    "output": {
                        "intent_type": "ORDER",
                        "menus": [
                            {
                                "menu_name": "바닐라라떼",
                                "quantity": 1,
                                "options": [
                                    {
                                        "option_name": "온도",
                                        "option_value": "ICE"
                                    },
                                    {
                                        "option_name": "샷추가",
                                        "option_value": "샷1개 추가"
                                    }
                                ]
                            }
                        ]
                    }
                },
                {
                    "input": "아아 하나 주세요",  # 특수 케이스 추가
                    "output": {
                        "intent_type": "ORDER",
                        "menus": [
                            {
                                "menu_name": "아메리카노",
                                "quantity": 1,
                                "options": [
                                    {
                                        "option_name": "온도",
                                        "option_value": "ICE"
                                    }
                                ]
                            }
                        ]
                    }
                },
                {
                    "input": "큰 사이즈 아아 한잔이요",  # 사이즈 옵션 포함 예제 추가
                    "output": {
                        "intent_type": "ORDER",
                        "menus": [
                            {
                                "menu_name": "아메리카노",
                                "quantity": 1,
                                "options": [
                                    {
                                        "option_name": "온도",
                                        "option_value": "ICE"
                                    },
                                    {
                                        "option_name": "사이즈",
                                        "option_value": "L"
                                    }
                                ]
                            }
                        ]
                    }
                },
                {
                    "input": "아메리카노 하나 주세요",
                    "output": {
                        "intent_type": "ORDER",
                        "menus": [
                            {
                                "menu_name": "아메리카노",
                                "quantity": 1,
                                "options": []
                            }
                        ]
                    }
                },
                {
                    "input": "아이스 아메리카노 주세요",
                    "output": {
                        "intent_type": "ORDER",
                        "menus": [
                            {
                                "menu_name": "아메리카노",
                                "quantity": 1,
                                "options": [
                                    {
                                        "option_name": "온도",
                                        "option_value": "ICE"
                                    }
                                ]
                            }
                        ]
                    }
                },
                {
                    "input": "아메리카노 하나 주세요",
                    "output": {
                        "intent_type": "ORDER",
                        "menus": [
                            {
                                "menu_name": "아메리카노",
                                "quantity": 1,
                                "options": []
                            }
                        ]
                    }
                },
                {
                    "input": "아이스 아메리카노 주세요",
                    "output": {
                        "intent_type": "ORDER",
                        "menus": [
                            {
                                "menu_name": "아메리카노",
                                "quantity": 1,
                                "options": [
                                    {
                                        "option_name": "온도",
                                        "option_value": "ICE"
                                    }
                                ]
                            }
                        ]
                    }
                },
                {
                    "input": "따뜻한 아메리카노 라지 사이즈로 주세요",
                    "output": {
                        "intent_type": "ORDER",
                        "menus": [
                            {
                                "menu_name": "아메리카노",
                                "quantity": 1,
                                "options": [
                                    {
                                        "option_name": "온도",
                                        "option_value": "HOT"
                                    },
                                    {
                                        "option_name": "사이즈",
                                        "option_value": "L"
                                    }
                                ]
                            }
                        ]
                    }
                },
                {
                    "input": "카페라떼 미디엄 사이즈로 뜨겁게 해주세요",
                    "output": {
                        "intent_type": "ORDER",
                        "menus": [
                            {
                                "menu_name": "카페 라떼",
                                "quantity": 1,
                                "options": [
                                    {
                                        "option_name": "사이즈",
                                        "option_value": "M"
                                    },
                                    {
                                        "option_name": "온도",
                                        "option_value": "HOT"
                                    }
                                ]
                            }
                        ]
                    }
                }
            ],
            
            # 옵션 선택 예제
            "option": [ 
                {
                    "input": "아이스로 해주세요",
                    "output": {
                        "intent_type": "ORDER",
                        "menus": [
                            {
                                "options": [
                                    {
                                        "option_name": "온도",
                                        "option_value": "ICE"
                                    }
                                ]
                            }
                        ]
                    }
                },
                {
                    "input": "라지 사이즈로 주세요",
                    "output": {
                        "intent_type": "ORDER",
                        "menus": [
                            {
                                "options": [
                                    {
                                        "option_name": "사이즈",
                                        "option_value": "L"
                                    }
                                ]
                            }
                        ]
                    }
                },
                {
                    "input": "작은 거로 할게요",
                    "output": {
                        "intent_type": "ORDER", 
                        "menus": [
                            {
                                "options": [
                                    {
                                        "option_name": "사이즈",
                                        "option_value": "S"
                                    }
                                ]
                            }
                        ]
                    }
                },
                {
                    "input": "따뜻하게 해주세요",
                    "output": {
                        "intent_type": "ORDER",
                        "menus": [
                            {
                                "options": [
                                    {
                                        "option_name": "온도",
                                        "option_value": "HOT"
                                    }
                                ]
                            }
                        ]
                    }
                },
                {
                    "input": "아이스로 할게요",
                    "output": {
                        "intent_type": "ORDER",
                        "menus": [
                            {
                                "options": [
                                    {
                                        "option_name": "온도",
                                        "option_value": "ICE"
                                    }
                                ]
                            }
                        ]
                    }
                },
                {
                    "input": "라지 사이즈로 주세요",
                    "output": {
                        "intent_type": "ORDER",
                        "menus": [
                            {
                                "options": [
                                    {
                                        "option_name": "사이즈",
                                        "option_value": "L"
                                    }
                                ]
                            }
                        ]
                    }
                }
            ],
            
            # 검색 예제
            "search": [
                {
                    "input": "커피 메뉴 알려주세요",
                    "output": {
                        "intent_type": "SEARCH",
                        "search_query": "커피"
                    }
                },
                {
                    "input": "아메리카노 종류가 뭐가 있나요?",
                    "output": {
                        "intent_type": "SEARCH",
                        "search_query": "아메리카노"
                    }
                },
                {
                    "input": "라떼 메뉴 좀 보여주세요",
                    "output": {
                        "intent_type": "SEARCH",
                        "search_query": "라떼"
                    }
                }
            ],
            
            # 결제 예제
            "payment": [
                {
                    "input": "결제할게요",
                    "output": {
                        "intent_type": "PAYMENT"
                    }
                },
                {
                    "input": "카드로 결제할게요",
                    "output": {
                        "intent_type": "PAYMENT",
                        "payment_method": "card"
                    }
                },
                {
                    "input": "결제 진행해주세요",
                    "output": {
                        "intent_type": "PAYMENT"
                    }
                }
            ]
        }
    
    def _select_examples(self, screen_state: str, language: str) -> str:
        """화면 상태에 맞는 Few-shot 예제 선택"""
        examples = []
        
        # 1. 메인 화면(MAIN)에서는 주문 + 검색 예제
        if screen_state == ScreenState.MAIN:
            examples.extend(self.examples["order"][:2])  # 주문 예제 일부
            examples.append(self.examples["search"][0])  # 검색 예제 하나
        
        # 2. 검색 화면(SEARCH)에서는 검색 + 주문 예제
        elif screen_state == ScreenState.SEARCH:
            examples.extend(self.examples["search"])  # 검색 예제 모두
            examples.append(self.examples["order"][0])  # 주문 예제 하나
        
        # 3. 메뉴 상세(DETAIL) 화면에서는 주문 예제
        elif screen_state == ScreenState.DETAIL:
            examples.extend(self.examples["order"])  # 주문 예제 모두
        
        # 4. 주문(ORDER) 화면에서는 옵션 선택 + 결제 예제
        elif screen_state == ScreenState.ORDER:
            examples.extend(self.examples["option"])  # 옵션 예제 모두
            examples.append(self.examples["payment"][0])  # 결제 예제 하나
        
        # 5. 주문 확인(CONFIRM) 화면에서는 결제 + 주문 예제
        elif screen_state == ScreenState.CONFIRM:
            examples.extend(self.examples["payment"])  # 결제 예제 모두
            examples.append(self.examples["order"][0])  # 주문 예제 하나
        
        # 6. 결제 수단 선택(SELECT_PAY) 화면에서는 결제 예제
        elif screen_state == ScreenState.SELECT_PAY:
            examples.extend(self.examples["payment"])  # 결제 예제 모두
        
        # 7. 결제(PAY) 화면에서는 결제 + 주문 예제
        elif screen_state == ScreenState.PAY:
            examples.extend(self.examples["payment"])  # 결제 예제 모두
            examples.append(self.examples["order"][0])  # 주문 예제 하나
        
        # 기본: 모든 카테고리에서 하나씩
        else:
            examples.append(self.examples["order"][0])
            examples.append(self.examples["search"][0])
            examples.append(self.examples["payment"][0])
        
        # 예제 포맷팅
        formatted_examples = []
        for example in examples:
            example_text = f"사용자: \"{example['input']}\"\n"
            example_text += f"분석 결과: ```json\n{json.dumps(example['output'], ensure_ascii=False, indent=2)}\n```"
            formatted_examples.append(example_text)
        
        return "\n\n".join(formatted_examples)
    
    def _build_context(self, screen_state: str, store_id: int, store_menus: Dict[int, Dict[str, Any]], session: Dict[str, Any]) -> str:
        """상황에 맞는 컨텍스트 구성"""
        context_parts = []
        
        # 1. 메뉴 정보 요약 (모든 메뉴 포함)
        menu_list = list(store_menus.values())  # 모든 메뉴 포함
        
        # 카테고리별로 메뉴 그룹화
        categorized_menus = {}
        for menu in menu_list:
            category_id = menu.get("category_id")
            if category_id not in categorized_menus:
                categorized_menus[category_id] = []
            categorized_menus[category_id].append(menu)
        
        # 카테고리별로 메뉴 정보 구성
        for category_id, menus in categorized_menus.items():
            category_name = self._get_category_name(category_id, store_id) or f"카테고리 {category_id}"
            category_items = []
            
            for menu in menus:
                # 기본 메뉴 정보
                menu_info = [f"### {menu['name_kr']} ({menu.get('name_en', '')}): {menu['price']}원"]
                
                if menu.get('description'):
                    menu_info.append(f"설명: {menu['description']}")
                
                # 옵션 정보 추가
                if menu.get('options'):
                    options_info = ["#### 옵션:"]
                    for opt in menu['options']:
                        opt_name = opt.get('option_name', '')
                        required = "필수" if opt.get('required', False) else "선택"
                        options_info.append(f"- {opt_name} ({required})")
                        
                        # 옵션 상세 정보
                        if opt.get('option_details'):
                            detail_items = []
                            for detail in opt['option_details']:
                                value = detail.get('value', '')
                                add_price = detail.get('additional_price', 0)
                                price_info = f"+{add_price}원" if add_price > 0 else ""
                                detail_items.append(f"  * {value} {price_info}")
                            options_info.extend(detail_items)
                    
                    menu_info.append("\n".join(options_info))
                
                # 영양 성분 정보 추가
                if menu.get('nutrition'):
                    nutrition_info = ["#### 영양 성분:"]
                    for key, value in menu['nutrition'].items():
                        nutrition_info.append(f"- {key}: {value}")
                    menu_info.append("\n".join(nutrition_info))
                
                # 원재료 정보 추가
                if menu.get('ingredients'):
                    ingredients = [ing.get('name_kr', '') for ing in menu['ingredients']]
                    if ingredients:
                        menu_info.append(f"#### 원재료: {', '.join(ingredients)}")
                
                category_items.append("\n".join(menu_info))
            
            context_parts.append(f"## {category_name}\n" + "\n\n".join(category_items))
        # 2. 장바구니 정보 (있는 경우)
        cart = session.get("cart", [])
        if cart:
            cart_summary = ["## 현재 장바구니"]
            
            for item in cart:
                option_text = ""
                if item.get("selected_options"):
                    option_strs = []
                    for opt in item["selected_options"]:
                        if opt.get("option_details"):
                            opt_value = opt["option_details"][0].get("value", "")
                            option_strs.append(f"{opt['option_name']}: {opt_value}")
                    
                    if option_strs:
                        option_text = f" ({', '.join(option_strs)})"
                
                cart_summary.append(f"- {item['name']}{option_text} x {item['quantity']}개: {item['total_price']}원")
            
            context_parts.append("\n".join(cart_summary))
        
        # 3. 화면 상태별 추가 컨텍스트
        if screen_state == ScreenState.ORDER and session.get("last_state", {}).get("menu"):
            menu = session["last_state"]["menu"]
            context_parts.append(f"## 현재 선택된 메뉴\n{menu['name_kr']} ({menu['price']}원)")
        
        return "\n\n".join(context_parts)
    
    def _format_history(self, session: Dict[str, Any]) -> str:
        """대화 기록 포맷팅"""
        history = session.get("history", [])
        
        if not history:
            return "대화 기록 없음"
        
        # 최근 3개 대화만 포함
        recent_history = history[-3:]
        formatted_history = []
        
        for entry in recent_history:
            formatted_history.append(f"사용자: \"{entry.get('user_input', '')}\"")
            
            response = entry.get("system_response", {})
            formatted_history.append(f"시스템: \"{response.get('data', {}).get('reply', '')}\"")
        
        return "\n".join(formatted_history)
    
    def _parse_llm_response(self, response: str) -> Dict[str, Any]:
        """LLM 응답 파싱"""
        try:
            print(f"파싱할 LLM 응답: {response}")  # 디버깅용
            # JSON 블록 추출
            json_pattern = r'```(?:json)?\s*([\s\S]*?)```'
            match = re.search(json_pattern, response)
            
            if match:
                json_str = match.group(1).strip()
            else:
                # 중괄호로 둘러싸인 부분 추출
                json_pattern = r'{[\s\S]*?}'
                match = re.search(json_pattern, response)
                
                if match:
                    json_str = match.group(0).strip()
                else:
                    json_str = response.strip()
        
            print(f"파싱된 JSON 문자열: {json_str}")  # 디버깅용
            
            # JSON 파싱
            result = json.loads(json_str)
            
            # 필수 필드 확인
            if "intent_type" not in result:
                result["intent_type"] = IntentType.UNKNOWN
            
            # 대소문자 표준화
            if isinstance(result["intent_type"], str):
                result["intent_type"] = result["intent_type"].upper()
            
            return result
        
        except Exception as e:
            print(f"LLM 응답 파싱 오류: {e}")
            print(f"원본 응답: {response}")
            
            # 기본 응답
            return {
                "intent_type": IntentType.UNKNOWN,
                "menus": []
            }
    
    def _match_option(self, options: List[Dict[str, Any]], option_name: str, option_value: str) -> Optional[Dict[str, Any]]:
        """옵션 매핑 함수"""
        # 디버깅을 위한 로그 추가
        print(f"옵션 매핑: 이름={option_name}, 값={option_value}, 사용 가능한 옵션={options}")
    
        # 1. 옵션 이름으로 매칭 시도
        matching_options = []
        for option in options:
            opt_name_kr = option.get("option_name", "").lower()
            opt_name_en = option.get("option_name_en", "").lower()
            
            if (option_name in opt_name_kr or opt_name_kr in option_name or
                option_name in opt_name_en or opt_name_en in option_name):
                matching_options.append(option)
        
        # 2. 온도/사이즈 특수 처리
        if not matching_options:
            # 온도 관련 키워드
            if any(kw in option_value for kw in ["ice", "아이스", "차가운", "시원한", "아아"]):
                for option in options:
                    if "온도" in option.get("option_name", "").lower() or "temperature" in option.get("option_name_en", "").lower():
                        matching_options.append(option)
                        option_value = "ice"
            elif any(kw in option_value for kw in ["hot", "따뜻한", "뜨거운", "따아"]):
                for option in options:
                    if "온도" in option.get("option_name", "").lower() or "temperature" in option.get("option_name_en", "").lower():
                        matching_options.append(option)
                        option_value = "hot"
            
            # 사이즈 관련 키워드
            elif any(kw in option_value for kw in ["small", "s", "작은", "스몰"]):
                for option in options:
                    if "사이즈" in option.get("option_name", "").lower() or "size" in option.get("option_name_en", "").lower():
                        matching_options.append(option)
                        option_value = "s"
            elif any(kw in option_value for kw in ["medium", "m", "미디엄", "중간"]):
                for option in options:
                    if "사이즈" in option.get("option_name", "").lower() or "size" in option.get("option_name_en", "").lower():
                        matching_options.append(option)
                        option_value = "m"
            elif any(kw in option_value for kw in ["large", "l", "라지", "큰"]):
                for option in options:
                    if "사이즈" in option.get("option_name", "").lower() or "size" in option.get("option_name_en", "").lower():
                        matching_options.append(option)
                        option_value = "l"
        
        # 3. 매칭된 옵션에서 옵션 값 찾기
        if matching_options:
            for option in matching_options:
                matched_detail = None
                
                for detail in option.get("option_details", []):
                    detail_value = detail.get("value", "").lower()
                    
                    # 정확한 일치
                    if detail_value == option_value:
                        matched_detail = detail
                        break
                    # 부분 일치
                    elif option_value in detail_value or detail_value in option_value:
                        matched_detail = detail
                        break
                    # 특수 케이스 (예: "s"와 "S" 매칭)
                    elif option_value.upper() == detail_value.upper():
                        matched_detail = detail
                        break
                
                if matched_detail:
                    return {
                        "option_id": option.get("option_id"),
                        "option_name": option.get("option_name"),
                        "option_name_en": option.get("option_name_en"),
                        "required": option.get("required", False),
                        "is_selected": True,
                        "option_details": [matched_detail]
                    }
        
        return None
    
    def _determine_menu_status(self, menu: Dict[str, Any]) -> ResponseStatus:
        """메뉴 상태 판단"""
        # 1. 메뉴명 교정 여부 확인
        if menu.get("is_corrected", False):
            return ResponseStatus.CORRECTED
        
        # 2. 추천 메뉴 여부 확인
        if menu.get("is_recommendation", False):
            return ResponseStatus.RECOMMENDATION
        
        # 3. 필수 옵션 누락 여부 확인
        missing_required = False
        for option in menu.get("options", []):
            if option.get("required", False) and not option.get("is_selected", False):
                missing_required = True
                break
        
        if missing_required:
            return ResponseStatus.MISSING_REQUIRED_OPTIONS
        
        # 4. 장바구니 추가 가능 상태
        return ResponseStatus.READY_TO_ADD_CART
    
    def _calculate_total_price(self, menu: Dict[str, Any]) -> int:
        """선택된 옵션을 포함한 총 가격 계산"""
        base_price = menu.get("base_price", 0)
        additional_price = 0
        
        for option in menu.get("selected_options", []):
            if option.get("option_details"):
                option_detail = option["option_details"][0]
                additional_price += option_detail.get("additional_price", 0)
        
        return base_price + additional_price
    
    # app/services/intent_service.py에 추가

    def _process_context_based_option_selection(self, text: str, language: str, screen_state: str, store_id: int, session: Dict[str, Any]) -> Dict[str, Any]:
        """이전 컨텍스트를 기반으로 옵션 선택 처리"""
        # 1. 이전 상태 확인
        last_state = session.get("last_state", {})
        if not last_state or "menu" not in last_state:
            # 이전 상태가 없으면 기존 메뉴 검색
            print(f"[컨텍스트 처리] 이전 상태 없음, 일반 의도 인식 시도")
            # 세션 상태 디버깅
            print(f"[세션 상태] {session}")
            return self._process_unknown_intent(text, language, screen_state, store_id, session)
        
        # 2. 이전 메뉴 정보 가져오기
        menu = last_state["menu"]
        print(f"[컨텍스트 처리] 이전 메뉴: {menu.get('name')}")
        
        # 3. 이전에 물어본 옵션이 있는지 확인
        pending_option = last_state.get("pending_option")
        if not pending_option:
            print(f"[컨텍스트 처리] 대기 중인 옵션 없음")
            return self._process_unknown_intent(text, language, screen_state, store_id, session)
        
        print(f"[컨텍스트 처리] 대기 중인 옵션: {pending_option.get('option_name')}")
        
        # 4. 사용자 응답 파싱하여 옵션 값 도출
        selected_option = self._parse_option_response(text, pending_option, menu)
        if not selected_option:
            # 옵션 파싱 실패 시 다시 물어보기
            reply = self.response_service.get_response("option_not_understood", language, {
                "option_name": pending_option.get("option_name"),
                "options": ", ".join(detail.get("value") for detail in pending_option.get("option_details", []))
            })
            
            return {
                "intent_type": IntentType.OPTION_SELECT,
                "confidence": 0.7,
                "raw_text": text,
                "screen_state": screen_state,
                "data": {
                    "pre_text": text,
                    "post_text": text,
                    "reply": reply,
                    "status": ResponseStatus.UNKNOWN,
                    "language": language,
                    "session_id": session.get("id", ""),
                    "cart": session.get("cart", []),
                    "contents": [menu],
                    "store_id": store_id
                }
            }
        
        # 5. 메뉴에 옵션 적용
        self._apply_option_to_menu(menu, selected_option)
        
        # 6. 다음 필수 옵션 확인
        next_required_option = self._get_next_required_option(menu)
        
        if next_required_option:
            # 아직 필수 옵션이 남아있는 경우
            option_name = next_required_option.get("option_name")
            options_str = ", ".join(detail.get("value") for detail in next_required_option.get("option_details", []))
            
            reply = self.response_service.get_response("select_option", language, {
                "menu_name": menu.get("name"),
                "option_name": option_name,
                "options": options_str
            })
            
            # 다음 옵션 대기 상태 설정
            session["last_state"] = {
                "menu": menu,
                "pending_option": next_required_option
            }
            # Redis에 명시적으로 세션 저장 추가
            self.session_manager._save_session(session["id"], session)
            
            return {
                "intent_type": IntentType.OPTION_SELECT,
                "confidence": 0.8,
                "raw_text": text,
                "screen_state": screen_state,
                "data": {
                    "pre_text": text,
                    "post_text": text,
                    "reply": reply,
                    "status": ResponseStatus.MISSING_REQUIRED_OPTIONS,
                    "language": language,
                    "session_id": session.get("id", ""),
                    "cart": session.get("cart", []),
                    "contents": [menu],
                    "store_id": store_id
                }
            }
        else:
            # 모든 필수 옵션이 선택된 경우, 장바구니에 추가
            cart = self.session_manager.add_to_cart(session.get("id", ""), menu)
            
            # 옵션 문자열 생성
            option_strs = []
            for opt in menu.get("selected_options", []):
                if opt.get("option_details"):
                    option_value = opt["option_details"][0].get("value", "")
                    option_strs.append(f"{opt['option_name']}: {option_value}")
            
            options_summary = f" ({', '.join(option_strs)})" if option_strs else ""
            
            reply = self.response_service.get_response("added_to_cart", language, {
                "menu_name": menu.get("name"),
                "options_summary": options_summary
            })
            
            # 주문 완료 후 상태 초기화
            session["last_state"] = {}
            self.session_manager._save_session(session["id"], session)
            
            return {
                "intent_type": IntentType.ORDER,
                "confidence": 0.9,
                "raw_text": text,
                "screen_state": ScreenState.MAIN,  # 메인 화면으로 돌아감
                "data": {
                    "pre_text": text,
                    "post_text": text,
                    "reply": reply,
                    "status": ResponseStatus.READY_TO_ADD_CART,
                    "language": language,
                    "session_id": session.get("id", ""),
                    "cart": cart,
                    "contents": [menu],
                    "store_id": store_id
                }
            }

    def _parse_option_response(self, text: str, pending_option: Dict[str, Any], menu: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """사용자 응답에서 옵션 값 파싱"""
        text = text.lower().strip()
        option_details = pending_option.get("option_details", [])
        
        # 옵션 종류별 특수 처리
        option_name = pending_option.get("option_name", "").lower()
        
        # 1. 사이즈 옵션 처리
        if "사이즈" in option_name or "size" in option_name:
            if any(kw in text for kw in ["small", "s", "작은", "스몰", "작게", "작은거", "작은 거"]):
                # 작은 사이즈 선택
                for detail in option_details:
                    if detail.get("value", "").lower() in ["s", "small"]:
                        return {
                            "option_id": pending_option.get("option_id"),
                            "option_name": pending_option.get("option_name"),
                            "option_name_en": pending_option.get("option_name_en"),
                            "required": pending_option.get("required", False),
                            "is_selected": True,
                            "selected_id": detail.get("id"),
                            "option_details": [detail]
                        }
            
            elif any(kw in text for kw in ["medium", "m", "미디엄", "중간", "보통", "중간거", "중간 거"]):
                # 중간 사이즈 선택
                for detail in option_details:
                    if detail.get("value", "").lower() in ["m", "medium"]:
                        return {
                            "option_id": pending_option.get("option_id"),
                            "option_name": pending_option.get("option_name"),
                            "option_name_en": pending_option.get("option_name_en"),
                            "required": pending_option.get("required", False),
                            "is_selected": True,
                            "selected_id": detail.get("id"),
                            "option_details": [detail]
                        }
            
            elif any(kw in text for kw in ["large", "l", "라지", "큰", "크게", "큰거", "큰 거"]):
                # 큰 사이즈 선택
                for detail in option_details:
                    if detail.get("value", "").lower() in ["l", "large"]:
                        return {
                            "option_id": pending_option.get("option_id"),
                            "option_name": pending_option.get("option_name"),
                            "option_name_en": pending_option.get("option_name_en"),
                            "required": pending_option.get("required", False),
                            "is_selected": True,
                            "selected_id": detail.get("id"),
                            "option_details": [detail]
                        }
        
        # 2. 온도 옵션 처리
        elif "온도" in option_name or "temperature" in option_name:
            if any(kw in text for kw in ["hot", "따뜻", "뜨겁", "따듯", "따뜻한", "뜨거운"]):
                # HOT 선택
                for detail in option_details:
                    if detail.get("value", "").lower() in ["hot", "따뜻한", "뜨거운"]:
                        return {
                            "option_id": pending_option.get("option_id"),
                            "option_name": pending_option.get("option_name"),
                            "option_name_en": pending_option.get("option_name_en"),
                            "required": pending_option.get("required", False),
                            "is_selected": True,
                            "selected_id": detail.get("id"),
                            "option_details": [detail]
                        }
            
            elif any(kw in text for kw in ["ice", "아이스", "차가운", "시원", "아이스로", "차갑"]):
                # ICE 선택
                for detail in option_details:
                    if detail.get("value", "").lower() in ["ice", "아이스", "차가운"]:
                        return {
                            "option_id": pending_option.get("option_id"),
                            "option_name": pending_option.get("option_name"),
                            "option_name_en": pending_option.get("option_name_en"),
                            "required": pending_option.get("required", False),
                            "is_selected": True,
                            "selected_id": detail.get("id"),
                            "option_details": [detail]
                        }
        
        # 3. 일반 옵션 값 매칭 시도
        for detail in option_details:
            detail_value = detail.get("value", "").lower()
            if detail_value in text or any(word in detail_value for word in text.split()):
                return {
                    "option_id": pending_option.get("option_id"),
                    "option_name": pending_option.get("option_name"),
                    "option_name_en": pending_option.get("option_name_en"),
                    "required": pending_option.get("required", False),
                    "is_selected": True,
                    "selected_id": detail.get("id"),
                    "option_details": [detail]
                }
        
        # 매칭 실패
        return None

    def _apply_option_to_menu(self, menu: Dict[str, Any], selected_option: Dict[str, Any]) -> None:
        """메뉴에 선택된 옵션 적용"""
         # 1. 기존 옵션 리스트에서 해당 옵션 업데이트
        for i, option in enumerate(menu.get("options", [])):
            if option.get("option_id") == selected_option.get("option_id"):
                menu["options"][i]["is_selected"] = True
                menu["options"][i]["selected_id"] = selected_option.get("selected_id")


        # 선택된 옵션 목록에 추가/업데이트
        found = False
        for i, option in enumerate(menu.get("selected_options", [])):
            if option.get("option_id") == selected_option.get("option_id"):
                menu["selected_options"][i] = selected_option
                found = True
                break
        
        if not found:
            menu.setdefault("selected_options", []).append(selected_option)
            # if "selected_options" not in menu:
            #     menu["selected_options"] = []
            # menu["selected_options"].append(selected_option)
        
        # 총 가격 재계산
        menu["total_price"] = self._calculate_total_price(menu)

    def _get_next_required_option(self, menu: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """다음 필수 옵션 가져오기"""
        for option in menu.get("options", []):
            if option.get("required", False) and not option.get("is_selected", False):
                return option
        return None
    
    def _get_category_name(self, category_id: int, store_id: int = None) -> str:
        """카테고리 ID에 해당하는 카테고리 이름 반환"""
        # 카테고리 매핑 (실제로는 DB에서 조회할 수 있음)
        category_names = {
            1: "커피",
            2: "음료",
            3: "티/차",
            4: "디저트",
            5: "베이커리",
            6: "샌드위치",
            7: "기타"
        }
        
        return category_names.get(category_id, f"카테고리 {category_id}")