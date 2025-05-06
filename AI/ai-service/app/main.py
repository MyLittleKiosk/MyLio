# app/main.py
import logging
from fastapi import FastAPI, HTTPException
from typing import List, Dict, Any, Optional
from .schema import ParseReq, KioskResponse, ConversationState, CartItem, CurrentOrder, Option, OptionDetail
from .db import store_meta
from .model import llm_parse
from .postprocess import enrich, process_multiple_orders
from .vectordb import search_menu
from .response_generator import ResponseGenerator

app = FastAPI(title="Kiosk AI")
log = logging.getLogger("kiosk-api")

def is_multiple_order(utterance: str) -> bool:
    """다중 주문 감지"""
    keywords = ['하나', '한 잔', '한개', '1개', '2개', '두 개', '두잔', '세 개', '세잔']
    count = sum(utterance.count(keyword) for keyword in keywords)
    conjunction_words = ['랑', '이랑', '하고', '그리고', ',', 'and', '&', 'また', '和']
    has_conjunction = any(word in utterance for word in conjunction_words)
    
    # 메뉴 이름이 2개 이상 포함되어 있는지 확인
    common_menu_words = ['아메리카노', '라떼', '카페', '스무디', '에이드', '차', '커피', 
                        'americano', 'latte', 'coffee', 'smoothie', 'ade', 'tea']
    menu_count = sum(utterance.count(menu) for menu in common_menu_words)
    
    return (count > 1 or has_conjunction or menu_count > 1)

def merge_cart_items(cart: List[CartItem], new_item: CartItem) -> List[CartItem]:
    """장바구니 아이템 병합 또는 추가"""
    for existing_item in cart:
        if existing_item.has_same_options(new_item):
            existing_item.quantity += new_item.quantity
            return cart
    cart.append(new_item)
    return cart

def get_option_display_name(option_key: str, option_value: str, store_meta_data: Dict, language: str) -> str:
    """옵션의 표시 이름 가져오기"""
    if not store_meta_data or "option_mappings" not in store_meta_data:
        return option_value
    
    # 옵션 키를 한글 이름으로 변환
    key_to_kr = {
        "temperature": "온도",
        "size": "사이즈",
        "ice_amount": "얼음량",
        "sweetness": "당도",
        "whipped_cream": "휘핑크림",
        "extra_shot": "샷 추가",
        "extra_syrup": "시럽 추가",
        "milk_change": "우유 변경"
    }
    
    option_name_kr = key_to_kr.get(option_key, option_key)
    mappings = store_meta_data["option_mappings"].get(option_name_kr, [])
    
    for mapping in mappings:
        if mapping.get("original") == option_value:
            display_key = "display_kr" if language == "kr" else "display_en"
            return mapping.get(display_key, option_value)
    
    return option_value

def get_option_additional_price(option_key: str, option_value: str, store_meta_data: Dict) -> int:
    """옵션의 추가 가격 가져오기"""
    if not store_meta_data or "option_mappings" not in store_meta_data:
        return 0
    
    # 옵션 키를 한글 이름으로 변환
    key_to_kr = {
        "temperature": "온도",
        "size": "사이즈",
        "ice_amount": "얼음량",
        "sweetness": "당도",
        "whipped_cream": "휘핑크림",
        "extra_shot": "샷 추가",
        "extra_syrup": "시럽 추가",
        "milk_change": "우유 변경"
    }
    
    option_name_kr = key_to_kr.get(option_key, option_key)
    mappings = store_meta_data["option_mappings"].get(option_name_kr, [])
    
    for mapping in mappings:
        if mapping.get("original") == option_value:
            return mapping.get("additional_price", 0)
    
    return 0

