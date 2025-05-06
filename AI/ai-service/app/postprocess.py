# app/postprocess.py
from typing import Any, Dict, List
from .vectordb import menu_id
from .db import store_meta

# 옵션 매핑은 기본값으로만 사용하고, 실제 옵션은 DB에서 동적으로 가져옴
OPTION_KEY_MAP = {
    # 온도 옵션
    "온도": "temperature",
    "TEMPERATURE": "temperature",
    
    # 사이즈 옵션  
    "사이즈": "size",
    "SIZE": "size",
    
    # 얼음 옵션 추가
    "얼음량": "ice_amount",
    "ICE_AMOUNT": "ice_amount",
    
    # 당도 옵션 추가
    "당도": "sweetness",
    "SWEETNESS": "sweetness",
    
    # 휘핑크림 옵션
    "휘핑크림": "whipped_cream",
    "WHIPPED_CREAM": "whipped_cream",
    
    # 샷 추가 옵션
    "샷 추가": "extra_shot",
    "EXTRA_SHOT": "extra_shot",
    
    # 시럽 추가 옵션
    "시럽 추가": "extra_syrup",
    "EXTRA_SYRUP": "extra_syrup",
    
    # 우유 변경 옵션
    "우유 변경": "milk_change",
    "MILK_CHANGE": "milk_change",
}

def _get_option_key(option_name: str) -> str:
    """옵션 한글 이름을 필드 키로 변환"""
    return OPTION_KEY_MAP.get(option_name, option_name.lower().replace(" ", "_"))

def process_multiple_orders(fields: Dict[str, Any], store_id: int, language: str) -> List[Dict[str, Any]]:
    """다중 주문 처리"""
    if "orders" not in fields:
        return [fields]
    
    orders = fields.get("orders", [])
    result = []
    for order in orders:
        enriched = enrich(order, store_id, language)
        result.append(enriched)
    
    return result

def enrich(fields: Dict[str, Any], store_id: int, language: str = "kr") -> Dict[str, Any]:
    """fields를 메타데이터로 보강"""
    meta_data = store_meta(store_id)
    menu_name = fields.get("menuName", "")
    
    # 메뉴 ID 확인 - 벡터 검색으로
    mid = menu_id(menu_name, store_id, language)
    
    if not mid and menu_name:
        # 다른 언어로 다시 시도
        alternate_lang = "en" if language == "kr" else "kr"
        mid = menu_id(menu_name, store_id, alternate_lang)

    # 필수 옵션 확인
    need = []
    if not mid:
        need.append("menuName")
        return {
            **fields,
            "menuId": None,
            "need": need,
            "error": "메뉴를 찾을 수 없습니다."
        }

    # 해당 메뉴의 모든 필수 옵션 확인 - 동적으로 처리
    required_options = meta_data.get("required_options", {}).get(mid, [])
    for req_opt in required_options:
        opt_name_kr = req_opt["name_kr"]
        mapped_key = _get_option_key(opt_name_kr)
        
        # 필수 옵션이 빠졌는지 확인
        if mapped_key not in fields or fields.get(mapped_key) is None:
            need.append(mapped_key)
    
    # 언어에 맞는 필드명 설정
    name_field = "name_kr" if language == "kr" else "name_en"
    
    # 가격 가져오기
    base_price = meta_data["menus"].get(mid, {}).get("price", 0)
    
    # 옵션별 추가 요금 계산
    total_price = base_price
    
    # 메뉴 이름 (언어에 맞게)
    menu_name = meta_data["menus"].get(mid, {}).get(name_field, fields.get("menuName", ""))
    
    # 영양·재료 정보 (언어에 맞게)
    if language == "kr":
        nut = meta_data["nutrition"].get(mid, {})
        ing = meta_data["ingredients"].get(mid, [])
        tags = meta_data["tags"].get(mid, [])
    else:
        nut = meta_data["nutrition_en"].get(mid, {})
        ing = meta_data["ingredients_en"].get(mid, [])
        tags = meta_data["tags_en"].get(mid, [])

    # 기존 필드 중 옵션으로 처리할 것만 추출
    valid_option_keys = ["temperature", "size", "ice_amount", "sweetness", 
                        "whipped_cream", "extra_shot", "extra_syrup", "milk_change", "decaf"]
    options = {}
    
    for key, value in fields.items():
        if key in valid_option_keys and value is not None:
            # 옵션 표시 이름과 추가 가격 계산
            display_name = value
            additional_price = 0
            
            # 옵션 정보 가져오기
            if "option_mappings" in meta_data:
                for opt_name, mappings in meta_data["option_mappings"].items():
                    opt_key = _get_option_key(opt_name)
                    if key == opt_key:
                        for mapping in mappings:
                            if mapping.get("original") == value:
                                display_name = value  # 표시 이름은 원래 값 유지
                                additional_price = mapping.get("additional_price", 0)
                                total_price += additional_price  # 추가 가격 누적
                                break
            
            # 옵션 정보 저장
            options[key] = {
                "value": value,
                "display_name": display_name,
                "additional_price": additional_price
            }
    
    # 수량에 따른 총 가격
    quantity = fields.get("quantity", 1)
    total_price *= quantity
    
    # 결과 반환 - 필요한 필드만 포함
    result = {
        "menuId": mid,
        "menuName": menu_name,
        "base_price": base_price,
        "price": total_price,
        "quantity": quantity,
        "options": options,
        "need": need,
        "tags": tags
    }
    
    # 기타 필드 복사 (옵션 제외)
    for key, value in fields.items():
        if key not in options and key not in ["menuId", "menuName", "price", "need", "options", "tags"]:
            result[key] = value
    
    return result