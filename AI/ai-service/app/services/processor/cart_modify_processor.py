from typing import Dict, Any, List, Optional
from app.models.schemas import IntentType, ScreenState, Language, ResponseStatus
from app.services.processor.base_processor import BaseProcessor
import re
uuid_pat = re.compile(
    r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}",
    re.I
)
class CartModifyProcessor(BaseProcessor):
    """장바구니 수정 처리 프로세서"""
    
    def __init__(self, response_generator, menu_service, session_manager):
        """프로세서 초기화"""
        self.response_generator = response_generator
        self.menu_service = menu_service
        self.session_manager = session_manager
    
    def process(self, intent_data: Dict[str, Any], text: str, language: str, screen_state: str, store_id: int, session: Dict[str, Any]) -> Dict[str, Any]:
        """장바구니 수정 의도 처리"""
        # LLM에서 생성한 응답 가져오기 (나중에 사용)
        llm_reply = intent_data.get("reply", "")
        
        # 장바구니 가져오기
        cart = session.get("cart", [])
        session_id = session.get("id", "")
        
        if not cart:
            # 장바구니가 비어있는 경우
            reply = llm_reply or "장바구니가 비어있어요. 먼저 메뉴를 추가해주세요."
            return self._build_response(
                intent_data, text, language, screen_state, store_id, session,
                ResponseStatus.UNKNOWN, reply=reply
            )
        
        # 액션 타입 확인 (UPDATE, REMOVE, QUANTITY)
        action_type = intent_data.get("action_type", "UNKNOWN").upper()
        menu_name = intent_data.get("menu_name", "")

        # 0. 장바구니 페이지 이동
        if action_type == "SHOW":
            reply = llm_reply or "장바구니 내역입니다."
            return self._build_response(
                intent_data, text, language, screen_state, store_id, session,
                ResponseStatus.CART_VIEWED, reply=reply,
                new_screen_state=ScreenState.CONFIRM,  
                contents=cart                           # 그대로 내려줌
            )
        
        # 1. 전체 장바구니 비우기
        if action_type == "REMOVE" and not menu_name:
            self.session_manager.clear_cart(session_id)
            reply = llm_reply or "장바구니를 비웠어요."
            return self._build_response(
                intent_data, text, language, screen_state, store_id, session,
                ResponseStatus.CART_CLEARED, reply=reply, contents=[],
                new_screen_state=ScreenState.MAIN
            )
        
        #cart id 매칭
        cart_id_in_text = None

        # 수정할 메뉴 검색
        target_item = None
        target_index = -1

        m = uuid_pat.search(text)
        if m:
            cart_id_in_text = m.group(0).lower()
            for i, item in enumerate(cart):
                if item.get("cart_id", "").lower() == cart_id_in_text:
                    target_item, target_index = item, i
                    break

        if menu_name:
            # 메뉴 이름으로 검색
            for i, item in enumerate(cart):
                if menu_name.lower() in item.get("name", "").lower():
                    target_item = item
                    target_index = i
                    break
        else:
            # 메뉴 이름이 없으면 가장 최근에 추가된 메뉴 선택
            if cart:
                target_item = cart[-1]
                target_index = len(cart) - 1
        
        if not target_item:
            reply = llm_reply or f"장바구니에서 '요청하신 메뉴를 찾을 수 없어요."
            return self._build_response(
                intent_data, text, language, screen_state, store_id, session,
                ResponseStatus.UNKNOWN, reply=reply
            )
        
        
        # 2. 특정 메뉴 삭제
        if action_type == "REMOVE":
            # 장바구니에서 메뉴 삭제
            removed_item = cart.pop(target_index)
            
            # 세션 업데이트
            session["cart"] = cart
            self.session_manager._save_session(session_id, session)
            
            reply = llm_reply or f"요청하신 메뉴를 장바구니에서 삭제했어요."

            if len(cart) < 1:
                new_screen_state=ScreenState.MAIN
            else:
                new_screen_state=ScreenState.CONFIRM

            return self._build_response(
                intent_data, text, language, screen_state, store_id, session,
                ResponseStatus.ITEM_REMOVED, reply=reply, new_screen_state = new_screen_state
            )
            
        # 4. 옵션 변경
        elif action_type == "UPDATE":
            # 1) 메뉴 컨텍스트(메타) 조회
            menu_info = self.menu_service.find_menu_by_id(target_item["menu_id"], store_id)
            if not menu_info:
                return self._build_response(
                    intent_data, text, language, screen_state, store_id, session,
                    ResponseStatus.UNKNOWN,
                    reply="메뉴 정보를 가져오지 못했습니다."
                )

            # 2) LLM이 준 옵션 목록 확보 (new_options 우선, 없으면 options)
            options_from_llm = intent_data.get("new_options") \
                            or intent_data.get("options") \
                            or []
            if not options_from_llm:
                return self._build_response(
                    intent_data, text, language, screen_state, store_id, session,
                    ResponseStatus.UNKNOWN,
                    reply=llm_reply or "변경할 옵션을 명확히 말씀해주세요."
                )

            # 3) 이름+값으로 ID 매핑 후 target_item 수정
            try:
                self._apply_new_options(menu_info, target_item, options_from_llm)
            except ValueError as err:
                # 매핑 실패 시 사용자에게 오류 메시지로 알려줌
                return self._build_response(
                    intent_data, text, language, screen_state, store_id, session,
                    ResponseStatus.UNKNOWN,
                    reply=str(err)
                )

            # 4) 세션에 저장
            cart[target_index] = target_item
            session["cart"] = cart
            saved = self.session_manager._save_session(session_id, session)
            print(f"[장바구니 수정] 옵션 변경 세션 저장 결과: {saved}")

            # 5) 응답 반환
            return self._build_response(
                intent_data, text, language, screen_state, store_id, session,
                ResponseStatus.OPTIONS_UPDATED,
                reply=llm_reply or "옵션을 변경했어요."
            )
        # elif action_type == "UPDATE":
        #     # LLM 응답에서 옵션 정보 추출
        #     menus = intent_data.get("menus", [])
        #     options_from_llm = []
            
        #     # 메뉴 배열에서 옵션 정보 추출
        #     for menu in menus:
        #         if "options" in menu:
        #             options_from_llm.extend(menu.get("options", []))
            
        #     # 직접 주어진 new_options나 options가 있으면 그것 사용
        #     if intent_data.get("new_options"):
        #         options_from_llm = intent_data.get("new_options")
        #     elif intent_data.get("options") and not options_from_llm:
        #         options_from_llm = intent_data.get("options")
            
        #     # 옵션 정보가 없는 경우
        #     if not options_from_llm:
        #         reply = llm_reply or "변경할 옵션을 명확히 말씀해주세요."
        #         return self._build_response(
        #             intent_data, text, language, screen_state, store_id, session,
        #             ResponseStatus.UNKNOWN, reply=reply
        #         )
            
        #     print(f"[장바구니 수정] 변경할 옵션 정보: {options_from_llm}")
            
        #     # 기존 옵션 가져오기
        #     selected_options = target_item.get("selected_options", [])
        #     print(f"[장바구니 수정] 현재 선택된 옵션: {selected_options}")
            
        #     # 변경된 옵션 추적
        #     updated_options = []
            
        #     for llm_option in options_from_llm:
        #         option_name  = llm_option["option_name"].lower()
        #         option_value = llm_option["option_value"].upper()

        #         # ① 삭제 요청(is_selected=False) 처리
        #         if not llm_option.get("is_selected", True):
        #             selected_options = [
        #                 o for o in selected_options
        #                 if o["option_name"].lower() != option_name
        #             ]
        #             updated_options.append(f"removed {option_name}")
        #             continue

        #         # ② 추가 요청: 기존 동일 옵션 제거
        #         selected_options = [
        #             o for o in selected_options
        #             if o["option_name"].lower() != option_name
        #         ]

        #         # ③ detail_id 우선, 없으면 get_option_detail 호출
        #         detail_id = llm_option.get("option_detail_id")
        #         if detail_id is None:
        #             detail_id, add_price = self.menu_service.get_option_detail(
        #                 option_name, option_value, store_id
        #             )
        #         else:
        #             # 추가금까지 정확히 가져오려면 helper 메서드로 조회
        #             add_price = getattr(
        #                 self.menu_service,
        #                 "get_price_by_detail_id",
        #                 lambda _id, _sid: 0
        #             )(detail_id, store_id)

        #         # ③ 새 옵션 객체 생성
        #         new_option = {
        #             "option_id": llm_option.get("option_id"),
        #             "option_name": llm_option["option_name"],
        #             "is_selected": True,
        #             "option_details": [{
        #                 "id": detail_id,
        #                 "value": option_value,
        #                 "additional_price": add_price
        #             }]
        #         }
        #         selected_options.append(new_option)
        #         # updated_options.append(option_name)
        #         updated_options.append(f"added {option_name}")

        #     # 옵션이 변경되었으면 세션 업데이트
        #     if updated_options:
        #         # 타겟 아이템 업데이트
        #         target_item["selected_options"] = selected_options
                
        #         # 2) total_price 재계산
        #         base_price = self.menu_service.get_menu_price(
        #             target_item["menu_id"], store_id
        #         )
        #         options_sum = sum(
        #             d["additional_price"]
        #             for opt in selected_options
        #             for d in opt.get("option_details", [])
        #         )
        #         new_total = (base_price + options_sum)
        #         target_item["total_price"] = new_total

        #         # 세션 업데이트
        #         cart[target_index] = target_item
        #         session["cart"] = cart
        #         result = self.session_manager._save_session(session_id, session)
        #         print(f"[장바구니 수정] 옵션 변경 세션 저장 결과: {result}, 변경된 옵션: {', '.join(updated_options)}")
                
        #         # 디버깅: 세션 저장 후 다시 확인
        #         updated_session = self.session_manager.get_session(session_id)
        #         updated_cart = updated_session.get("cart", [])
        #         if updated_cart and len(updated_cart) > target_index:
        #             print(f"[장바구니 수정] 업데이트 후 옵션: {updated_cart[target_index].get('selected_options')}")
        #     else:
        #         print("[장바구니 수정] 변경된 옵션 없음")
            
        #     # 응답 반환
        #     return self._build_response(
        #         intent_data, text, language, screen_state, store_id, session,
        #         ResponseStatus.OPTIONS_UPDATED, reply=llm_reply
        #     )

        # 3. 메뉴 수량 변경
        elif action_type == "QUANTITY":
            # 현재 수량
            current_quantity = target_item.get("quantity", 1)
            print(f"현재 수량 : {current_quantity}")
            if "quantity_change" in intent_data:
                # ± 증감값
                new_quantity = current_quantity + intent_data["quantity_change"]
            elif "new_quantity" in intent_data:
                # 절대값
                new_quantity = intent_data["new_quantity"]
            else:
                reply = llm_reply or "변경할 수량을 명확히 말씀해주세요."
                return self._build_response(
                    intent_data, text, language, screen_state, store_id, session,
                    ResponseStatus.UNKNOWN, reply=reply, new_screen_state=ScreenState.CONFIRM
                )
            
             
            if new_quantity <= 0:
                reply = "수량은 1개 이상이어야 합니다."
                return self._build_response(
                    intent_data, text, language, screen_state, store_id, session,
                    ResponseStatus.UNKNOWN, reply=reply, new_screen_state=ScreenState.CONFIRM
                )
            # 실제 업데이트
            if new_quantity == current_quantity:
                reply = llm_reply or "이미 해당 수량으로 설정되어 있어요."
            else:
                target_item["quantity"] = new_quantity
                reply = llm_reply or f"{target_item['name']}의 수량을 {new_quantity}개로 변경했어요."
            
            # 세션 업데이트
            cart[target_index] = target_item
            session["cart"] = cart
            result = self.session_manager._save_session(session_id, session)
            print(f"[장바구니 수정] 수량 변경 세션 저장 결과: {result}")
            
            return self._build_response(
                intent_data, text, language, screen_state, store_id, session,
                ResponseStatus.QUANTITY_UPDATED, reply=reply,
                new_screen_state=ScreenState.CONFIRM
            )
            
        else:
            # 알 수 없는 액션 타입
            reply = llm_reply or "장바구니 수정 요청을 이해하지 못했습니다. 다시 말씀해주세요."
            return self._build_response(
                intent_data, text, language, screen_state, store_id, session,
                ResponseStatus.UNKNOWN, reply=reply
            )
    
    def _build_response(self, intent_data: Dict[str, Any], text: str, language: str, screen_state: str, store_id: int, session: Dict[str, Any], status: str, contents: List[Dict[str, Any]] = None, reply: str = None,
                    new_screen_state: str = ScreenState.CONFIRM) -> Dict[str, Any]:
        """응답 구성 헬퍼 메서드"""
        # 세션 ID 확인
        session_id = session.get("id", "")
        
        # 최신 장바구니 정보 확인 (변경 후)
        cart = self.session_manager.get_cart(session_id)
        
        # 컨텐츠가 None이면 빈 리스트로 초기화
        if contents is None:
            contents = []
            
        return {
            "intent_type": IntentType.CART_MODIFY,
            "confidence": intent_data.get("confidence", 0.8),
            "raw_text": text,
            "screen_state": new_screen_state,
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

    def _apply_new_options(self,
                        menu_info: Dict[str, Any],
                        target_item: Dict[str, Any],
                        new_options: List[Dict[str, Any]]):
        # 기존 선택 옵션 초기화
        target_item["selected_options"] = []
        base_price = menu_info["price"]
        extras_sum = 0

        for opt in new_options:
            name = opt["option_name"].lower()
            value = opt["option_value"].lower()

            # 1) Option 메타 찾기
            opt_meta = next(
                (o for o in menu_info["options"]
                if o["option_name"].lower() == name),
                None
            )
            if not opt_meta:
                raise ValueError(f"알 수 없는 옵션명: {opt['option_name']}")

            # 2) OptionDetail 찾기
            detail = next(
                (d for d in opt_meta["option_details"]
                if d["value"].lower() == value),
                None
            )
            if not detail:
                raise ValueError(
                    f"옵션 '{opt['option_name']}'에 '{opt['option_value']}' 값이 없습니다."
                )

            # 3) 선택 옵션 추가
            target_item["selected_options"].append({
                "option_id":     opt_meta["option_id"],
                "option_name":   opt_meta["option_name"],
                "selected_id":   detail["id"],
                "option_details":[detail],
            })
            extras_sum += detail.get("additional_price", 0)

        # 4) 가격 재계산
        target_item["base_price"]  = base_price
        target_item["total_price"] = base_price + extras_sum