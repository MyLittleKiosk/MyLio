# app/services/processor/order_processor.py
from typing import Dict, Any, Optional, List
import json
import re
from langchain.prompts import PromptTemplate 

from app.models.schemas import IntentType, ScreenState, Language, ResponseStatus
from app.services.processor.base_processor import BaseProcessor
from app.services.option.option_matcher import OptionMatcher

class OrderProcessor(BaseProcessor):
    """주문 처리 프로세서"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.option_matcher = OptionMatcher()
    
    def process(self, intent_data: Dict[str, Any], text: str, language: str, screen_state: str, store_id: int, session: Dict[str, Any]) -> Dict[str, Any]:
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
                    matched_option = self.option_matcher.match_option(menu_match["options"], option_name, option_value)
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
                enriched_menu["total_price"] = self.option_matcher.calculate_total_price(enriched_menu)
                
                enriched_menus.append(enriched_menu)
        
        # 3. 메뉴 상태 확인
        status = ResponseStatus.UNKNOWN
        if enriched_menus:
            status = self.option_matcher.determine_menu_status(enriched_menus[0])
        
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

                # 기존 장바구니 가져오기
                if "cart" not in session:
                    session["cart"] = []
                
                # 응답 생성 전 최신 장바구니 로깅
                print(f"[응답 생성 전] 세션 ID: {session['id']}, 장바구니 항목 수: {len(session['cart'])}, 항목: {[item.get('name') for item in session['cart']]}")
                
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
                        "cart": session["cart"],  # 세션에서 직접 장바구니 가져오기
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

            # 추가: 최신 장바구니 정보 다시 조회
            cart = self.session_manager.get_cart(session["id"])
        
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
    
    def process_option_selection(self, text: str, language: str, screen_state: str, store_id: int, session: Dict[str, Any]) -> Dict[str, Any]:
        """이전 컨텍스트를 기반으로 옵션 선택 처리"""

        # 세션 ID 확보
        session_id = session.get("id")
        if not session_id:
            print("[컨텍스트 처리] 세션 ID 없음")
            return self._process_unknown_intent(text, language, screen_state, store_id, session)
        
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
        selected_option = self.option_matcher.parse_option_response(text, pending_option, menu)
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
                    "session_id": session_id,
                    "cart": session.get("cart", []),
                    "contents": [menu],
                    "store_id": store_id
                }
            }
        
        # 5. 메뉴에 옵션 적용
        self.option_matcher.apply_option_to_menu(menu, selected_option)
        
        # 6. 다음 필수 옵션 확인
        next_required_option = self.option_matcher.get_next_required_option(menu)
        
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
                    "session_id": session_id,
                    "cart": session.get("cart", []),
                    "contents": [menu],
                    "store_id": store_id
                }
            }
        else:
            # 모든 필수 옵션이 선택된 경우, 장바구니에 추가
            print(f"[장바구니 추가 전] 세션 ID: {session_id}, 장바구니 항목 수: {len(session.get('cart', []))}")
            
            # 장바구니 초기화 (필요 시)
            if "cart" not in session:
                session["cart"] = []
                self.session_manager._save_session(session_id, session)
                print(f"[장바구니 초기화] 세션 ID: {session_id}")
            
            # 장바구니에 메뉴 추가
            cart = self.session_manager.add_to_cart(session_id, menu)
            print(f"[장바구니 추가 직후] 세션 ID: {session_id}, 장바구니 항목 수: {len(cart)}")
            
            # 중요: 세션에서 업데이트된 장바구니 가져오기
            session["cart"] = cart  # 추가 - 세션 객체 업데이트
            self.session_manager._save_session(session_id, session)  # 명시적 저장

            # 추가: 세션에서 최신 장바구니 정보 다시 조회
            updated_cart = self.session_manager.get_cart(session_id)
            print(f"[장바구니 최종 확인] 세션 ID: {session_id}, 장바구니 항목 수: {len(updated_cart)}")
            
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
            self.session_manager._save_session(session_id, session)
            
            # 최종 응답 생성
            response = {
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
                    "session_id": session_id,
                    "cart": updated_cart,  # 최신 장바구니 정보 사용
                    "contents": [menu],
                    "store_id": store_id
                }
            }
            
            # 응답 확인 로깅
            print(f"[응답 생성] 장바구니 항목 수: {len(response['data']['cart'])}")
            
            return response
    
    def _get_prompt_template(self):
        """주문 의도 인식을 위한 프롬프트 템플릿"""
        return PromptTemplate(
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
            - "아이스/아이스아메리카노/차가운/아아/아바라" → 온도 옵션의 "ICE" 값
            - "따뜻한/뜨거운/따아/뜨아" → 온도 옵션의 "HOT" 값
            - "작은/스몰/S" → 사이즈 옵션의 "S" 값
            - "중간/미디엄/M" → 사이즈 옵션의 "M" 값
            - "큰/라지/L" → 사이즈 옵션의 "L" 값
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
    
    def _load_examples(self):
        """주문 관련 Few-shot 학습 예제"""
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
    
    def _select_examples(self, screen_state, language):
        """화면 상태에 맞는 Few-shot 예제 선택"""
        # (기존 _select_examples 코드에서 주문 관련 부분만 이동)
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

    # 기타 주문 관련 헬퍼 메서드들