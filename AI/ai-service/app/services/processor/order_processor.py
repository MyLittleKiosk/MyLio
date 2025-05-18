from typing import Dict, Any, Optional, List
import copy

from app.models.schemas import IntentType, ScreenState, Language, ResponseStatus
from app.services.processor.base_processor import BaseProcessor
from app.services.response.response_generator import ResponseGenerator
from app.services.option.option_handler import OptionHandler

class OrderProcessor(BaseProcessor):
    """주문 처리 프로세서"""
    
    def __init__(self, response_generator: ResponseGenerator, menu_service, session_manager, intent_recognizer):
        """프로세서 초기화"""
        self.response_generator = response_generator
        self.menu_service = menu_service
        self.session_manager = session_manager
        self.intent_recognizer = intent_recognizer
        self.option_handler = OptionHandler()
    
    def process(self, intent_data: Dict[str, Any], text: str, language: str, screen_state: str, store_id: int, session: Dict[str, Any]) -> Dict[str, Any]:
        """주문 의도 처리"""
        print(f"[주문 처리] 시작: 텍스트='{text}', 화면 상태={screen_state}")
        
        # 세션 ID 가져오기
        session_id = session.get("id", "")
        
        # 취소 요청 처리
        if self._is_cancellation_request(text, language):
            print("[주문 처리] 취소 요청 감지")
            # 현재 메뉴 선택 상태 및 대기열 초기화
            session["last_state"] = {}
            if "order_queue" in session:
                session["order_queue"] = []
            
            # 세션 저장
            self.session_manager._save_session(session_id, session)
            
            # 취소 응답 생성
            return self._generate_cancellation_response(text, language, screen_state, store_id, session)
        
        # LLM 인식 메뉴 목록 확인
        if "menus" not in intent_data or not intent_data["menus"]:
            print("[주문 처리] 인식된 메뉴 없음")
            
            # 응답 컨텍스트 구성
            context = {
                "status": ResponseStatus.UNKNOWN,
                "screen_state": screen_state
            }
            
            # 응답 생성
            reply = intent_data.get("reply") or self.response_generator.generate_response(
                intent_data, language, context
            )
            
            return self._build_response(
                intent_data, text, language, screen_state, store_id, session,
                ResponseStatus.UNKNOWN, reply=reply
            )
        
        # 장바구니에 넣을 메뉴와 옵션 선택이 필요한 메뉴 목록
        ready_to_add_menus = []
        pending_option_menus = []
        
        # 모든 메뉴 순회하며 처리
        for menu_data in intent_data["menus"]:
            # 메뉴 정보 조회
            menu_name = menu_data.get("menu_name", "")
            print(f"[주문 처리] 메뉴 처리: {menu_name}")
            
            full_menu = self.menu_service.find_menu_by_name(menu_name, store_id)
            
            if not full_menu:
                print(f"[주문 처리] 메뉴 정보 조회 실패: {menu_name}")
                continue
            
            # 디버깅 추가 - 메뉴 정보 확인
            print(f"[주문 처리] 메뉴 정보 조회 결과: {full_menu}")
            
            # 메뉴 기본 정보 확인
            if "menu_id" not in full_menu or not full_menu.get("id"):
                print(f"[주문 처리] 메뉴 ID 누락, 메뉴 이름 정확도 확인 필요: {menu_name}")
                # 여기서 메뉴 이름 유사도 검색 시도 (유사 이름 매칭)
                similar_menu = self.menu_service.find_similar_menu(menu_name, store_id)
                if similar_menu:
                    print(f"[주문 처리] 유사 메뉴 발견: {similar_menu.get('name_kr')}")
                    full_menu = similar_menu
                else:
                    continue
            
            # 인식된 메뉴 정보를 전체 메뉴 정보로 보강
            full_menu["quantity"] = menu_data.get("quantity", 1)
            
            # 인식된 옵션 정보 추가
            if "options" in menu_data and menu_data["options"]:
                print(f"[주문 처리] LLM이 인식한 옵션 정보: {menu_data['options']}")
                for menu_option in menu_data["options"]:
                    option_name = menu_option.get("option_name", "")
                    option_value = menu_option.get("option_value", "")
                    option_detail_id = menu_option.get("option_detail_id")
                    
                    print(f"[주문 처리] 옵션 매칭 시도: 이름={option_name}, 값={option_value}, ID={option_detail_id}")
                    
                    # 옵션 매칭 시도
                    matched_option = self._match_menu_option(full_menu, option_name, option_value, option_detail_id)
                    if matched_option:
                        print(f"[주문 처리] 옵션 매칭 성공: {matched_option.get('option_name')}={matched_option['option_details'][0]['value']} (ID: {matched_option['option_details'][0]['id']})")
                        # 메뉴에 옵션 적용
                        self.option_handler.option_matcher.apply_option_to_menu(full_menu, matched_option)
                    else:
                        print(f"[주문 처리] 옵션 매칭 실패: {option_name}={option_value} (요청 ID: {option_detail_id})")
                        
                        # id가 제공된 경우 직접 매칭 시도
                        if option_detail_id:
                            print(f"[주문 처리] ID 기반 직접 매칭 시도: option_detail_id={option_detail_id}")
                            for option in full_menu.get("options", []):
                                if option_name.lower() in option.get("option_name", "").lower() or option.get("option_name", "").lower() in option_name.lower():
                                    for detail in option.get("option_details", []):
                                        if detail.get("id") == option_detail_id:
                                            print(f"[주문 처리] ID로 옵션 직접 매칭 성공: {option.get('option_name')}={detail.get('value')}")
                                            option["is_selected"] = True
                                            option["selected_id"] = option_detail_id
                                            # 총 가격 업데이트
                                            self.option_handler.calculate_total_price(full_menu)
                                            break
            
            # 주문 메뉴 상태 확인
            menu_status = self.option_handler.determine_menu_status(full_menu)
            
            # 필수 옵션이 누락된 경우: 옵션 선택이 필요한 메뉴 목록에 추가
            if menu_status == ResponseStatus.MISSING_REQUIRED_OPTIONS:
                print(f"[주문 처리] 메뉴 {menu_name}의 필수 옵션 누락, 옵션 선택 필요 목록에 추가")
                pending_option_menus.append(full_menu)
            
            # 장바구니에 추가 가능한 경우: 바로 장바구니에 추가
            elif menu_status == ResponseStatus.READY_TO_ADD_CART:
                print(f"[주문 처리] 메뉴 {menu_name} 장바구니에 바로 추가")
                ready_to_add_menus.append(full_menu)
                self.session_manager.add_to_cart(session_id, full_menu)
        
        # 옵션 선택이 필요한 메뉴가 있는 경우
        if pending_option_menus:
            print(f"[주문 처리] 옵션 선택이 필요한 메뉴 {len(pending_option_menus)}개 있음")
            
            # 첫 번째 메뉴 처리 시작
            first_pending_menu = pending_option_menus[0]
            
            # 추가 메뉴가 있는 경우 대기열에 추가 (첫 번째 메뉴 제외)
            if len(pending_option_menus) > 1:
                print(f"[주문 처리] 추가 메뉴 {len(pending_option_menus)-1}개 대기열에 추가")
                print(f"[주문 처리] 대기열에 추가하는 메뉴: {pending_option_menus[1:]}")

                self.session_manager.add_to_order_queue(session_id, pending_option_menus[1:])

                # 🔻 **딱 한 번** 최신 세션을 가져와 session 에 할당
                session = self.session_manager.get_session(session_id)   

                # 디버깅
                if "order_queue" in session:
                    print(f"[주문 처리] 대기열 추가 후 크기: {len(session['order_queue'])}")
                    for idx, menu in enumerate(session['order_queue']):
                        print(f"[주문 처리] 대기열 아이템 {idx}: "
                            f"{menu.get('name_kr', '') or menu.get('menu_name', '')}")
            
            # 다음 필수 옵션 가져오기
            next_option = self.option_handler.get_next_required_option(first_pending_menu)
            
            if next_option:
                # 기존 장바구니 정보 보존
                current_cart = self.session_manager.get_cart(session_id)
                
                # 세션에 메뉴 및 다음 옵션 정보 저장
                session["last_state"] = {
                    "menu": {
                        "menu_id": first_pending_menu.get("id"),
                        "name": first_pending_menu.get("name_kr"),
                        "name_en": first_pending_menu.get("name_en"),
                        "description": first_pending_menu.get("description"),
                        "base_price": first_pending_menu.get("price", 0),
                        "total_price": first_pending_menu.get("price", 0),
                        "image_url": first_pending_menu.get("image_url"),
                        "options": first_pending_menu.get("options", []),
                        "quantity": first_pending_menu.get("quantity", 1)
                    },
                    "pending_option": next_option,
                    "pending_option_menus": pending_option_menus
                }
                
                # 기존 장바구니 정보 복원
                if current_cart:
                    session["cart"] = current_cart
                
                # 세션 저장
                self.session_manager._save_session(session_id, session)
                
                # 메뉴와 옵션 정보 추출
                menu_name = first_pending_menu.get("name_kr", "메뉴")
                option_name = next_option.get("option_name", "옵션")
                
                # LLM이 생성한 응답이 있으면 그것을 사용, 없으면 직접 구성
                # if intent_data.get("reply") and "선택해주세요" in intent_data.get("reply"):
                #     reply = intent_data.get("reply")
                # else:
                #     # 다국어 메시지 생성
                #     reply = self._generate_option_selection_message(menu_name, option_name, "", language)
                reply = self._generate_option_selection_message(menu_name, option_name, "", language)
                
                # 이미 추가된 메뉴가 있는 경우 안내 포함
                if ready_to_add_menus:
                    menu_names = ", ".join([menu.get("name_kr") for menu in ready_to_add_menus])
                    
                    if language == Language.KR:
                        cart_message = f"주문하신 메뉴가 장바구니에 추가되었어요. "
                    elif language == Language.EN:
                        cart_message = f"{menu_names} has been added to your cart. "
                    elif language == Language.CN:
                        cart_message = f"{menu_names}已添加到您的购物车。"
                    elif language == Language.JP:
                        cart_message = f"{menu_names}はカートに追加されました。"
                    else:
                        cart_message = f"{menu_names} has been added to your cart. "
                        
                    #reply = cart_message + reply
                
                # 의도 타입 변경 - OPTION_SELECT로 설정
                intent_data["intent_type"] = IntentType.OPTION_SELECT
                
                # 응답 데이터 생성 시 필요 없는 정보 제거 및 selected_options 추가
                cleaned_menu = {
                    "menu_id": first_pending_menu.get("id"),
                    "name": first_pending_menu.get("name_kr"),
                    "name_en": first_pending_menu.get("name_en"),
                    "description": first_pending_menu.get("description"),
                    "base_price": first_pending_menu.get("price", 0),
                    "total_price": first_pending_menu.get("price", 0),
                    "image_url": first_pending_menu.get("image_url"),
                    "quantity": first_pending_menu.get("quantity", 1),
                    "options": first_pending_menu.get("options", []),
                    "selected_options": []
                }
                
                # 응답 반환
                return self._build_response(
                    intent_data, text, language, ScreenState.ORDER, store_id, session,
                    ResponseStatus.MISSING_REQUIRED_OPTIONS, contents=[cleaned_menu], reply=reply
                )
        
        # 모든 메뉴가 장바구니에 바로 추가된 경우
        elif ready_to_add_menus:
            print(f"[주문 처리] 모든 메뉴 {len(ready_to_add_menus)}개가 장바구니에 추가됨")
            
            # 장바구니에 대한 응답 메시지 생성
            menu_names = ", ".join([menu.get("name_kr", "") or menu.get("name", "") for menu in ready_to_add_menus])
            
            if language == Language.KR:
                reply = f"{menu_names}가 장바구니에 담겼어요."
            elif language == Language.EN:
                reply = f"{menu_names} has been added to your cart."
            elif language == Language.CN:
                reply = f"{menu_names}已添加到您的购物车。"
            elif language == Language.JP:
                reply = f"{menu_names}はカートに追加されました。"
            else:
                reply = f"{menu_names} has been added to your cart."
            
            # LLM이 생성한 응답이 있으면 그것을 사용
            # if intent_data.get("reply"):
            #     reply = intent_data.get("reply")
            
            # 응답 반환
            return self._build_response(
                intent_data, text, language, ScreenState.MAIN, store_id, session,
                ResponseStatus.READY_TO_ADD_CART, contents=ready_to_add_menus, reply=reply
            )
        
        # 처리할 메뉴가 없는 경우
        return self._build_response(
            intent_data, text, language, ScreenState.MAIN, store_id, session,
            ResponseStatus.UNKNOWN, reply=intent_data.get("reply", "처리할 메뉴가 없습니다.")
        )
    
    def process_option_selection(self, text: str, language: str, screen_state: str, store_id: int, session: Dict[str, Any]) -> Dict[str, Any]:
        """옵션 선택 처리"""
        print(f"[옵션 선택 처리] 시작: 텍스트='{text}', 화면 상태={screen_state}")
        
        # 기본 intent_data 정의
        intent_data = {
            "intent_type": IntentType.OPTION_SELECT,
            "confidence": 0.9,
            "post_text": text
        }
        
        # 세션 ID 가져오기
        session_id = session.get("id", "")
        
        # 취소 요청 처리
        if self._is_cancellation_request(text, language):
            print("[옵션 선택 처리] 취소 요청 감지")
            # 현재 메뉴 선택 상태 및 대기열 초기화
            session["last_state"] = {}
            if "order_queue" in session:
                session["order_queue"] = []
            
            # 세션 저장
            self.session_manager._save_session(session_id, session)
            
            # 취소 응답 생성
            return self._generate_cancellation_response(text, language, screen_state, store_id, session)
        
        # 세션에서 현재 처리 중인 메뉴와 옵션 가져오기
        menu = session.get("last_state", {}).get("menu", {})
        pending_option = session.get("last_state", {}).get("pending_option", {})
        
        if not menu or not pending_option:
            print("[옵션 선택 처리] 진행 중인 메뉴 또는 옵션 정보 없음")
            
            # 의도 데이터 구성
            intent_data = {
                "intent_type": IntentType.UNKNOWN,
                "confidence": 0.3,
                "post_text": text
            }
            
            # 메인 화면으로 리디렉션
            return self._build_response(
                intent_data, text, language, ScreenState.MAIN, store_id, session,
                ResponseStatus.UNKNOWN, reply="선택 중인 메뉴가 없습니다."
            )
        
        # 텍스트에서 LLM을 통해 옵션 값 추출 시도
        # 1. 현재 필수 옵션 처리
        all_selected_options = []
        selected_option = self.option_handler.process_option_selection(text, pending_option, menu)
        
        if selected_option:
            new_id = selected_option["option_details"][0]["id"]

            # ⚠️ 이미 같은 값(Ice → Ice 등)이면 덮어쓰지 않는다
            if pending_option.get("selected_id") == new_id:
                print(f"[옵션 선택 처리] {pending_option['option_name']} 이미 {selected_option['option_details'][0]['value']} 로 선택돼 있어 변경하지 않음")
            else:
                self.option_handler.option_matcher.apply_option_to_menu(menu, selected_option)
                all_selected_options.append(selected_option)
        # 2. 추가 옵션 처리 (샷 옵션 등 모든 옵션 처리)
        menu_options = menu.get("options", [])
        
        # 추가 옵션 키워드 맵핑
        keyword_option_map = {
            "샷": ["샷", "shot"],
            "얼음": ["얼음", "ice"],
            "시럽": ["시럽", "syrup"],
            "우유": ["우유", "milk"]
        }
        
        # LLM을 통해 텍스트 분석 - 다양한 옵션 추출 시도
        # 텍스트에서 키워드 기반 검색
        for keyword_type, keywords in keyword_option_map.items():
            if any(kw in text.lower() for kw in keywords):
                for option in menu_options:
                    option_name = option.get("option_name", "").lower()
                    # 키워드 유형에 맞는 옵션 찾기
                    if any(kw in option_name for kw in keywords):
                        # 이미 선택된 옵션은 건너뛰기
                        if option.get("is_selected"):
                            continue
                        
                        current_option = {
                            "option_id": option.get("option_id"),
                            "option_name": option.get("option_name"),
                            "required": option.get("required"),
                            "option_details": option.get("option_details", [])
                        }
                        
                        # 옵션 매칭 시도
                        option_match = self.option_handler.process_option_selection(text, current_option, menu)
                        if option_match:
                            print(f"[옵션 선택 처리] 추가 옵션 선택 성공: {current_option.get('option_name')}={option_match.get('option_details', [{}])[0].get('value', '')}")
                            self.option_handler.option_matcher.apply_option_to_menu(menu, option_match)
                            all_selected_options.append(option_match)
        
        # remaining_required = [
        #     opt for opt in menu["options"]
        #     if opt.get("required") and not opt.get("is_selected")
        # ]
        # for opt in remaining_required:
        #     #opt_match = self.option_handler.option_matcher.parse_option_response(text, opt, menu)
        #     opt_match = self.option_handler.process_option_selection(text, opt, menu)
        #     if opt_match:
        #         print(f"[옵션 선택 처리] 추가 필수 옵션 선택 성공: "
        #             f"{opt.get('option_name')}="
        #             f"{opt_match['option_details'][0]['value']}")
        #         self.option_handler.option_matcher.apply_option_to_menu(menu, opt_match)
        #         all_selected_options.append(opt_match)

        remaining_any = [
            opt for opt in menu["options"]
            if not opt.get("is_selected")
        ]        

        for opt in remaining_any:     
            if opt.get("is_selected"):
                continue  # 이미 선택된 옵션은 건너뜀
            #opt_match = self.option_handler.option_matcher.parse_option_response(text, opt, menu)
            opt_match = self.option_handler.process_option_selection(text, opt, menu)
            if opt_match:
                print(f"[옵션 선택 처리] 추가 옵션 선택 성공: "
                    f"{opt.get('option_name')}="
                    f"{opt_match['option_details'][0]['value']}")
                self.option_handler.option_matcher.apply_option_to_menu(menu, opt_match)
                all_selected_options.append(opt_match)
                
        # 메뉴 상태 확인
        menu_status = self.option_handler.determine_menu_status(menu)
        
        # 다음 필수 옵션이 있는 경우
        if menu_status == ResponseStatus.MISSING_REQUIRED_OPTIONS:
            # 다음 필수 옵션 가져오기
            next_option = self.option_handler.get_next_required_option(menu)
            
            if next_option:
                print(f"[옵션 선택 처리] 다음 필수 옵션: {next_option.get('option_name')}")
                
                # 세션에 메뉴 및 다음 옵션 정보 저장
                session["last_state"]["menu"] = menu
                session["last_state"]["pending_option"] = next_option
                
                # 세션 저장
                self.session_manager._save_session(session_id, session)
                
                # 응답 생성
                if 'reply' in locals() and reply:
                    pass  # 이미 reply가 있으면 그대로 사용
                else:
                    # 기본 메시지 생성
                    if language == Language.KR:
                        reply = f"{menu.get('name')}의 필수 옵션이 아직 선택되지 않았어요."
                    elif language == Language.EN:
                        reply = f"Selecting options for {menu.get('name')} is required. Please select options."
                    else:
                        reply = f"{menu.get('name')}의 필수 옵션을 선택해주세요."
                
                # 응답 반환
                return self._build_response(
                    intent_data, text, language, ScreenState.ORDER, store_id, session,
                    ResponseStatus.MISSING_REQUIRED_OPTIONS, contents=[menu], reply=reply
                )
        
        # 모든 필수 옵션 선택 완료 - 장바구니에 추가
        print("[옵션 선택 처리] 모든 필수 옵션 선택 완료")
        
        # 선택된 옵션 목록 정리
        selected_options_list = []
        for option in menu.get("options", []):
            if option.get("is_selected"):
                option_details = []
                for detail in option.get("option_details", []):
                    if detail.get("id") == option.get("selected_id"):
                        option_details.append({
                            "id": detail.get("id"),
                            "value": detail.get("value"),
                            "additional_price": detail.get("additional_price", 0)
                        })
                
                if option_details:
                    selected_options_list.append({
                        "option_id": option.get("option_id"),
                        "option_name": option.get("option_name"),
                        "option_name_en": option.get("option_name_en"),
                        "required": option.get("required", False),
                        "is_selected": True,
                        "option_details": option_details
                    })

        print(f"[옵션 선택 처리] 선택된 옵션 목록: {selected_options_list}")

        # 장바구니에 추가할 메뉴 데이터 준비
        # base_price와 menu_id가 제대로 설정되어 있는지 확인
        base_price = menu.get("base_price") or menu.get("price") or 0
        if base_price == 0:
            # 메뉴 서비스에서 원본 메뉴 정보 가져와 가격 확인
            original_menu = self.menu_service.find_menu_by_id(menu.get("menu_id") or menu.get("id"), store_id)
            if original_menu:
                base_price = original_menu.get("price", 0)
                print(f"[옵션 선택 처리] 원본 메뉴에서 가격 복구: {base_price}")
        
        # 총 가격 계산 (base_price + 옵션 추가 가격)
        total_price = base_price
        for opt in selected_options_list:
            for detail in opt.get("option_details", []):
                total_price += detail.get("additional_price", 0)
        
        # 샷 옵션 특별 처리 - 텍스트에 '샷' 키워드가 있지만 아직 샷 옵션이 적용되지 않은 경우
        if "샷" in text.lower() or "shot" in text.lower():
            # 메뉴에서 샷 옵션 찾기
            shot_option = None
            for opt in menu.get("options", []):
                if opt.get("option_name") == "샷옵션" and not opt.get("is_selected"):
                    shot_option = opt
                    break
            
            # 샷 옵션이 있고 선택되지 않은 경우
            if shot_option:
                # 샷 추가 상세 옵션 찾기
                shot_detail = None
                for detail in shot_option.get("option_details", []):
                    if "추가" in detail.get("value", ""):
                        shot_detail = detail
                        break
                
                # 샷 옵션 적용
                if shot_detail:
                    print(f"[옵션 선택 처리] 샷 추가 옵션 추가: {shot_detail.get('value')}")
                    
                    # 옵션 정보 구성
                    selected_shot_option = {
                        "option_id": shot_option.get("option_id"),
                        "option_name": shot_option.get("option_name"),
                        "option_name_en": shot_option.get("option_name_en"),
                        "required": shot_option.get("required", False),
                        "is_selected": True,
                        "option_details": [{
                            "id": shot_detail.get("id"),
                            "value": shot_detail.get("value"),
                            "additional_price": shot_detail.get("additional_price", 0)
                        }]
                    }
                    
                    # 선택된 옵션 목록에 추가
                    selected_options_list.append(selected_shot_option)
                    
                    # 메뉴 옵션 정보 업데이트
                    shot_option["is_selected"] = True
                    shot_option["selected_id"] = shot_detail.get("id")
                    
                    # 총 가격 업데이트
                    total_price += shot_detail.get("additional_price", 0)
                    
                    print(f"[옵션 선택 처리] 샷 옵션 적용 후 가격: {total_price}")
        
        print(f"[옵션 선택 처리] 최종 메뉴 가격: base_price={base_price}, total_price={total_price}")
        
        cart_menu = {
            "menu_id": menu.get("menu_id") or menu.get("id"),
            "name": menu.get("name") or menu.get("name_kr"),
            "name_en": menu.get("name_en"),
            "quantity": menu.get("quantity", 1),
            "base_price": base_price,
            "total_price": total_price,
            "options": menu.get("options", []),
            "selected_options": selected_options_list
        }
        
        # 디버깅 - 필수 정보 확인
        if not cart_menu.get("menu_id") or not cart_menu.get("name"):
            print(f"[경고] 불완전한 메뉴 정보: menu_id={cart_menu.get('menu_id')}, name={cart_menu.get('name')}")
            # 세션에서 메뉴 이름 확인 시도
            if "pending_option_menus" in session.get("last_state", {}):
                pending_menus = session["last_state"]["pending_option_menus"]
                if pending_menus and len(pending_menus) > 0:
                    first_menu = pending_menus[0]
                    if not cart_menu.get("menu_id"):
                        cart_menu["menu_id"] = first_menu.get("id") or first_menu.get("menu_id")
                    if not cart_menu.get("name"):
                        cart_menu["name"] = first_menu.get("name_kr") or first_menu.get("name")
                    if not cart_menu.get("base_price") or cart_menu.get("base_price") == 0:
                        cart_menu["base_price"] = first_menu.get("price", 0)

        print(f"[옵션 선택 처리] 장바구니 추가 메뉴: {cart_menu}")
        self.session_manager.add_to_cart(session_id, cart_menu)

        # 장바구니 업데이트 확인
        updated_cart = self.session_manager.get_cart(session_id)
        print(f"[카트 추가 성공] 이전: {len(session.get('cart', []))}, 현재: {len(updated_cart)}")

        # 세션에서 처리 중인 메뉴 정보만 제거, order_queue 유지
        session["last_state"] = {}

        # 대기열 정보 보존
        if "order_queue" in session:
            print(f"[옵션 선택 처리] 기존 대기열 유지: {len(session['order_queue'])}개 항목")

        # 카트 정보 유지를 위해 최신 카트 정보를 세션에 업데이트
        if updated_cart and len(updated_cart) > 0:
            session["cart"] = updated_cart

        self.session_manager._save_session(session_id, session)

        # 장바구니 저장 확인
        final_cart = self.session_manager.get_cart(session_id)
        if not final_cart or len(final_cart) == 0:
            print(f"[경고] 장바구니 정보 유실, 다시 시도합니다.")
            self.session_manager.add_to_cart(session_id, cart_menu)

        # 대기열에서 다음 메뉴 가져오기 시도
        print("[옵션 선택 처리] 대기열에서 다음 메뉴 확인 중")

        # 매우 중요한 부분: 최신 세션 데이터 가져오기
        fresh_session = self.session_manager.get_session(session_id)

        # 대기열에서 현재 메뉴 제거 - 명시적으로 제거
        print("[옵션 선택 처리] 대기열에서 메뉴 제거 시도 중")
        self.session_manager.remove_from_order_queue(session_id)
        
        # 다음 메뉴 확인
        next_menu = self.session_manager.get_next_queued_menu(session_id)
        if next_menu:
            # 수량 처리 추가
            if "quantity" not in next_menu:
                next_menu["quantity"] = 1
                
            print(f"[옵션 선택 처리] 다음 메뉴 처리 시작: {next_menu.get('menu_name', '') or next_menu.get('name_kr', '') or next_menu.get('name', '')}")
            
            return self._start_menu_processing(next_menu, text, language, store_id, fresh_session)


        # 만약 원래 session에 order_queue가 있지만 fresh_session에 없는 경우 복원
        if "order_queue" in session and session["order_queue"] and (
            "order_queue" not in fresh_session or not fresh_session["order_queue"]
        ):
            print(f"[옵션 선택 처리] 대기열 복원 중: {len(session['order_queue'])}개 항목")
            fresh_session["order_queue"] = session["order_queue"]
            # 복원된 대기열 저장
            self.session_manager._save_session(session_id, fresh_session)

        # 대기열 디버깅 정보 추가
        if "order_queue" in fresh_session:
            queue_size = len(fresh_session["order_queue"]) if fresh_session["order_queue"] else 0
            print(f"[옵션 선택 처리] 대기열 크기: {queue_size}")
            if queue_size > 0:
                print(f"[옵션 선택 처리] 대기열 첫 번째 메뉴: {fresh_session['order_queue'][0].get('name_kr', '') or fresh_session['order_queue'][0].get('menu_name', '')}")
        else:
            print("[옵션 선택 처리] 대기열이 존재하지 않음")

        # 대기열에서 다음 메뉴가 없는 경우 - 장바구니 추가 완료 응답 생성
        if 'reply' in locals() and reply:
            pass  # 이미 reply가 있으면 그대로 사용
        else:
            # 기본 메시지 생성
            if language == Language.KR:
                reply = f"주문하신 메뉴가 장바구니에 담겼어요."
            elif language == Language.EN:
                reply = f"{menu.get('name')} has been added to your cart."
            elif language == Language.CN:
                reply = f"{menu.get('name')}已添加到您的购物车。"
            elif language == Language.JP:
                reply = f"{menu.get('name')}はカートに追加されました。"
            else:
                reply = f"{menu.get('name')} has been added to your cart."
        
        # 응답 반환
        return self._build_response(
            intent_data, text, language, ScreenState.MAIN, store_id, session,
            ResponseStatus.READY_TO_ADD_CART, reply=reply
        )
    
    def _start_menu_processing(self, menu_data: Dict[str, Any], text: str, language: str, store_id: int, session: Dict[str, Any]) -> Dict[str, Any]:
        """메뉴 처리 시작"""
        print(f"[메뉴 처리 시작] 메뉴: {menu_data.get('menu_name', '')}")
        
        # 세션 ID 가져오기
        session_id = session.get("id", "")

        intent_data = {
            "intent_type": IntentType.ORDER,
            "confidence": 0.9,
            "post_text": text
        }
        
        # 메뉴 이름으로 메뉴 정보 조회
        menu_name = menu_data.get("menu_name", "")
        full_menu = self.menu_service.find_menu_by_name(menu_name, store_id)
        
        if not full_menu:
            print(f"[메뉴 처리 시작] 메뉴 정보 조회 실패: {menu_name}")
            
            # 다음 메뉴가 있는지 확인
            self.session_manager.remove_from_order_queue(session_id)
            next_menu = self.session_manager.get_next_queued_menu(session_id)
            
            if next_menu:
                # 다음 메뉴 처리
                return self._start_menu_processing(next_menu, text, language, store_id, session)
            
            # 의도 데이터 구성
            intent_data = {
                "intent_type": IntentType.UNKNOWN,
                "confidence": 0.3,
                "post_text": text
            }
            
            # 응답 반환
            return self._build_response(
                intent_data, text, language, ScreenState.MAIN, store_id, session,
                ResponseStatus.UNKNOWN, reply="메뉴를 찾을 수 없습니다."
            )
        
        # 기본 수량 설정
        full_menu["quantity"] = menu_data.get("quantity", 1)
        
        # 인식된 옵션 정보 추가
        if "options" in menu_data and menu_data["options"]:
            for menu_option in menu_data["options"]:
                option_name = menu_option.get("option_name", "")
                option_value = menu_option.get("option_value", "")
                option_detail_id = menu_option.get("option_detail_id")
                
                # 옵션 매칭 시도
                matched_option = self._match_menu_option(full_menu, option_name, option_value, option_detail_id)
                if matched_option:
                    # 메뉴에 옵션 적용
                    self.option_handler.option_matcher.apply_option_to_menu(full_menu, matched_option)
        
        # 주문 메뉴 상태 확인
        menu_status = self.option_handler.determine_menu_status(full_menu)
        
        # 필수 옵션이 누락된 경우: 옵션 선택 단계로 진행
        if menu_status == ResponseStatus.MISSING_REQUIRED_OPTIONS:
            print("[메뉴 처리 시작] 필수 옵션 누락 감지")
            # 다음 필수 옵션 가져오기
            next_option = self.option_handler.get_next_required_option(full_menu)
            
            if next_option:
                # 세션에 메뉴 및 다음 옵션 정보 저장
                session["last_state"] = {
                    "menu": {
                        "menu_id": full_menu.get("id"),
                        "name":      full_menu.get("name_kr") or full_menu.get("name"),
                        "name_en":   full_menu.get("name_en"),
                        "description": full_menu.get("description"),
                        "base_price": full_menu.get("price", 0),
                        "total_price": full_menu.get("price", 0),
                        "image_url":  full_menu.get("image_url"),
                        "quantity":   full_menu.get("quantity", 1),
                        # 옵션 원본을 그대로 줘야 나중에 선택 가능
                        "options":    copy.deepcopy(full_menu.get("options", [])),
                        "selected_options": []
                    },
                    "pending_option": next_option
                }
                
                # 세션 저장
                self.session_manager._save_session(session_id, session)
                
                # 기본 메시지 생성
                if language == Language.KR:
                    reply = f"{full_menu.get('name') or full_menu.get('name_kr') or full_menu.get('menu_name')}의 필수 옵션을 선택해주세요."
                elif language == Language.EN:
                    reply = f"Selecting options for {full_menu.get('name')} is required. Please select options."
                else:
                    reply = f"{full_menu.get('name') or full_menu.get('name_kr') or full_menu.get('menu_name')}의 필수 옵션을 선택해주세요."
                
                # 응답 반환
                return self._build_response(
                    intent_data, text, language, ScreenState.ORDER, store_id, session,
                    ResponseStatus.MISSING_REQUIRED_OPTIONS, contents=[full_menu], reply=reply
                )
        
        # 장바구니에 추가 가능한 경우
        elif menu_status == ResponseStatus.READY_TO_ADD_CART:
            print("[메뉴 처리 시작] 장바구니 추가 가능")
            # 장바구니에 추가
            self.session_manager.add_to_cart(session_id, full_menu)
            
            # 현재 메뉴는 처리 완료했으니 대기열에서 명시적으로 제거
            self.session_manager.remove_from_order_queue(session_id)
            
            # 다음 메뉴가 있는지 확인
            next_menu = self.session_manager.get_next_queued_menu(session_id)
            
            if next_menu:
                print(f"[메뉴 처리 시작] 대기열에 다음 메뉴 존재: {next_menu.get('name_kr', '') or next_menu.get('menu_name', '') or next_menu.get('name', '')}")
                
                # 다음 메뉴 처리 시작
                return self._start_menu_processing(next_menu, text, language, store_id, session)
            
            # 모든 메뉴 처리 완료
            print("[메뉴 처리 시작] 모든 메뉴 처리 완료")
            
            # 기본 메시지 생성
            if language == Language.KR:
                reply = f"주문하신 메뉴가 장바구니에 담겼어요."
            elif language == Language.EN:
                reply = f"{full_menu.get('name')} has been added to your cart."
            elif language == Language.CN:
                reply = f"{full_menu.get('name')}已添加到您的购物车。"
            elif language == Language.JP:
                reply = f"{full_menu.get('name')}はカートに追加されました。"
            else:
                reply = f"{full_menu.get('name')} has been added to your cart."
            
            # 응답 반환
            return self._build_response(
                intent_data, text, language, ScreenState.MAIN, store_id, session,
                ResponseStatus.READY_TO_ADD_CART, reply=reply
            )
        
        # 기본적으로 MAIN 화면으로 돌아가도록 처리
        intent_data = {
            "intent_type": IntentType.UNKNOWN,
            "confidence": 0.5,
            "post_text": text
        }
        
        return self._build_response(
            intent_data, text, language, ScreenState.MAIN, store_id, session,
            ResponseStatus.UNKNOWN, reply="주문 처리 중 오류가 발생했습니다."
        )
    
    def _match_menu_option(self, menu: Dict[str, Any], option_name: str, option_value: str, option_detail_id: Optional[int] = None) -> Optional[Dict[str, Any]]:
        """메뉴 옵션 매칭"""
        # 옵션 리스트 확인
        if "options" not in menu or not menu["options"]:
            return None
        
        print(f"옵션 매칭 시도: 이름={option_name}, 값={option_value}")
        
        # 옵션 이름 정규화 - 공백 제거 및 소문자 변환
        normalized_option_name = option_name.lower().replace(' ', '')
        
        for option in menu["options"]:
            option_name_kr = option.get("option_name", "").lower().replace(' ', '')
            
            # 부분 일치 검사 (정확히 일치하지 않아도 됨)
            if normalized_option_name in option_name_kr or option_name_kr in normalized_option_name:
                print(f"옵션 이름 매칭 성공: {option.get('option_name')}")
                
                # 옵션 ID가 제공된 경우 직접 매칭 시도
                if option_detail_id:
                    print(f"옵션 ID 직접 매칭 시도: option_detail_id={option_detail_id}")
                    for detail in option.get("option_details", []):
                        if detail.get("id") == option_detail_id:
                            print(f"옵션 ID 매칭 성공: id={option_detail_id}, value={detail.get('value')}")
                            return {
                                "option_id": option.get("option_id"),
                                "option_name": option.get("option_name"),
                                "option_name_en": option.get("option_name_en"),
                                "required": option.get("required", False),
                                "is_selected": True,
                                "option_details": [{
                                    "id": detail.get("id"),
                                    "value": detail.get("value"),
                                    "additional_price": detail.get("additional_price", 0)
                                }]
                            }
                
                if not option_value:       
                    return None 
                # 옵션 ID가 없을 경우 텍스트 기반 매칭
                return self.option_handler.option_matcher.match_option_value(option, option_value, option_detail_id)
        
        return None
    
    def _is_cancellation_request(self, text: str, language: str) -> bool:
        """취소 요청인지 확인"""
        text_lower = text.lower()
        
        if language == Language.KR:
            cancel_keywords = ["취소", "그만", "안 할래", "안할래", "메인으로", "취소해줘"]
            return any(keyword in text_lower for keyword in cancel_keywords)
        elif language == Language.EN:
            cancel_keywords = ["cancel", "stop", "nevermind", "main menu", "forget it"]
            return any(keyword in text_lower for keyword in cancel_keywords)
        
        return False
    
    def _generate_cancellation_response(self, text: str, language: str, screen_state: str, store_id: int, session: Dict[str, Any]) -> Dict[str, Any]:
        """취소 응답 생성"""
        # 의도 데이터 구성
        intent_data = {
            "intent_type": IntentType.UNKNOWN,
            "confidence": 0.8,
            "post_text": "취소 요청"
        }
        
        # 컨텍스트 구성
        context = {
            "status": ResponseStatus.UNKNOWN,
            "screen_state": ScreenState.MAIN,
            "cancel_type": "order_cancellation"
        }
        
        # 취소 메시지 생성 (다국어 지원)
        if screen_state == ScreenState.ORDER:
            if language == Language.KR:
                reply = "주문하던 메뉴가 취소되었어요.."
            elif language == Language.EN:
                reply = "Your order has been cancelled."
            elif language == Language.CN:
                reply = "您正在订购的菜单已取消。"
            elif language == Language.JP:
                reply = "注文中のメニューがキャンセルされました。"
            else:
                reply = "Your order has been cancelled."
        else:
            if language == Language.KR:
                reply = "취소되었어요."
            elif language == Language.EN:
                reply = "Cancelled."
            elif language == Language.CN:
                reply = "已取消。"
            elif language == Language.JP:
                reply = "キャンセルされました。"
            else:
                reply = "Cancelled."
        
        # 응답 반환
        return self._build_response(
            intent_data, text, language, ScreenState.MAIN, store_id, session,
            ResponseStatus.UNKNOWN, reply=reply
        )
    
    def _check_new_order_intent(self, text: str, language: str, store_id: int) -> bool:
        """새로운 메뉴 주문 의도인지 확인"""
        # 메뉴 이름 목록 가져오기
        store_menus = self.menu_service.get_store_menus(store_id)
        menu_names = [menu["name_kr"].lower() for menu in store_menus.values()]
        
        # 별칭 추가
        aliases = self.menu_service._get_menu_aliases()
        for alias in aliases.keys():
            menu_names.append(alias.lower())
        
        # 텍스트에 메뉴 이름이 포함되어 있는지 확인
        text_lower = text.lower()
        return any(menu_name in text_lower for menu_name in menu_names)

    def _build_response(self, intent_data, text, language, screen_state, store_id, session, status, contents=None, reply=None):
        """응답 구성"""
        # 세션 ID 가져오기
        session_id = session.get("id", "")
        
        # 장바구니 정보 새로 불러오기 - 반드시 get_cart 메서드 사용
        updated_cart = []
        try:
            # 직접 장바구니 조회 API 사용 (session에 의존하지 않음)
            updated_cart = self.session_manager.get_cart(session_id)
            print(f"[응답 구성] 카트 API 조회 결과 - 항목 수: {len(updated_cart)}")
        except Exception as e:
            print(f"[응답 구성] 장바구니 조회 오류: {str(e)}")
        
        # 장바구니 항목이 없는 경우 세션의 장바구니 정보 확인 (백업)
        if not updated_cart and session and "cart" in session:
            updated_cart = session.get("cart", [])
            print(f"[응답 구성] 세션 카트 백업 사용 - 항목 수: {len(updated_cart)}")
        
        # 로그에 카트 내용 기록 (디버깅용)
        if updated_cart:
            cart_items = [f"{item.get('name')} x{item.get('quantity')}" for item in updated_cart]
            print(f"[응답 구성] 장바구니 구성: {', '.join(cart_items)}")

        # contents가 있는 경우 불필요한 정보 제거
        cleaned_contents = []
        if contents:
            for item in contents:
                # 기본 메뉴 ID와 이름 확인 (에러 방지)
                menu_id = None
                name = None
                
                if "menu_id" in item:
                    menu_id = item["menu_id"]
                elif "id" in item:
                    menu_id = item["id"]
                
                if "name" in item:
                    name = item["name"]
                elif "name_kr" in item:
                    name = item["name_kr"]
                
                # 모든 필수 필드가 있는지 확인
                if menu_id is not None and name is not None:
                    # 이미 정제된 메뉴 데이터인 경우 그대로 사용
                    if "menu_id" in item and "name" in item and "options" in item:
                        # 🔸 selected_options 가 없거나 빈 리스트면 즉석에서 만들어 준다
                        if not item.get("selected_options"):
                            item["selected_options"] = self._extract_selected_options(item)
                        cleaned_contents.append(item)
                    else:
                        # 필요한 정보만 추출
                        cleaned_item = {
                            "menu_id": menu_id,
                            "name": name,
                            "name_en": item.get("name_en"),
                            "description": item.get("description", ""),
                            "base_price": item.get("base_price", 0) if "base_price" in item else item.get("price", 0),
                            "total_price": item.get("total_price", 0) if "total_price" in item else item.get("price", 0),
                            "image_url": item.get("image_url"),
                            "quantity": item.get("quantity", 1),
                            "options": item.get("options", [])
                        }
                        
                        # selected_options가 있으면 추가
                        if "selected_options" in item:
                            cleaned_item["selected_options"] = item["selected_options"]
                        else:
                            # selected_options 생성
                            selected_options = []
                            for option in item.get("options", []):
                                if option.get("is_selected"):
                                    option_details = []
                                    for detail in option.get("option_details", []):
                                        if detail.get("id") == option.get("selected_id"):
                                            option_details.append({
                                                "id": detail.get("id"),
                                                "value": detail.get("value"),
                                                "additional_price": detail.get("additional_price", 0)
                                            })
                                    
                                    if option_details:
                                        selected_options.append({
                                            "option_id": option.get("option_id"),
                                            "option_name": option.get("option_name"),
                                            "option_name_en": option.get("option_name_en"),
                                            "required": option.get("required", False),
                                            "is_selected": True,
                                            "option_details": option_details
                                        })
                        
                            cleaned_item["selected_options"] = selected_options
                        
                        cleaned_contents.append(cleaned_item)
        
        # 콘솔에 최종 장바구니 디버깅 정보 출력
        print(f"[응답 보강] 최종 장바구니 항목 수: {len(updated_cart)}")
        
        response = {
            "intent_type": intent_data.get("intent_type", IntentType.UNKNOWN),
            "confidence": intent_data.get("confidence", 0.0),
            "search_query": intent_data.get("search_query"),
            "payment_method": intent_data.get("payment_method"),
            "raw_text": text,
            "screen_state": screen_state,
            "search_results": None,
            "data": {
                "pre_text": text,
                "post_text": text,
                "reply": reply,
                "status": status,
                "language": language,
                "session_id": session_id,
                "cart": updated_cart,  # 최신 장바구니 정보 사용
                "contents": cleaned_contents,
                "store_id": store_id
            }
        }
        
        return response

    def _generate_option_selection_message(self, menu_name, option_name, option_values, language):
        """옵션 선택 안내 메시지 생성 (다국어 지원)"""
        if language == Language.KR:
            return f"{menu_name}의 옵션을 선택해주세요."
        elif language == Language.EN:
            return f"Please select the options for your {menu_name}."
        elif language == Language.CN:
            return f"请选择您的{menu_name}的{option_name}。"
        elif language == Language.JP:
            return f"{menu_name}の{option_name}を選択してください。"
        else:
            return f"{menu_name}의 옵션을 선택해주세요."

    def _extract_selected_options(self,menu_dict: dict) -> list:
        """옵션 배열에서 is_selected=True 인 항목만 골라 selected_options 형태로 변환"""
        selected = []
        for opt in menu_dict.get("options", []):
            if not opt.get("is_selected"):
                continue
            detail = next(
                (d for d in opt["option_details"] if d["id"] == opt.get("selected_id")),
                None
            )
            if detail:
                selected.append({
                    "option_id":   opt["option_id"],
                    "option_name": opt["option_name"],
                    "option_name_en": opt.get("option_name_en"),
                    "required":    opt.get("required", False),
                    "is_selected": True,
                    "option_details": [{
                        "id": detail["id"],
                        "value": detail["value"],
                        "additional_price": detail.get("additional_price", 0)
                    }]
                })
        return selected