def create_current_order(menu_id: Optional[int], menu_name: str, base_price: int, 
                        fields: Dict[str, Any], need: List[str], 
                        store_meta_data: Dict, language: str) -> CurrentOrder:
    """현재 주문 객체 생성"""
    # 필수 옵션 정보 가져오기
    required_options = []
    if store_meta_data and "required_options" in store_meta_data and menu_id:
        menu_options = store_meta_data["required_options"].get(menu_id, [])
        
        # 중복 제거
        seen_option_ids = set()
        unique_menu_options = []
        for opt in menu_options:
            option_id = opt.get("id", 0)
            if option_id not in seen_option_ids:
                seen_option_ids.add(option_id)
                unique_menu_options.append(opt)

        for opt in unique_menu_options:
            option_id = opt.get("id", 0)
            option_name = opt.get("name_kr" if language == "kr" else "name_en", "Unknown")
            
            option_details = []
            # 옵션 매핑 키 확인 (option_mappings 또는 options_mappings)
            mapping_key = "option_mappings"
            if mapping_key not in store_meta_data and "options_mappings" in store_meta_data:
                mapping_key = "options_mappings"
            
            option_kr_name = opt.get("name_kr", "")
            
            # 옵션 상세 정보 찾기
            if mapping_key in store_meta_data and option_kr_name in store_meta_data[mapping_key]:
                for detail in store_meta_data[mapping_key][option_kr_name]:
                    display_name = detail.get("display_kr" if language == "kr" else "display_en", 
                                           detail.get("original", ""))
                    option_details.append(
                        OptionDetail(
                            id=detail.get("id", 0),
                            value=detail.get("original", ""),
                            display_name=display_name,
                            additional_price=detail.get("additional_price", 0)
                        )
                    )
                
            # if "options" in store_meta_data:
            #     # 옵션 상세 정보 추가
            #     option_kr_name = opt.get("name_kr", "")
                
            #     if option_kr_name in store_meta_data.get("option_mappings", {}):
            #         for detail in store_meta_data["option_mappings"][option_kr_name]:
            #             display_name = detail.get("display_kr" if language == "kr" else "display_en", 
            #                                    detail.get("original", ""))
            #             option_details.append(
            #                 OptionDetail(
            #                     id=detail.get("id", 0),
            #                     value=detail.get("original", ""),
            #                     display_name=display_name,
            #                     additional_price=detail.get("additional_price", 0)
            #                 )
            #             )
            
            required_options.append(
                Option(
                    id=option_id,
                    name=option_name,
                    required=True,
                    details=option_details
                )
            )
    
    # 현재 주문 객체 생성
    current_order = CurrentOrder(
        menu_id=menu_id,
        menu_name=menu_name,
        base_price=base_price,
        quantity=fields.get("quantity", 1),
        options={},
        required_options=required_options,
        missing_options=need
    )
    
    # 이미 선택된 옵션 추가
    for key, value in fields.items():
        if key not in ["menuName", "quantity", "menuId"] and value is not None:
            display_name = get_option_display_name(key, value, store_meta_data, language)
            additional_price = get_option_additional_price(key, value, store_meta_data)
            
            current_order.options[key] = {
                "value": value,
                "display_name": display_name,
                "additional_price": additional_price
            }
    
    # 총 가격 계산 (기본 가격 + 옵션 추가 가격)
    total_price = base_price
    for option_info in current_order.options.values():
        total_price += option_info.get("additional_price", 0)
    total_price *= current_order.quantity
    
    current_order.total_price = total_price
    
    return current_order

def update_current_order(current_order: CurrentOrder, fields: Dict[str, Any], 
                        store_meta_data: Dict, language: str) -> CurrentOrder:
    """현재 주문 객체 업데이트"""
    # 새 옵션 추가/업데이트
    for key, value in fields.items():
        if key not in ["menuName", "quantity", "menuId"] and value is not None:
            display_name = get_option_display_name(key, value, store_meta_data, language)
            additional_price = get_option_additional_price(key, value, store_meta_data)
            
            current_order.options[key] = {
                "value": value,
                "display_name": display_name,
                "additional_price": additional_price
            }
    
    # 총 가격 다시 계산
    total_price = current_order.base_price
    for option_info in current_order.options.values():
        total_price += option_info.get("additional_price", 0)
    total_price *= current_order.quantity
    
    current_order.total_price = total_price
    
    return current_order

