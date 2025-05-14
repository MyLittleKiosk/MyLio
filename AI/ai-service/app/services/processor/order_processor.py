# app/services/processor/order_processor.py
import re
from typing import Dict, Any, Optional, List
from app.models.schemas import IntentType, ScreenState, Language, ResponseStatus
from app.services.processor.base_processor import BaseProcessor
from app.services.option.option_matcher import OptionMatcher
from app.services.response.response_generator import ResponseGenerator
from app.services.response_service import ResponseService  
from app.models.schemas import ResponseStatus

class OrderProcessor(BaseProcessor):
    """주문 처리 프로세서"""
    
    def __init__(self, response_generator: ResponseGenerator, menu_service, session_manager):
        """프로세서 초기화"""
        self.response_generator = response_generator
        self.menu_service = menu_service
        self.session_manager = session_manager
        self.option_matcher = OptionMatcher()
    
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
                    "options": [],  # 옵션 배열 초기화
                    "selected_options": [],
                    "is_corrected": menu_name.lower() != menu_match["name_kr"].lower(),
                    "original_name": menu_name if menu_name.lower() != menu_match["name_kr"].lower() else None
                }

                # 옵션 정보 복사 (additional_price 포함)
                for option in menu_match["options"]:
                    enriched_option = {
                        "option_id": option.get("option_id"),
                        "option_name": option.get("option_name"),
                        "option_name_en": option.get("option_name_en"),
                        "required": option.get("required", False),
                        "is_selected": False,
                        "option_details": []
                    }
                    
                    # 옵션 상세 정보 복사 (additional_price 포함)
                    for detail in option.get("option_details", []):
                        enriched_option["option_details"].append({
                            "id": detail.get("id"),
                            "value": detail.get("value"),
                            "additional_price": detail.get("additional_price", 0)
                        })
                    
                    enriched_menu["options"].append(enriched_option)
                
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
                            # 원본 옵션에서 additional_price 가져오기
                            for original_option in menu_match["options"]:
                                if original_option["option_id"] == matched_option["option_id"]:
                                    for original_detail in original_option["option_details"]:
                                        if original_detail["id"] == matched_option["option_details"][0]["id"]:
                                            matched_option["option_details"][0]["additional_price"] = original_detail.get("additional_price", 0)
                                            break
                                    break
                            
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
                pending_option = {
                    "option_id": missing_option.get("option_id"),
                    "option_name": missing_option.get("option_name"),
                    "required": missing_option.get("required", False),
                    "option_details": []
                }
                
                # 옵션 상세 정보 복사 (additional_price 포함)
                for detail in missing_option.get("option_details", []):
                    detail_copy = {
                        "id": detail.get("id"),
                        "value": detail.get("value"),
                        "additional_price": detail.get("additional_price", 0)  # additional_price 추가
                    }
                    pending_option["option_details"].append(detail_copy)
                
                session["last_state"] = {
                    "menu": menu,
                    "pending_option": pending_option
                }
                
                # Redis에 세션 상태 즉시 업데이트 (중요!)
                self.session_manager._save_session(session["id"], session)
                
                print(f"[세션 업데이트] 세션 ID: {session['id']}, last_state 설정됨: menu={menu_name}, option={missing_option.get('option_name')}")
                
                # 필수 옵션 선택 요청 응답 컨텍스트 구성
                context = {
                    "status": ResponseStatus.MISSING_REQUIRED_OPTIONS,
                    "screen_state": screen_state,
                    "menu_name": menu_name,
                    "option_name": missing_option.get("option_name"),
                    "options": ", ".join([detail.get("value") for detail in missing_option.get("option_details", [])])
                }
                
                # 응답 생성
                reply = intent_data.get("reply") or self.response_generator.generate_response(intent_data, language, context)
                
                # 기존 장바구니 가져오기
                if "cart" not in session:
                    session["cart"] = []
                
                return {
                    "intent_type": IntentType.OPTION_SELECT,  # 옵션 선택 의도로 변경
                    "confidence": intent_data.get("confidence", 0.8),
                    "raw_text": text,
                    "screen_state": ScreenState.ORDER,  # 주문 화면으로 설정
                    "data": {
                        "pre_text": text,
                        "post_text": intent_data.get("post_text", text),
                        "reply": reply,
                        "status": ResponseStatus.MISSING_REQUIRED_OPTIONS,
                        "language": language,
                        "session_id": session.get("id", ""),
                        "cart": session["cart"],
                        "contents": enriched_menus,
                        "store_id": store_id
                    }
                }
        
        # 4. 응답 메시지 생성 (LLM 사용)
        context = {
            "status": status,
            "screen_state": screen_state,
            "menus": enriched_menus,  # 실제 메뉴 객체를 전달
            "cart": session.get("cart", [])
        }

        # LLM에 전달할 때 템플릿 변수 대신 실제 값을 전달
        if "reply" in intent_data:
            # LLM에서 생성된 응답이 이미 있다면 그대로 사용
            reply = intent_data["reply"]
        else:
            # LLM을 통해 새로운 응답 생성
            reply = self.response_generator.generate_response(intent_data, language, context)

        # 혹시 모를 템플릿 변수가 포함된 경우 정리
        if "{" in reply and "}" in reply:
            import re
            reply = re.sub(r'\{[^}]+\}', '', reply)

        # 5. 장바구니 처리 (READY_TO_ADD_CART 상태인 경우)
        cart = session.get("cart", [])
        if status == ResponseStatus.READY_TO_ADD_CART:
            for menu in enriched_menus:
                cart = self.session_manager.add_to_cart(session["id"], menu)

            # 추가: 최신 장바구니 정보 다시 조회
            cart = self.session_manager.get_cart(session["id"])
        
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
                
                # 또는 응답 생성기를 사용하는 경우 다음과 같이:
                # intent_data = {
                #     "intent_type": IntentType.OPTION_SELECT,
                #     "confidence": 0.7,
                #     "menu_name": menu.get("name", ""),
                #     "option_name": pending_option.get("option_name", "")
                # }
                # context = {
                #     "status": ResponseStatus.UNKNOWN,
                #     "option_name": pending_option.get("option_name", ""),
                #     "options": ", ".join(detail.get("value", "") for detail in pending_option.get("option_details", [])),
                #     "menu_name": menu.get("name", "")
                # }
                # reply = self.response_generator.generate_response(intent_data, language, context)
                
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
                
                # 컨텍스트 구성
                context = {
                    "status": ResponseStatus.MISSING_REQUIRED_OPTIONS,
                    "screen_state": screen_state,
                    "menu_name": menu.get("name"),
                    "option_name": option_name,
                    "options": options_str
                }
                
                # 의도 데이터 구성
                intent_data = {
                    "intent_type": IntentType.OPTION_SELECT,
                    "confidence": 0.8,
                    "menu_name": menu.get("name"),
                    "option_name": option_name
                }
                
                # 응답 생성
                reply = self.response_generator.generate_response(intent_data, language, context)
                
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
                print(f"[선택된 옵션] {[opt.get('option_name') for opt in menu.get('selected_options', [])]}")

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
                
                # response_generator 사용
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