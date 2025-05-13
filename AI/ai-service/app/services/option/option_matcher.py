# app/services/option/option_matcher.py
from typing import Dict, Any, Optional, List
from app.models.schemas import ResponseStatus 

class OptionMatcher:
    """옵션 매칭 로직"""
    
    def match_option(self, options: List[Dict[str, Any]], option_name: str, option_value: str) -> Optional[Dict[str, Any]]:
        """옵션 매핑 함수"""
        # 입력 검증 추가
        if not options or not option_name or not option_value:
            print(f"[옵션 매칭] 유효하지 않은 입력: options={bool(options)}, name={bool(option_name)}, value={bool(option_value)}")
            return None
        
        # 디버깅을 위한 로그 추가
        print(f"옵션 매핑: 이름={option_name}, 값={option_value}, 사용 가능한 옵션={options}")
        
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
    
    def parse_option_response(self, text: str, pending_option: Dict[str, Any], menu: Dict[str, Any]) -> Optional[Dict[str, Any]]:
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
    
    def apply_option_to_menu(self, menu: Dict[str, Any], selected_option: Dict[str, Any]) -> None:
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
        menu["total_price"] = self.calculate_total_price(menu)
    
    def get_next_required_option(self, menu: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """다음 필수 옵션 가져오기"""
        for option in menu.get("options", []):
            if option.get("required", False) and not option.get("is_selected", False):
                return option
        return None
    
    def determine_menu_status(self, menu: Dict[str, Any]) -> ResponseStatus:
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
    
    def calculate_total_price(self, menu: Dict[str, Any]) -> int:
        """메뉴의 총 가격 계산 (옵션 포함)"""
        base_price = menu.get("base_price", 0)
        quantity = menu.get("quantity", 1)
        
        # 선택된 옵션의 추가 가격 계산
        additional_price = 0
        for option in menu.get("selected_options", []):
            option_details = option.get("option_details", [])
            if option_details:
                additional_price += option_details[0].get("additional_price", 0)
        
        # (기본 가격 + 추가 가격) * 수량
        return (base_price + additional_price) * quantity