@app.post("/parse", response_model=KioskResponse)
def parse(req: ParseReq):
    try:
        context = req.context
        response_gen = ResponseGenerator(context.language)
        
        # 1. 매장 메타데이터 로드
        store_meta_data = store_meta(context.store_id)
        
        # 2. LLM 파싱 (매장별 옵션 매핑 사용)
        if context.state == ConversationState.MAIN and is_multiple_order(req.utterance):
            # 다중 주문 감지 - LLM에게 다중 주문으로 처리하도록 요청
            fields = llm_parse(req.utterance, store_meta_data.get("option_mappings", {}), context.language)
            
            # orders 필드가 있으면 다중 주문
            if "orders" in fields:
                multiple_orders = process_multiple_orders(fields, context.store_id, context.language)
                if multiple_orders and len(multiple_orders) > 0:
                    # 첫 번째 주문 시작
                    first_order = multiple_orders[0]
                    context.multiple_orders = multiple_orders[1:]  # 나머지 주문들 저장
                    fields = first_order
                else:
                    # 단일 주문으로 처리
                    fields = llm_parse(req.utterance, store_meta_data.get("option_mappings", {}), context.language)
            else:
                # 단일 주문으로 처리
                fields = llm_parse(req.utterance, store_meta_data.get("option_mappings", {}), context.language)
        else:
            # 단일 주문 처리
            fields = llm_parse(req.utterance, store_meta_data.get("option_mappings", {}), context.language)
        
        # 3. 메뉴 ID 확인 및 필수 옵션 체크
        enriched = enrich(fields, context.store_id, context.language)
        need = enriched.get("need", [])
        
        # 4. 상태별 처리
        
        # MAIN 상태 - 메뉴 선택 또는 검색
        if context.state == ConversationState.MAIN:
            if enriched.get("menuId"):
                # 메뉴 찾음 -> 주문 진행
                # 현재 주문 객체 생성
                current_order = create_current_order(
                    menu_id=enriched.get("menuId"),
                    menu_name=enriched.get("menuName", ""),
                    base_price=enriched.get("price", 0),
                    fields=fields,
                    need=need,
                    store_meta_data=store_meta_data,
                    language=context.language
                )
                
                context.current_order = current_order
                
                # 다중 주문 처리 중인지 확인
                multiple_orders_info = None
                if getattr(context, 'multiple_orders', None):
                    multiple_orders_info = {
                        "current_index": 1,
                        "remaining": len(context.multiple_orders)
                    }
                
                # 응답 생성
                if need:
                    # 아직 필요한 옵션이 있음
                    option_suggestions = []
                    if need[0] in ["temperature", "size", "ice_amount", "sweetness", "whipped_cream", 
                                  "extra_shot", "extra_syrup", "milk_change"]:
                        # 옵션 선택지 제안
                        option_key = need[0]
                        option_name = response_gen._translate_option_name(option_key)
                        
                        # 옵션 선택지 가져오기
                        option_suggestions = response_gen._get_option_suggestions(option_key, store_meta_data)
                        
                        # 메시지 생성
                        values_text = ", ".join(option_suggestions) if option_suggestions else ""
                        if values_text:
                            message = response_gen._get_text(
                                "ask_option_with_values", 
                                menu=current_order.menu_name,
                                option=option_name,
                                values=values_text
                            )
                        else:
                            message = response_gen._get_text(
                                "ask_option", 
                                menu=current_order.menu_name,
                                option=option_name
                            )
                    else:
                        # 기타 옵션
                        option_name = response_gen._translate_option_name(need[0])
                        message = response_gen._get_text(
                            "ask_option", 
                            menu=current_order.menu_name,
                            option=option_name
                        )
                    
                    return KioskResponse(
                        text=message,
                        next_state=ConversationState.ORDER,
                        cart=context.cart,
                        current_order=current_order,
                        suggestions=option_suggestions,
                        actions={"show_options": True, "option_key": need[0]},
                        store_meta=store_meta_data if req.return_full_meta else None
                    )
                else:
                    # 모든 필수 옵션이 이미 선택됨 -> 장바구니에 바로 추가
                    cart_item = CartItem(
                        menuId=current_order.menu_id,
                        menuName=current_order.menu_name,
                        quantity=current_order.quantity,
                        price=current_order.total_price,
                        options=current_order.options,
                        need=[],
                        temperature=fields.get("temperature"),
                        size=fields.get("size"),
                        decaf=fields.get("decaf", False)
                    )
                    
                    context.cart = merge_cart_items(context.cart, cart_item)
                    context.current_order = None
                    
                    return KioskResponse(
                        text=response_gen._get_text("added_to_cart", item=cart_item.menuName),
                        next_state=ConversationState.MAIN,
                        cart=context.cart,
                        suggestions=response_gen._get_main_suggestions(),
                        actions={"add_to_cart": True, "item_added": cart_item.dict()},
                        store_meta=store_meta_data if req.return_full_meta else None
                    )
            else:
                # 메뉴 못 찾음 -> 검색
                search_results = search_menu(req.utterance, context.store_id, n_results=3)
                
                suggestions = []
                if search_results:
                    suggestions = [result["menuName"] for result in search_results]
                else:
                    suggestions = response_gen._get_search_suggestions()
                
                return KioskResponse(
                    text=response_gen._get_text("search_not_found", keyword=req.utterance),
                    next_state=ConversationState.SEARCH,
                    cart=context.cart,
                    suggestions=suggestions,
                    search_results=search_results,
                    actions={"show_search": True},
                    store_meta=store_meta_data if req.return_full_meta else None
                )
        
        # SEARCH 상태 - 검색 결과 선택
        elif context.state == ConversationState.SEARCH:
            # 검색 중 메뉴 선택
            if enriched.get("menuId"):
                # 현재 주문 객체 생성
                current_order = create_current_order(
                    menu_id=enriched.get("menuId"),
                    menu_name=enriched.get("menuName", ""),
                    base_price=enriched.get("price", 0),
                    fields=fields,
                    need=need,
                    store_meta_data=store_meta_data,
                    language=context.language
                )
                
                context.current_order = current_order
                
                if need:
                    # 아직 필요한 옵션이 있음
                    option_suggestions = []
                    if need[0] in ["temperature", "size", "ice_amount", "sweetness", "whipped_cream", 
                                  "extra_shot", "extra_syrup", "milk_change"]:
                        # 옵션 선택지 제안
                        option_key = need[0]
                        option_name = response_gen._translate_option_name(option_key)
                        
                        # 옵션 선택지 가져오기
                        option_suggestions = response_gen._get_option_suggestions(option_key, store_meta_data)
                        
                        # 메시지 생성
                        values_text = ", ".join(option_suggestions) if option_suggestions else ""
                        if values_text:
                            message = response_gen._get_text(
                                "ask_option_with_values", 
                                menu=current_order.menu_name,
                                option=option_name,
                                values=values_text
                            )
                        else:
                            message = response_gen._get_text(
                                "ask_option", 
                                menu=current_order.menu_name,
                                option=option_name
                            )
                    else:
                        # 기타 옵션
                        option_name = response_gen._translate_option_name(need[0])
                        message = response_gen._get_text(
                            "ask_option", 
                            menu=current_order.menu_name,
                            option=option_name
                        )
                    
                    return KioskResponse(
                        text=message,
                        next_state=ConversationState.ORDER,
                        cart=context.cart,
                        current_order=current_order,
                        suggestions=option_suggestions,
                        actions={"show_options": True, "option_key": need[0]}
                    )
                else:
                    # 모든 필수 옵션이 이미 선택됨 -> 장바구니에 바로 추가
                    cart_item = CartItem(
                        menuId=current_order.menu_id,
                        menuName=current_order.menu_name,
                        quantity=current_order.quantity,
                        price=current_order.total_price,
                        options=current_order.options,
                        need=[],
                        temperature=fields.get("temperature"),
                        size=fields.get("size"),
                        decaf=fields.get("decaf", False)
                    )
                    
                    context.cart = merge_cart_items(context.cart, cart_item)
                    context.current_order = None
                    
                    return KioskResponse(
                        text=response_gen._get_text("added_to_cart", item=cart_item.menu_name),
                        next_state=ConversationState.MAIN,
                        cart=context.cart,
                        suggestions=response_gen._get_main_suggestions(),
                        actions={"add_to_cart": True, "item_added": cart_item.dict()}
                    )
            else:
                # 여전히 못 찾음
                return KioskResponse(
                    text=response_gen._get_text("try_again"),
                    next_state=ConversationState.MAIN,
                    cart=context.cart,
                    suggestions=response_gen._get_main_suggestions(),
                    actions={}
                )
        
        # ORDER 상태 - 옵션 선택
        elif context.state == ConversationState.ORDER:
            if context.current_order:
                # 현재 주문 업데이트
                current_order = update_current_order(
                    current_order=context.current_order,
                    fields=fields,
                    store_meta_data=store_meta_data,
                    language=context.language
                )
                
                # 필수 옵션 다시 체크
                current_order_dict = {
                    "menuId": current_order.menu_id,
                    "menuName": current_order.menu_name,
                    "price": current_order.base_price,
                    "quantity": current_order.quantity
                }
                
                # 옵션 값 추가
                for key, value in current_order.options.items():
                    current_order_dict[key] = value.get("value")
                
                updated_enriched = enrich(current_order_dict, context.store_id, context.language)
                need = updated_enriched.get("need", [])
                
                # 현재 주문 업데이트
                current_order.missing_options = need
                context.current_order = current_order
                
                # 다중 주문 처리 정보
                multiple_orders_info = None
                if getattr(context, 'multiple_orders', None):
                    multiple_orders_info = {
                        "current_index": 1,
                        "remaining": len(context.multiple_orders)
                    }
                
                if not need:
                    # 주문 완료 -> 장바구니에 추가
                    # 옵션 정보 추출
                    temperature = None
                    size = None
                    decaf = False
                    
                    for key, value in current_order.options.items():
                        if key == "temperature":
                            temperature = value.get("value")
                        elif key == "size":
                            size = value.get("value")
                        elif key == "decaf":
                            decaf = value.get("value", False)
                    
                    cart_item = CartItem(
                        menuId=current_order.menu_id,
                        menuName=current_order.menu_name,
                        quantity=current_order.quantity,
                        price=current_order.total_price,
                        options=current_order.options,
                        need=[],
                        temperature=temperature,
                        size=size,
                        decaf=decaf
                    )
                    
                    context.cart = merge_cart_items(context.cart, cart_item)
                    
                    # 다중 주문 처리 중이면 다음 주문으로
                    if getattr(context, 'multiple_orders', None):
                        next_order = context.multiple_orders.pop(0)
                        next_enriched = enrich(next_order, context.store_id, context.language)
                        
                        # 다음 주문의 현재 주문 객체 생성
                        context.current_order = create_current_order(
                            menu_id=next_enriched.get("menuId"),
                            menu_name=next_enriched.get("menuName", ""),
                            base_price=next_enriched.get("price", 0),
                            fields=next_order,
                            need=next_enriched.get("need", []),
                            store_meta_data=store_meta_data,
                            language=context.language
                        )
                        
                        need = context.current_order.missing_options
                        
                        # 다중 주문 정보 업데이트
                        multiple_orders_info = {
                            "current_index": 2,  # 두 번째 주문
                            "remaining": len(context.multiple_orders)
                        }
                        
                        if need:
                            # 다음 주문에 필요한 옵션이 있음
                            option_key = need[0]
                            option_name = response_gen._translate_option_name(option_key)
                            option_suggestions = response_gen._get_option_suggestions(option_key, store_meta_data)
                            
                            # 메시지 생성
                            values_text = ", ".join(option_suggestions) if option_suggestions else ""
                            if values_text:
                                message = response_gen._get_text(
                                    "multiple_orders_processing",
                                    current_order_index=2,
                                    remaining=len(context.multiple_orders)
                                ) + " " + response_gen._get_text(
                                    "ask_option_with_values", 
                                    menu=context.current_order.menu_name,
                                    option=option_name,
                                    values=values_text
                                )
                            else:
                                message = response_gen._get_text(
                                    "multiple_orders_processing",
                                    current_order_index=2,
                                    remaining=len(context.multiple_orders)
                                ) + " " + response_gen._get_text(
                                    "ask_option", 
                                    menu=context.current_order.menu_name,
                                    option=option_name
                                )
                            
                            return KioskResponse(
                                text=message,
                                next_state=ConversationState.ORDER,
                                cart=context.cart,
                                current_order=context.current_order,
                                suggestions=option_suggestions,
                                actions={
                                    "show_options": True, 
                                    "option_key": need[0],
                                    "add_to_cart": True,
                                    "item_added": cart_item.dict(),
                                    "multiple_orders": True,
                                    "current_order_index": 2,
                                    "remaining_orders": len(context.multiple_orders)
                                }
                            )
                        else:
                            # 다음 주문도 바로 장바구니에 추가
                            next_cart_item = CartItem(
                                menuId=context.current_order.menu_id,
                                menuName=context.current_order.menu_name,
                                quantity=context.current_order.quantity,
                                price=context.current_order.total_price,
                                options=context.current_order.options,
                                need=[],
                                temperature=next_order.get("temperature"),
                                size=next_order.get("size"),
                                decaf=next_order.get("decaf", False)
                            )
                            
                            context.cart = merge_cart_items(context.cart, next_cart_item)
                            context.current_order = None
                            
                            return KioskResponse(
                                text=response_gen._get_text("added_to_cart", item=next_cart_item.menu_name),
                                next_state=ConversationState.MAIN,
                                cart=context.cart,
                                suggestions=response_gen._get_main_suggestions(),
                                actions={
                                    "add_to_cart": True, 
                                    "items_added": [cart_item.dict(), next_cart_item.dict()]
                                }
                            )
                    else:
                        # 단일 주문 완료
                        context.current_order = None
                        
                        return KioskResponse(
                            text=response_gen._get_text("added_to_cart", item=cart_item.menu_name),
                            next_state=ConversationState.MAIN,
                            cart=context.cart,
                            suggestions=response_gen._get_main_suggestions(),
                            actions={"add_to_cart": True, "item_added": cart_item.dict()}
                        )
                else:
                    # 아직 선택해야 할 옵션이 있음
                    option_key = need[0]
                    option_name = response_gen._translate_option_name(option_key)
                    option_suggestions = response_gen._get_option_suggestions(option_key, store_meta_data)
                    
                    # 메시지 생성
                    values_text = ", ".join(option_suggestions) if option_suggestions else ""
                    if values_text:
                        message = response_gen._get_text(
                            "ask_option_with_values", 
                            menu=current_order.menu_name,
                            option=option_name,
                            values=values_text
                        )
                    else:
                        message = response_gen._get_text(
                            "ask_option", 
                            menu=current_order.menu_name,
                            option=option_name
                        )
                    
                    return KioskResponse(
                        text=message,
                        next_state=ConversationState.ORDER,
                        cart=context.cart,
                        current_order=current_order,
                        suggestions=option_suggestions,
                        actions={"show_options": True, "option_key": option_key}
                    )
            else:
                # current_order가 없으면 메인으로
                return KioskResponse(
                    text=response_gen._get_text("default_error"),
                    next_state=ConversationState.MAIN,
                    cart=context.cart,
                    suggestions=response_gen._get_main_suggestions(),
                    actions={}
                )
        
        # CART 상태 - 장바구니 확인
        elif context.state == ConversationState.CART:
            if not context.cart:
                return KioskResponse(
                    text=response_gen._get_text("empty_cart"),
                    next_state=ConversationState.MAIN,
                    cart=context.cart,
                    suggestions=response_gen._get_main_suggestions()[:1],  # "메뉴 보기"만
                    actions={"show_menu": True}
                )
            else:
                # 장바구니 총액 계산
                total_price = sum(item.price for item in context.cart)
                
                # 언어별 확인 버튼
                confirm_suggestions = {
                    "kr": ["주문하기", "계속 쇼핑"],
                    "en": ["Order", "Continue Shopping"],
                    "ja": ["注文する", "ショッピングを続ける"],
                    "cn": ["下单", "继续购物"]
                }.get(context.language, ["Order", "Continue Shopping"])
                
                return KioskResponse(
                    text=response_gen._get_text("cart_summary", total=total_price),
                    next_state=ConversationState.CONFIRM,
                    cart=context.cart,
                    suggestions=confirm_suggestions,
                    actions={"show_cart": True, "cart_total": total_price}
                )
        
        # CONFIRM 상태 - 주문 확인
        elif context.state == ConversationState.CONFIRM:
            # 언어별 확인 버튼
            payment_suggestions = {
                "kr": ["결제하기", "수정하기"],
                "en": ["Pay", "Modify"],
                "ja": ["支払う", "修正する"],
                "cn": ["付款", "修改"]
            }.get(context.language, ["Pay", "Modify"])
            
            # 장바구니 상세 정보 준비
            cart_details = []
            for item in context.cart:
                # 옵션 정보 문자열 생성
                options_text = ""
                for key, option in item.options.items():
                    option_name = response_gen._translate_option_name(key)
                    options_text += f"{option_name}: {option.get('display_name', '')}, "
                
                # 장바구니 아이템 상세
                cart_details.append({
                    "menu_name": item.menu_name,
                    "quantity": item.quantity,
                    "price": item.price,
                    "options": options_text.strip(", ")
                })
            
            return KioskResponse(
                text=response_gen._get_text("confirm_order"),
                next_state=ConversationState.PAYMENT,
                cart=context.cart,
                suggestions=payment_suggestions,
                actions={"show_order_summary": True, "cart_details": cart_details}
            )
        
        # PAYMENT 상태 - 결제 처리
        elif context.state == ConversationState.PAYMENT:
            # 결제 방법 확인
            payment_method = None
            payment_keywords = {
                "kr": {"카드": "CARD", "현금": "CASH", "포인트": "POINTS", "모바일": "MOBILE"},
                "en": {"card": "CARD", "cash": "CASH", "points": "POINTS", "mobile": "MOBILE"},
                "ja": {"カード": "CARD", "現金": "CASH", "ポイント": "POINTS", "モバイル": "MOBILE"},
                "cn": {"卡": "CARD", "现金": "CASH", "积分": "POINTS", "移动支付": "MOBILE"}
            }
            
            # 언어에 맞는 결제 키워드 선택
            lang_keywords = payment_keywords.get(context.language, payment_keywords["en"])
            
            # 입력에서 결제 방법 확인
            for keyword, method in lang_keywords.items():
                if keyword.lower() in req.utterance.lower():
                    payment_method = method
                    break
            
            if payment_method:
                # 결제 완료 - 장바구니 비우기
                completed_cart = context.cart.copy()
                context.cart = []
                
                # 결제 영수증 정보 준비
                receipt = {
                    "payment_method": payment_method,
                    "items": [item.dict() for item in completed_cart],
                    "total": sum(item.price for item in completed_cart),
                    "timestamp": "현재 시간",  # 실제로는 datetime.now().isoformat() 같은 형식 사용
                    "order_number": "A-123"  # 실제로는 주문 번호 생성 로직 필요
                }
                
                # 결제 완료 응답
                return KioskResponse(
                    text=response_gen._get_text("order_complete"),
                    next_state=ConversationState.MAIN,
                    cart=[],  # 빈 장바구니
                    suggestions=response_gen._get_main_suggestions(),
                    actions={
                        "payment_complete": True, 
                        "payment_method": payment_method, 
                        "completed_cart": [item.dict() for item in completed_cart],
                        "receipt": receipt
                    }
                )
            else:
                # 결제 방법 선택 대기
                # 언어별 결제 수단
                payment_methods = {
                    "kr": ["카드", "현금", "취소"],
                    "en": ["Card", "Cash", "Cancel"],
                    "ja": ["カード", "現金", "キャンセル"],
                    "cn": ["卡", "现金", "取消"]
                }.get(context.language, ["Card", "Cash", "Cancel"])
                
                return KioskResponse(
                    text=response_gen._get_text("payment_options"),
                    next_state=ConversationState.PAYMENT,
                    cart=context.cart,
                    suggestions=payment_methods,
                    actions={"show_payment_methods": True}
                )
        
        # 기본 상태 처리
        return KioskResponse(
            text=response_gen._get_text("default_error"),
            next_state=ConversationState.MAIN,
            cart=context.cart,
            suggestions=response_gen._get_main_suggestions(),
            actions={}
        )
        
    except Exception as e:
        log.exception(f"파싱 실패: {str(e)}")
        return KioskResponse(
            text=response_gen._get_text("error"),
            next_state=ConversationState.MAIN,
            cart=context.cart if hasattr(context, 'cart') else [],
            suggestions=response_gen._get_main_suggestions() if 'response_gen' in locals() else [],
            actions={"error": str(e)}
        )

# 헬스체크 엔드포인트
@app.get("/health")
def health_check():
    """헬스체크"""
    return {"status": "healthy"}

# 매장 메타데이터 엔드포인트
@app.get("/store/{store_id}/meta")
def get_store_metadata(store_id: int):
    """매장 메타데이터 조회"""
    try:
        meta = store_meta(store_id)
        return {"status": "success", "data": meta}
    except Exception as e:
        log.exception(f"매장 메타데이터 조회 실패: {store_id}")
        raise HTTPException(500, f"메타데이터 조회 실패: {str(e)}")