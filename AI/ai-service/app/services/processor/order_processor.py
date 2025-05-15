# app/services/processor/order_processor.py
import re
from typing import Dict, Any, Optional, List
from app.models.schemas import IntentType, ScreenState, Language, ResponseStatus
from app.services.processor.base_processor import BaseProcessor
from app.services.option.option_matcher import OptionMatcher
from app.services.response.response_generator import ResponseGenerator
from app.services.response_service import ResponseService  
from app.models.schemas import ResponseStatus
from app.services.intent_recognizer import IntentRecognizer

class OrderProcessor(BaseProcessor):
    """주문 처리 프로세서"""
    
    def __init__(self, response_generator: ResponseGenerator, menu_service, session_manager, intent_recognizer):
        """프로세서 초기화"""
        self.response_generator = response_generator
        self.menu_service = menu_service
        self.session_manager = session_manager
        self.option_matcher = OptionMatcher()
        self.intent_recognizer = intent_recognizer
    
    def process(self, intent_data: Dict[str, Any], text: str, language: str, screen_state: str, store_id: int, session: Dict[str, Any]) -> Dict[str, Any]:
        """주문 의도 처리"""
        # 1. 인식된 메뉴 정보 추출
        recognized_menus = intent_data.get("menus", [])
        
        if not recognized_menus:
            # 메뉴 인식 실패
            reply = intent_data.get("reply") or "메뉴를 인식하지 못했습니다. 다시 말씀해주세요."
            return self._build_response(
                intent_data, text, language, screen_state, store_id, session,
                ResponseStatus.UNKNOWN, contents=[], reply=reply
            )
        
        # 2. 메뉴 정보 보강
        enriched_menus = []

        for menu_info in recognized_menus:
            menu_name = menu_info.get("menu_name")
            if not menu_name:
                print(f"[오류] menu_name이 비어있습니다. 입력 텍스트: {text}")
                continue
            
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
                                    break

                # 총 가격 계산
                enriched_menu["total_price"] = self.option_matcher.calculate_total_price(enriched_menu)
                
                enriched_menus.append(enriched_menu)

        # 보강된 메뉴가 없으면 처리 중단
        if not enriched_menus:
            reply = intent_data.get("reply") or "메뉴를 인식하지 못했습니다. 다시 말씀해주세요."
            return self._build_response(
                intent_data, text, language, screen_state, store_id, session,
                ResponseStatus.UNKNOWN, contents=[], reply=reply
            )

        # 3. 진행중인 옵션 선택이 있는지 확인
        if session.get("last_state") and session["last_state"].get("pending_option"):
            print("[주문 처리] 기존 진행 중인 옵션 선택 발견")
            
            # 대기열에 새 메뉴 추가
            if "order_queue" not in session:
                session["order_queue"] = []
            
            # 대기열에 새 메뉴 추가
            session["order_queue"].extend(enriched_menus)
            self.session_manager._save_session(session["id"], session)
            
            print(f"[대기열 추가] 현재 대기열 메뉴 수: {len(session['order_queue'])}")
            
            # 진행 중인 옵션 선택 계속
            menu = session["last_state"]["menu"]
            pending_option = session["last_state"]["pending_option"]
            
            # 사용자에게 옵션 선택 재요청
            option_name = pending_option.get("option_name")
            options_str = ", ".join([detail.get("value") for detail in pending_option.get("option_details", [])])
            
            # 대기열 정보 포함 응답 생성
            queue_info = f" {len(session.get('order_queue', []))}개의 추가 메뉴는 이 주문 완료 후 처리됩니다." if session.get("order_queue") else ""
            reply = f"{menu.get('name')}의 {option_name}을(를) 먼저 선택해주세요. ({options_str}){queue_info}"
            
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
                    "contents": [menu],  # 현재 진행 중인 메뉴
                    "store_id": store_id
                }
            }
        
        # 4. 여러 메뉴 처리 - 첫 번째 메뉴 처리하고 나머지는 대기열에 추가
        first_menu = enriched_menus[0]
        
        # 첫 번째 메뉴 외 나머지 메뉴가 있으면 대기열에 추가
        if len(enriched_menus) > 1:
            if "order_queue" not in session:
                session["order_queue"] = []
                
            # 첫 번째 메뉴를 제외한 나머지 메뉴를 대기열에 추가
            session["order_queue"].extend(enriched_menus[1:])
            
            # 중요: session을 확실히 저장 
            print(f"[대기열 디버깅] 대기열에 {len(enriched_menus[1:])}개 메뉴 추가 전: {len(session.get('order_queue', []))}")
            result = self.session_manager._save_session(session["id"], session)
            print(f"[대기열 디버깅] 세션 저장 결과: {result}")
            
            # 추가 후 다시 세션을 가져와서 대기열 확인 
            updated_session = self.session_manager.get_session(session["id"])
            print(f"[대기열 디버깅] 대기열에 추가 후: {len(updated_session.get('order_queue', []))}")
            print(f"[대기열 디버깅] 대기열 메뉴: {[m.get('name') for m in updated_session.get('order_queue', [])]}")
            
            print(f"[대기열 추가] 첫 번째 메뉴 외 {len(enriched_menus) - 1}개 메뉴를 대기열에 추가")
        
        # 5. 메뉴 상태 확인
        status = self.option_matcher.determine_menu_status(first_menu)
        
        # 6. 필수 옵션 누락 상태 처리
        if status == ResponseStatus.MISSING_REQUIRED_OPTIONS:
            menu_name = first_menu.get("name")
            
            # 첫 번째 누락된 필수 옵션 찾기
            missing_option = None
            for option in first_menu.get("options", []):
                if option.get("required", True) and not option.get("is_selected", False):
                    missing_option = option
                    break
            
            if missing_option:
                # 세션에 현재 상태 저장 (메뉴와 대기 중인 옵션)
                session["last_state"] = {
                    "menu": first_menu,
                    "pending_option": missing_option
                }
                self.session_manager._save_session(session["id"], session)
                
                # 대기열 정보 포함 응답 생성
                queue_info = ""
                if "order_queue" in session and session["order_queue"]:
                    queue_names = [menu.get("name", "알 수 없는 메뉴") for menu in session["order_queue"]]
                    queue_info = f" 추가로 {', '.join(queue_names)}(이)가 대기 중입니다." if queue_names else ""
                
                # 필수 옵션 선택 요청 응답 컨텍스트 구성
                option_name = missing_option.get("option_name")
                options_str = ", ".join([detail.get("value") for detail in missing_option.get("option_details", [])])
                
                context = {
                    "status": ResponseStatus.MISSING_REQUIRED_OPTIONS,
                    "screen_state": screen_state,
                    "menu_name": menu_name,
                    "option_name": option_name,
                    "options": options_str,
                    "queue_info": queue_info
                }
                
                # 응답 생성
                reply = intent_data.get("reply") or self.response_generator.generate_response(intent_data, language, context)
                
                # LLM 응답이 없는 경우 기본 응답
                if not reply:
                    reply = f"{menu_name}의 {option_name}을(를) 선택해주세요. ({options_str}){queue_info}"
                elif "order_queue" in session and session["order_queue"] and queue_info not in reply:
                    # 대기열 정보가 응답에 포함되지 않은 경우 추가
                    reply += queue_info
                return {
                    "intent_type": IntentType.OPTION_SELECT,
                    "confidence": intent_data.get("confidence", 0.8),
                    "raw_text": text,
                    "screen_state": ScreenState.ORDER,
                    "data": {
                        "pre_text": text,
                        "post_text": intent_data.get("post_text", text),
                        "reply": reply,
                        "status": ResponseStatus.MISSING_REQUIRED_OPTIONS,
                        "language": language,
                        "session_id": session.get("id", ""),
                        "cart": session.get("cart", []),
                        "contents": [first_menu],
                        "store_id": store_id
                    }
                }
        
        # 7. 필수 옵션이 모두 있는 경우 (READY_TO_ADD_CART) - 바로 장바구니에 추가
        if status == ResponseStatus.READY_TO_ADD_CART:
            # 장바구니에 첫 번째 메뉴 추가
            cart = self.session_manager.add_to_cart(session.get("id", ""), first_menu)
            
            # 대기열 확인
            if "order_queue" in session and session["order_queue"]:
                # 다음 메뉴 처리 시작
                next_menu = session["order_queue"][0]
                session["order_queue"].pop(0)
                self.session_manager._save_session(session["id"], session)
                
                # 다음 메뉴의 상태 확인
                next_status = self.option_matcher.determine_menu_status(next_menu)
                
                if next_status == ResponseStatus.MISSING_REQUIRED_OPTIONS:
                    # 다음 메뉴의 필수 옵션 선택 프로세스 시작
                    missing_option = None
                    for option in next_menu.get("options", []):
                        if option.get("required", True) and not option.get("is_selected", False):
                            missing_option = option
                            break
                    
                    if missing_option:
                        # 세션에 다음 메뉴 정보 저장
                        session["last_state"] = {
                            "menu": next_menu,
                            "pending_option": missing_option
                        }
                        self.session_manager._save_session(session["id"], session)
                        
                        # 옵션 문자열 생성 (첫 번째 메뉴)
                        option_strs = []
                        for opt in first_menu.get("selected_options", []):
                            if opt.get("option_details"):
                                option_value = opt["option_details"][0].get("value", "")
                                option_strs.append(f"{opt['option_name']}: {option_value}")
                        
                        options_summary = f" ({', '.join(option_strs)})" if option_strs else ""
                        first_menu_desc = f"{first_menu.get('name')}{options_summary}"
                        
                        # 다음 메뉴 옵션 선택 요청
                        option_name = missing_option.get("option_name")
                        options_str = ", ".join([detail.get("value") for detail in missing_option.get("option_details", [])])
                        
                        # 응답 생성 - 첫 번째 메뉴 완료 + 다음 메뉴 옵션 요청
                        reply = f"{first_menu_desc}을(를) 장바구니에 담았습니다. 이제 {next_menu.get('name')}의 {option_name}을(를) 선택해주세요. ({options_str})"
                        
                        return {
                            "intent_type": IntentType.OPTION_SELECT,
                            "confidence": 0.8,
                            "raw_text": text,
                            "screen_state": ScreenState.ORDER,
                            "data": {
                                "pre_text": text,
                                "post_text": text,
                                "reply": reply,
                                "status": ResponseStatus.MISSING_REQUIRED_OPTIONS,
                                "language": language,
                                "session_id": session.get("id", ""),
                                "cart": cart,
                                "contents": [next_menu],  # 다음 메뉴를 현재 컨텐츠로 설정
                                "store_id": store_id
                            }
                        }
                else:
                    # 필수 옵션이 없는 다음 메뉴는 바로 장바구니에 추가
                    cart = self.session_manager.add_to_cart(session.get("id", ""), next_menu)
                    
                    # 첫 번째와 두 번째 메뉴 정보
                    first_name = first_menu.get("name")
                    second_name = next_menu.get("name")
                    
                    # 대기열에 더 메뉴가 있는지 확인
                    if "order_queue" in session and session["order_queue"]:
                        # 다음 메뉴 처리를 위한 헬퍼 메서드 호출
                        return self._process_next_queued_menu(session["id"], f"{first_name}, {second_name}", language, screen_state, store_id)
                    
                    # 모든 메뉴 처리 완료
                    reply = f"{first_name}와(과) {second_name}을(를) 장바구니에 담았습니다. 더 필요한 것이 있으신가요?"
            
            else:  # 대기열 없음 - 첫 번째 메뉴만 처리
                # 옵션 문자열 생성
                option_strs = []
                for opt in first_menu.get("selected_options", []):
                    if opt.get("option_details"):
                        option_value = opt["option_details"][0].get("value", "")
                        option_strs.append(f"{opt['option_name']}: {option_value}")
                
                options_summary = f" ({', '.join(option_strs)})" if option_strs else ""
                
                # 응답 생성
                context = {
                    "status": ResponseStatus.READY_TO_ADD_CART,
                    "screen_state": ScreenState.MAIN,
                    "menu_name": first_menu.get("name"),
                    "options_summary": options_summary
                }
                
                reply = intent_data.get("reply") or self.response_generator.generate_response(intent_data, language, context)
                
                # LLM 응답이 없는 경우 기본 응답
                if not reply:
                    reply = f"{first_menu.get('name')}{options_summary}을(를) 장바구니에 담았습니다. 더 필요한 것이 있으신가요?"
            
            # 업데이트된 장바구니 정보 가져오기
            updated_cart = self.session_manager.get_cart(session.get("id", ""))
            
            # 응답 구성
            return {
                "intent_type": IntentType.ORDER,
                "confidence": intent_data.get("confidence", 0.9),
                "raw_text": text,
                "screen_state": ScreenState.MAIN,
                "data": {
                    "pre_text": text,
                    "post_text": intent_data.get("post_text", text),
                    "reply": reply,
                    "status": ResponseStatus.READY_TO_ADD_CART,
                    "language": language,
                    "session_id": session.get("id", ""),
                    "cart": updated_cart,
                    "contents": [first_menu],
                    "store_id": store_id
                }
            }
        # 8. 그 외 상태 처리 - 기본 응답 생성
        context = {
            "status": status,
            "screen_state": screen_state,
            "menus": enriched_menus,
            "cart": session.get("cart", [])
        }

        # # 3. 메뉴 상태 확인
        # status = ResponseStatus.UNKNOWN
        # if enriched_menus:
        #     status = self.option_matcher.determine_menu_status(enriched_menus[0])
        
        # # 여기에서 필수 옵션 누락 상태 처리 (status 변수가 설정된 후에 처리)
        # if status == ResponseStatus.MISSING_REQUIRED_OPTIONS and enriched_menus:
        #     menu = enriched_menus[0]  # 첫 번째 메뉴 사용
        #     menu_name = menu.get("name")
            
        #     # 첫 번째 누락된 필수 옵션 찾기
        #     missing_option = None
        #     for option in menu.get("options", []):
        #         if option.get("required", True) and not option.get("is_selected", False):
        #             missing_option = option
        #             break
            
        #     if missing_option:
        #         # 세션에 현재 상태 저장 (메뉴와 대기 중인 옵션)
        #         session["last_state"] = {
        #             "menu": menu,
        #             "pending_option": missing_option
        #         }
                
        #         # Redis에 세션 상태 즉시 업데이트 (중요!)
        #         self.session_manager._save_session(session["id"], session)
                
        #         print(f"[세션 업데이트] 세션 ID: {session['id']}, last_state 설정됨: menu={menu_name}, option={missing_option.get('option_name')}")
                
        #         # 필수 옵션 선택 요청 응답 컨텍스트 구성
        #         context = {
        #             "status": ResponseStatus.MISSING_REQUIRED_OPTIONS,
        #             "screen_state": screen_state,
        #             "menu_name": menu_name,
        #             "option_name": missing_option.get("option_name"),
        #             "options": ", ".join([detail.get("value") for detail in missing_option.get("option_details", [])])
        #         }
                
        #         # 응답 생성
        #         reply = intent_data.get("reply") or self.response_generator.generate_response(intent_data, language, context)
                
        #         # 기존 장바구니 가져오기
        #         if "cart" not in session:
        #             session["cart"] = []
                
        #         return {
        #             "intent_type": IntentType.OPTION_SELECT,  # 옵션 선택 의도로 변경
        #             "confidence": intent_data.get("confidence", 0.8),
        #             "raw_text": text,
        #             "screen_state": ScreenState.ORDER,  # 주문 화면으로 설정
        #             "data": {
        #                 "pre_text": text,
        #                 "post_text": intent_data.get("post_text", text),
        #                 "reply": reply,
        #                 "status": ResponseStatus.MISSING_REQUIRED_OPTIONS,
        #                 "language": language,
        #                 "session_id": session.get("id", ""),
        #                 "cart": session["cart"],
        #                 "contents": enriched_menus,
        #                 "store_id": store_id
        #             }
        #         }
        
        # # 4. 응답 메시지 생성 (LLM 사용)
        # context = {
        #     "status": status,
        #     "screen_state": screen_state,
        #     "menus": enriched_menus,  # 실제 메뉴 객체를 전달
        #     "cart": session.get("cart", [])
        # }

        # # LLM에 전달할 때 템플릿 변수 대신 실제 값을 전달
        # if "reply" in intent_data:
        #     # LLM에서 생성된 응답이 이미 있다면 그대로 사용
        #     reply = intent_data["reply"]
        # else:
        #     # LLM을 통해 새로운 응답 생성
        #     reply = self.response_generator.generate_response(intent_data, language, context)

        # # 혹시 모를 템플릿 변수가 포함된 경우 정리
        # if "{" in reply and "}" in reply:
        #     import re
        #     reply = re.sub(r'\{[^}]+\}', '', reply)

        # # 5. 장바구니 처리 (READY_TO_ADD_CART 상태인 경우)
        # cart = session.get("cart", [])
        # if status == ResponseStatus.READY_TO_ADD_CART:
        #     for menu in enriched_menus:
        #         cart = self.session_manager.add_to_cart(session["id"], menu)

        #     # 추가: 최신 장바구니 정보 다시 조회
        #     cart = self.session_manager.get_cart(session["id"])

        # LLM 응답 생성
        reply = intent_data.get("reply") or self.response_generator.generate_response(intent_data, language, context)
        
        # 템플릿 변수 제거
        if "{" in reply and "}" in reply:
            import re
            reply = re.sub(r'\{[^}]+\}', '', reply)
        
        # 6. 응답 구성
        return {
            "intent_type": IntentType.ORDER,
            "confidence": intent_data.get("confidence", 0.8),
            "raw_text": text,
            "screen_state": screen_state,
            "data": {
                "pre_text": text,
                "post_text": intent_data.get("post_text", text),
                "reply": reply,
                "status": status,
                "language": language,
                "session_id": session.get("id", ""),
                "cart": cart,
                "contents": enriched_menus,
                "store_id": store_id
            }
        }
    
    def process_option_selection(self, text: str, language: str, screen_state: str, store_id: int, session: Dict[str, Any]) -> Dict[str, Any]:
        """이전 컨텍스트를 기반으로 옵션 선택 처리"""
        try:
            # 세션 ID 확보
            session_id = session.get("id")
            if not session_id:
                print("[컨텍스트 처리] 세션 ID 없음")
                # 기본 의도 인식으로 처리
                intent_data = {
                    "intent_type": IntentType.UNKNOWN,
                    "confidence": 0.3
                }
                return self._build_response(
                    intent_data, text, language, screen_state, store_id, session,
                    ResponseStatus.UNKNOWN, reply="세션 정보가 없습니다. 다시 시도해주세요."
                )
            
            # 1. 이전 상태 확인 - 디버깅 정보 추가
            last_state = session.get("last_state", {})
            print(f"[컨텍스트 처리] 세션 ID: {session_id}, last_state 존재: {bool(last_state)}")
            print(f"[컨텍스트 처리] last_state 내용: {last_state.keys() if last_state else 'None'}")
            
            if not last_state or "menu" not in last_state:
                # 이전 상태가 없으면 기존 메뉴 검색
                print(f"[컨텍스트 처리] 이전 상태 없음, 일반 의도 인식 시도")
                # 기본 의도 인식으로 처리
                intent_data = {
                    "intent_type": IntentType.UNKNOWN,
                    "confidence": 0.3
                }
                return self._build_response(
                    intent_data, text, language, screen_state, store_id, session,
                    ResponseStatus.UNKNOWN, reply="이전 상태 정보가 없습니다. 처음부터 다시 주문해주세요."
                )
            
            # 2. 이전 메뉴 정보 가져오기 - 입력 검증 추가
            menu = last_state["menu"]
            if not menu or not isinstance(menu, dict):
                print(f"[컨텍스트 처리] 유효하지 않은 메뉴 정보: {menu}")
                intent_data = {"intent_type": IntentType.UNKNOWN, "confidence": 0.3}
                return self._build_response(
                    intent_data, text, language, screen_state, store_id, session,
                    ResponseStatus.UNKNOWN, reply="메뉴 정보가 유효하지 않습니다. 처음부터 다시 주문해주세요."
                )
            
            print(f"[컨텍스트 처리] 이전 메뉴: {menu.get('name')}")
            
            # 3. 이전에 물어본 옵션이 있는지 확인
            pending_option = last_state.get("pending_option")
            if not pending_option:
                print(f"[컨텍스트 처리] 대기 중인 옵션 없음")
                # 기본 의도 인식으로 처리
                intent_data = {
                    "intent_type": IntentType.UNKNOWN,
                    "confidence": 0.3
                }
                return self._build_response(
                    intent_data, text, language, screen_state, store_id, session,
                    ResponseStatus.UNKNOWN, reply="대기 중인 옵션이 없습니다. 처음부터 다시 주문해주세요."
                )
            
            print(f"[컨텍스트 처리] 대기 중인 옵션: {pending_option.get('option_name')}")
            
            # 4. 사용자 응답 파싱하여 옵션 값 도출
            selected_option = self.option_matcher.parse_option_response(text, pending_option, menu)
            if not selected_option:
                # 옵션 파싱 실패 시 다시 물어보기
                # 직접 메시지 구성 (템플릿 대신 하드코딩)
                option_name = pending_option.get("option_name", "")
                options_str = ", ".join(detail.get("value", "") for detail in pending_option.get("option_details", []))
                
                reply = f"{option_name} 선택을 이해하지 못했습니다. {options_str} 중에서 선택해주세요."
                
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
                
                # 응답 생성 - 여기서 LLM이 자연스러운 응답 생성
                reply = self.intent_recognizer.generate_option_selection_response(
                    menu, next_required_option, language
                )

                # 컨텍스트 구성
                # context = {
                #     "status": ResponseStatus.MISSING_REQUIRED_OPTIONS,
                #     "screen_state": screen_state,
                #     "menu_name": menu.get("name"),
                #     "option_name": option_name,
                #     "options": options_str
                # }
                
                # # 의도 데이터 구성
                # intent_data = {
                #     "intent_type": IntentType.OPTION_SELECT,
                #     "confidence": 0.8,
                #     "menu_name": menu.get("name"),
                #     "option_name": option_name
                # }
                
                # 응답 생성
                # reply = self.response_generator.generate_response(intent_data, language, context)
                
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

                # 대기열 상태 확인 추가
                print(f"[대기열 확인] 대기열 여부: {'order_queue' in session}")
                if "order_queue" in session:
                    print(f"[대기열 확인] 대기열 항목 수: {len(session['order_queue'])}")
                    if session['order_queue']:
                        print(f"[대기열 확인] 첫 번째 대기 메뉴: {session['order_queue'][0].get('name')}")
                
                # 장바구니에 메뉴 추가
                cart = self.session_manager.add_to_cart(session_id, menu)
                session["cart"] = cart
                self.session_manager._save_session(session_id, session)
                
                # 중요: 세션을 다시 가져와서 최신 상태 확인 (대기열이 소실될 수 있음)
                session = self.session_manager.get_session(session_id)
                
                # 대기열 상태 확인 추가
                print(f"[대기열 확인] 대기열 여부: {'order_queue' in session}")
                if "order_queue" in session:
                    print(f"[대기열 확인] 대기열 항목 수: {len(session['order_queue'])}")
                    if session['order_queue']:
                        print(f"[대기열 확인] 첫 번째 대기 메뉴: {session['order_queue'][0].get('name')}")
                
                # 장바구니에 메뉴 추가 후 상태 확인
                print(f"[대기열 확인] 장바구니 추가 후 대기열 여부: {'order_queue' in session}")
                if "order_queue" in session:
                    print(f"[대기열 확인] 장바구니 추가 후 대기열 개수: {len(session['order_queue'])}")
                    if session['order_queue']:
                        print(f"[대기열 확인] 다음 대기 메뉴: {session['order_queue'][0].get('name')}")

                # 옵션 문자열 생성
                option_strs = []
                for opt in menu.get("selected_options", []):
                    if opt.get("option_details"):
                        option_value = opt["option_details"][0].get("value", "")
                        option_strs.append(f"{opt['option_name']}: {option_value}")
                
                options_summary = f" ({', '.join(option_strs)})" if option_strs else ""
                completed_menu_name = menu.get("name") + options_summary
                
                # 대기열 추가 확인 (디버깅)
                print(f"[대기열 처리] 대기열 여부: {'order_queue' in session}")
                if "order_queue" in session and session["order_queue"]:
                    print(f"[대기열 처리] 대기열 항목 수: {len(session['order_queue'])}")
                    if len(session["order_queue"]) > 0:
                        print(f"[대기열 처리] 다음 메뉴: {session['order_queue'][0].get('name')}")

                # 대기열에 다음 메뉴가 있는지 확인 - 새로 추가된 부분
                if "order_queue" in session and session["order_queue"]:
                    # 대기열에서 다음 메뉴 가져오기
                    next_menu = session["order_queue"][0]
                    
                    # 대기열에서 해당 메뉴 제거
                    session["order_queue"].pop(0)
                    self.session_manager._save_session(session_id, session)
                    
                    # 다음 메뉴의 필수 옵션 확인
                    next_status = self.option_matcher.determine_menu_status(next_menu)
                    print(f"[대기열 처리] 다음 메뉴 상태: {next_status}")

                    if next_status == ResponseStatus.MISSING_REQUIRED_OPTIONS:
                        # 첫 번째 누락된 필수 옵션 찾기
                        missing_option = None
                        for option in next_menu.get("options", []):
                            if option.get("required", True) and not option.get("is_selected", False):
                                missing_option = option
                                break
                        
                        if missing_option:
                            # 다음 메뉴의 옵션 선택 프로세스 시작
                            session["last_state"] = {
                                "menu": next_menu,
                                "pending_option": missing_option
                            }
                            self.session_manager._save_session(session_id, session)
                            
                            # 직접 응답 구성 - LLM 응답에 의존하지 않고 하드코딩
                            menu_name = next_menu.get("name", "")
                            option_name = missing_option.get("option_name", "")
                            
                            # 옵션 값 목록 문자열
                            options_list = []
                            for detail in missing_option.get("option_details", []):
                                if detail and "value" in detail:
                                    options_list.append(detail["value"])
                            options_str = ", ".join(options_list)
                            
                            # 명시적 응답 구성 (템플릿 변수 사용 X)
                            reply = f"{menu_name}를 선택하셨네요. {option_name}을(를) 선택해주세요. ({options_str})"
                            
                            # 응답 구성
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
                                    "contents": [next_menu],
                                    "store_id": store_id
                                }
                            }
                        
                    else:
                        # 필수 옵션이 없는 메뉴는 바로 장바구니에 추가
                        cart = self.session_manager.add_to_cart(session_id, next_menu)
                        session["cart"] = cart
                        self.session_manager._save_session(session_id, session)
                        
                        # 다음 대기열 확인 (재귀적으로 처리)
                        if "order_queue" in session and session["order_queue"]:
                            return self._process_next_queued_menu(session_id, completed_menu_name, next_menu.get("name"), language, screen_state, store_id)
                        
                        # 대기열에 더 이상 메뉴가 없음 - 최종 응답
                        next_menu_name = next_menu.get("name")
                        reply = f"{completed_menu_name}과(와) {next_menu_name}을(를) 장바구니에 담았습니다. 더 필요한 것이 있으신가요?"
                
                else:
                    # 대기열에 메뉴가 없음 - 기존 응답 처리
                    context = {
                        "status": ResponseStatus.READY_TO_ADD_CART,
                        "screen_state": ScreenState.MAIN,
                        "menu_name": menu.get("name"),
                        "options_summary": options_summary
                    }

                    intent_data = {
                        "intent_type": IntentType.ORDER,
                        "confidence": 0.9,
                        "menu_name": menu.get("name")
                    }

                    reply = self.response_generator.generate_response(intent_data, language, context)
                    
                    if not reply:  # LLM 응답이 없는 경우 기본 응답
                        reply = f"{completed_menu_name}을(를) 장바구니에 담았어요. 더 필요한 것이 있으신가요?"
                
                # 주문 완료 후 상태 초기화 (대기열 처리가 남아있지 않은 경우)
                if not ("order_queue" in session and session["order_queue"]):
                    session["last_state"] = {}
                    self.session_manager._save_session(session_id, session)
                
                # 최종 응답 생성
                updated_cart = self.session_manager.get_cart(session_id)
                response = {
                    "intent_type": IntentType.ORDER,
                    "confidence": 0.9,
                    "raw_text": text,
                    "screen_state": ScreenState.MAIN,
                    "data": {
                        "pre_text": text,
                        "post_text": text,
                        "reply": reply,
                        "status": ResponseStatus.READY_TO_ADD_CART,
                        "language": language,
                        "session_id": session_id,
                        "cart": updated_cart,
                        "contents": [menu],
                        "store_id": store_id
                    }
                }
                
                return response
                
        except Exception as e:
            print(f"[옵션 선택 처리 오류] {e}")
            import traceback
            traceback.print_exc()
            
            # 오류 발생 시 안전한 응답 반환
            intent_data = {"intent_type": IntentType.UNKNOWN, "confidence": 0.3}
            return self._build_response(
                intent_data, text, language, screen_state, store_id, session,
                ResponseStatus.UNKNOWN, reply="옵션 처리 중 오류가 발생했습니다. 처음부터 다시 주문해주세요."
            )

    def _process_next_queued_menu(self, session_id: str, completed_menu_name: str, next_menu_name: str, language: str, screen_state: str, store_id: int) -> Dict[str, Any]:
        """대기열에서 다음 메뉴 처리"""
        session = self.session_manager.get_session(session_id)
        if not session or "order_queue" not in session or not session["order_queue"]:
            # 대기열이 비어있음 - 처리 완료 메시지 반환
            reply = f"{completed_menu_name}과(와) {next_menu_name}을(를) 장바구니에 담았습니다. 더 필요한 것이 있으신가요?"
            
            intent_data = {"intent_type": IntentType.ORDER, "confidence": 0.9}
            return self._build_response(
                intent_data, "", language, ScreenState.MAIN, store_id, session,
                ResponseStatus.READY_TO_ADD_CART, reply=reply
            )
        
        # 다음 대기 메뉴 가져오기
        next_menu = session["order_queue"][0]
        session["order_queue"].pop(0)
        self.session_manager._save_session(session_id, session)
        
        # 다음 메뉴의 필수 옵션 확인
        next_status = self.option_matcher.determine_menu_status(next_menu)
        
        if next_status == ResponseStatus.MISSING_REQUIRED_OPTIONS:
            # 첫 번째 필수 옵션 찾기
            missing_option = None
            for option in next_menu.get("options", []):
                if option.get("required", True) and not option.get("is_selected", False):
                    missing_option = option
                    break
            
            if missing_option:
                # 옵션 선택 프로세스 시작
                session["last_state"] = {
                    "menu": next_menu,
                    "pending_option": missing_option
                }
                self.session_manager._save_session(session_id, session)
                
                # # 변수 추출
                # menu_name = next_menu.get("name", "")
                # option_name = missing_option.get("option_name", "")
                # options_list = []
                # for detail in missing_option.get("option_details", []):
                #     if detail and "value" in detail:
                #         options_list.append(detail["value"])
                # options_str = ", ".join(options_list)
                
                # # 직접 응답 구성 (템플릿 변수 사용 X)
                # reply = f"{menu_name}를 선택하셨네요. {option_name}을(를) 선택해주세요. ({options_str})"
                
                # LLM으로 자연스러운 응답 생성
                reply = self.intent_recognizer.generate_option_selection_response(
                    next_menu, missing_option, language
                )

                return {
                    "intent_type": IntentType.OPTION_SELECT,
                    "confidence": 0.8,
                    "raw_text": "",
                    "screen_state": screen_state,
                    "data": {
                        "pre_text": "",
                        "post_text": "",
                        "reply": reply,
                        "status": ResponseStatus.MISSING_REQUIRED_OPTIONS,
                        "language": language,
                        "session_id": session_id,
                        "cart": session.get("cart", []),
                        "contents": [next_menu],
                        "store_id": store_id
                    }
                }
        else:
            # 필수 옵션이 없는 메뉴는 바로 장바구니에 추가
            cart = self.session_manager.add_to_cart(session_id, next_menu)
            third_menu_name = next_menu.get("name")
            
            # 다음 메뉴 확인 - 재귀적 처리
            if "order_queue" in session and session["order_queue"]:
                # 복합 처리 - 2개 이상 메뉴를 함께 처리
                completed_names = f"{completed_menu_name}, {next_menu_name}, {third_menu_name}"
                return self._process_next_queued_menu(session_id, completed_names, "", language, screen_state, store_id)
            else:
                # 모든 메뉴 처리 완료
                reply = f"{completed_menu_name}, {next_menu_name}, {third_menu_name}을(를) 모두 장바구니에 담았습니다. 더 필요한 것이 있으신가요?"
                
                # 상태 초기화
                session["last_state"] = {}
                self.session_manager._save_session(session_id, session)
                
                intent_data = {"intent_type": IntentType.ORDER, "confidence": 0.9}
                return self._build_response(
                    intent_data, "", language, ScreenState.MAIN, store_id, session,
                    ResponseStatus.READY_TO_ADD_CART, reply=reply
                )

    def _build_response(self, intent_data: Dict[str, Any], text: str, language: str, screen_state: str, store_id: int, session: Dict[str, Any], status: str, contents: List[Dict[str, Any]] = None, reply: str = None) -> Dict[str, Any]:
        """응답 구성 헬퍼 메서드"""
        # 세션 ID 확인
        session_id = session.get("id", "")
        
        # 장바구니 정보 확인
        cart = session.get("cart", [])
        
        # 컨텐츠가 None이면 빈 리스트로 초기화
        if contents is None:
            contents = []

         # 응답 메시지 확인 - 템플릿 변수가 있으면 치환 시도
        final_reply = reply or intent_data.get("reply", "")
        if '{' in final_reply and '}' in final_reply:
            # 컨텍스트 구성 시도
            context = {}
            
            # 메뉴 정보가 있으면 추가
            if contents and len(contents) > 0:
                menu = contents[0]
                context["menu_name"] = menu.get("name", "")
                
                # 옵션 정보 추가
                options_summary = ""
                if menu.get("selected_options"):
                    option_strs = []
                    for opt in menu.get("selected_options", []):
                        if opt.get("option_details"):
                            option_value = opt["option_details"][0].get("value", "")
                            option_strs.append(f"{opt['option_name']}: {option_value}")
                    
                    options_summary = f" ({', '.join(option_strs)})" if option_strs else ""
                
                context["options_summary"] = options_summary
                
                # 현재 필요한 옵션 정보 추가
                if session.get("last_state", {}).get("pending_option"):
                    pending_option = session["last_state"]["pending_option"]
                    context["option_name"] = pending_option.get("option_name", "")
                    context["options"] = ", ".join([detail.get("value", "") for detail in pending_option.get("option_details", [])])
            
            # 템플릿 변수 치환
            final_reply = self._replace_template_vars(final_reply, context)
        
        return {
            "intent_type": intent_data.get("intent_type", IntentType.UNKNOWN),
            "confidence": intent_data.get("confidence", 0.5),
            "raw_text": text,
            "screen_state": screen_state,
            "data": {
                "pre_text": text,
                "post_text": intent_data.get("post_text", text),
                "reply": reply or intent_data.get("reply", ""),
                "status": status,
                "language": language,
                "session_id": session_id,
                "cart": cart,
                "contents": contents,
                "store_id": store_id
            }
        }

    def _replace_template_vars(self, template: str, context: Dict[str, Any]) -> str:
        """템플릿 변수 치환"""
        if not template:
            return ""
            
        result = template
        for key, value in context.items():
            placeholder = "{" + key + "}"
            if placeholder in result:
                result = result.replace(placeholder, str(value))
        return result