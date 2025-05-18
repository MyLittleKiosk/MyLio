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
                        "option_details": [{
                            "id": matched_detail.get("id"),
                            "value": matched_detail.get("value"),
                            "additional_price": matched_detail.get("additional_price", 0)
                        }]
                    }
        
        return None
    
    def parse_option_response(self, text: str, pending_option: Dict[str, Any], menu: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """사용자 응답에서 옵션 값 파싱"""
        text = text.lower()
        option_name = pending_option.get("option_name", "").lower()
        option_details = pending_option.get("option_details", [])
        
        # Helper function to create option response
        def create_option_response(detail: Dict[str, Any]) -> Dict[str, Any]:
            return {
                "option_id": pending_option.get("option_id"),
                "option_name": pending_option.get("option_name"),
                "option_name_en": pending_option.get("option_name_en"),
                "required": pending_option.get("required", False),
                "is_selected": True,
                "option_details": [{
                    "id": detail.get("id"),
                    "value": detail.get("value"),
                    "additional_price": detail.get("additional_price", 0)
                }]
            }
        
        # 1. 사이즈 옵션 처리
        if "사이즈" in option_name or "size" in option_name:
            if any(kw in text for kw in ["small", "s", "작은", "스몰", "작게", "작은거", "작은 거","에스","톨"]):
                for detail in option_details:
                    if detail.get("value", "").lower() in ["s", "small"]:
                        return create_option_response(detail)
            
            elif any(kw in text for kw in ["medium", "m", "중간", "미디움", "보통", "중간거", "중간 거","엠","미디엄","그란데"]):
                for detail in option_details:
                    if detail.get("value", "").lower() in ["m", "medium"]:
                        return create_option_response(detail)
            
            elif any(kw in text for kw in ["large", "l", "큰", "라지", "크게", "큰거", "큰 거","엘","벤티","밴티"]):
                for detail in option_details:
                    if detail.get("value", "").lower() in ["l", "large"]:
                        return create_option_response(detail)
        
        # 2. 온도 옵션 처리
        elif "온도" in option_name or "temperature" in option_name:
            if any(kw in text for kw in ["hot", "뜨거운", "따뜻한", "따듯한", "핫", "하스로", "따뜻하게", "따뜻", "따뜻한걸로", "뜨거운걸로"]):
                for detail in option_details:
                    if detail.get("value", "").lower() == "hot":
                        return create_option_response(detail)
            
            elif any(kw in text for kw in ["ice", "차가운", "시원한", "아이스", "아이스로", "차갑게", "아이", "아아", "차가운걸로", "시원한걸로"]):
                for detail in option_details:
                    if detail.get("value", "").lower() == "ice":
                        return create_option_response(detail)
        
        # 3. 샷 추가 옵션 처리
        elif "샷" in option_name or "shot" in option_name:
            # 샷 추가 요청 키워드
            if any(kw in text for kw in ["샷", "shot", "샷추가", "샷 추가", "extra shot"]):
                # 샷 1개 추가
                if any(kw in text for kw in ["1개", "1잔", "한 개", "one", "single"]):
                    for detail in option_details:
                        if "1개" in detail.get("value", "") or "one" in detail.get("value", "").lower():
                            return create_option_response(detail)
                # 샷 2개 추가
                elif any(kw in text for kw in ["2개", "2잔", "두 개", "two", "double"]):
                    for detail in option_details:
                        if "2개" in detail.get("value", "") or "two" in detail.get("value", "").lower():
                            return create_option_response(detail)
                # 단순히 "샷 추가"만 요청한 경우 - 기본값은 1개 추가
                else:
                    for detail in option_details:
                        if "1개" in detail.get("value", ""):
                            return create_option_response(detail)
            # 샷 추가 안함 키워드
            elif any(kw in text for kw in ["추가 안해", "없이", "안함", "no shot", "no", "안 넣어"]):
                for detail in option_details:
                    if "없음" in detail.get("value", "") or "no" in detail.get("value", "").lower():
                        return create_option_response(detail)
            # 연하게 키워드
            elif any(kw in text for kw in ["연하게", "라이트", "light", "약하게"]):
                for detail in option_details:
                    if "연하게" in detail.get("value", "") or "light" in detail.get("value", "").lower():
                        return create_option_response(detail)
                        
        # 4. 얼음량 옵션 처리
        elif "얼음" in option_name or "ice" in option_name:
            if any(kw in text for kw in ["얼음 없이", "얼음 없음", "얼음 빼고", "no ice"]):
                for detail in option_details:
                    if "없음" in detail.get("value", "") or "no" in detail.get("value", "").lower():
                        return create_option_response(detail)
            elif any(kw in text for kw in ["얼음 적게", "얼음 조금", "less ice", "light ice"]):
                for detail in option_details:
                    if "적게" in detail.get("value", "") or "less" in detail.get("value", "").lower():
                        return create_option_response(detail)
            elif any(kw in text for kw in ["얼음 많이", "얼음 많게", "extra ice"]):
                for detail in option_details:
                    if "많이" in detail.get("value", "") or "extra" in detail.get("value", "").lower():
                        return create_option_response(detail)
            # 그 외에는 기본 (보통) 선택
            else:
                for detail in option_details:
                    if "보통" in detail.get("value", "") or "regular" in detail.get("value", "").lower():
                        return create_option_response(detail)
                        
        # 5. 우유 변경 옵션 처리
        elif "우유" in option_name or "milk" in option_name:
            if any(kw in text for kw in ["저지방", "저지방 우유", "low fat", "저지방우유"]):
                for detail in option_details:
                    if "저지방" in detail.get("value", "") or "low fat" in detail.get("value", "").lower():
                        return create_option_response(detail)
            elif any(kw in text for kw in ["두유", "soy", "콩", "콩우유"]):
                for detail in option_details:
                    if "두유" in detail.get("value", "") or "soy" in detail.get("value", "").lower():
                        return create_option_response(detail)
            elif any(kw in text for kw in ["오트", "오트 우유", "oat", "귀리", "귀리우유"]):
                for detail in option_details:
                    if "오트" in detail.get("value", "") or "oat" in detail.get("value", "").lower():
                        return create_option_response(detail)
            else:
                for detail in option_details:
                    if "일반" in detail.get("value", "") or "regular" in detail.get("value", "").lower():
                        return create_option_response(detail)
        
        return None
    
    def apply_option_to_menu(self, menu: Dict[str, Any], selected_option: Dict[str, Any]) -> None:
        """선택된 옵션을 메뉴 딕셔너리에 반영하고 총액을 다시 계산한다."""
        print(f"[옵션 적용] 시작: option_id={selected_option.get('option_id')}, option_name={selected_option.get('option_name')}")
        sel_id = selected_option.get("selected_id") or \
        selected_option.get("option_details", [{}])[0].get("id")

        sel_detail = next(
            (d for d in selected_option.get("option_details", []) if d.get("id") == sel_id),
            selected_option.get("option_details", [{}])[0]      # fallback
        )

        sel_value  = sel_detail.get("value")
        print(f"[옵션 적용] 선택된 값: {sel_value} (ID: {sel_id})")
        
        # 만약 option_details 길이가 1보다 크면 잘라낸다
        selected_option["option_details"] = [sel_detail]

        # 1) 옵션 마스터 목록(menu['options']) 업데이트
        for option in menu.get("options", []):
            if option.get("option_id") == selected_option.get("option_id"):
                option["is_selected"] = True
                old_id = option.get("selected_id")
                option["selected_id"] = sel_id
                # detail 테이블에도 추가요금·값 싱크 맞추기
                for d in option.get("option_details", []):
                    if d["id"] == sel_id:
                        d["additional_price"] = sel_detail.get("additional_price", 0)
                        d["value"]            = sel_value
                print(f"[옵션 적용] ID 업데이트: {old_id} -> {sel_id}")
                break  # 찾으면 종료

        # 2) menu['selected_options'] 갱신
        if "selected_options" not in menu:
            menu["selected_options"] = []

        for idx, opt in enumerate(menu["selected_options"]):
            if opt.get("option_id") == selected_option.get("option_id"):
                menu["selected_options"][idx] = selected_option
                break
        else:
            menu["selected_options"].append(selected_option)
            print(f"[옵션 적용] 새 선택 옵션 추가: {selected_option.get('option_name')}={sel_value}")

        # 3) 총액 재계산 – base_price + 모든 추가요금
        base_price = menu.get("base_price") or menu.get("price") or 0
        extra      = 0
        for opt in menu.get("selected_options", []):
            for d in opt.get("option_details", []):
                extra += d.get("additional_price", 0)
        old_total          = menu.get("total_price", base_price)
        menu["total_price"] = base_price + extra
        print(f"[옵션 적용] 가격 업데이트: {old_total} -> {menu['total_price']}")

        # 디버깅: 현재 선택된 옵션 상태
        print("[옵션 적용] 최종 메뉴 옵션 상태:")
        for option in menu.get("options", []):
            if option.get("is_selected"):
                chosen = next((d for d in option.get("option_details", []) if d["id"] == option.get("selected_id")), {})
                print(f"  - {option.get('option_name')} = {chosen.get('value')} (ID: {chosen.get('id')})")

    
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
        """메뉴의 총 가격 계산"""
        base     = menu.get("base_price", 0)
        quantity = menu.get("quantity", 1)
        extra    = 0

        for opt in menu.get("options", []):
            if not opt.get("is_selected"):
                continue
            sel_id = opt.get("selected_id")
            for d in opt.get("option_details", []):
                if d["id"] == sel_id:                # ★ 선택된 detail 만 사용
                    extra += d.get("additional_price", 0)
                    break

        return (base + extra) * quantity

    def match_option_value(self, option, option_value, option_detail_id=None):
        """옵션 값 매칭 함수 - option_detail_id가 제공되면 우선적으로 사용"""
        # 사용자가 값을 말하지 않았으면 매칭하지 않는다
        if not option_value or not option_value.strip():
            # 빈 문자열 · None · 공백뿐인 문자열 → 매칭 실패
            return None
        
        # LLM이 제공한 detail_id가 있으면 그것을 우선 사용
        if option_detail_id:
            print(f"[옵션 매처] ID 기반 매칭 시도: option_detail_id={option_detail_id}")
            for detail in option.get('option_details', []):
                if detail.get('id') == option_detail_id:
                    option_value_matched = detail.get('value', '')
                    print(f"[옵션 매처] ID 기반 매칭 성공: option_value={option_value_matched}")
                    option['is_selected'] = True
                    option['selected_id'] = detail.get('id')
                    return option
            
            # ID로 매칭 실패 시 로그 출력
            print(f"[옵션 매처] ID 기반 매칭 실패: option_detail_id={option_detail_id}, 텍스트 기반 매칭으로 전환")
        
        # 기존 텍스트 기반 매칭 로직
        print(f"[옵션 매처] 텍스트 기반 매칭 시도: option_value={option_value}")
        for detail in option.get('option_details', []):
            normalized_value = option_value.lower().replace(" ", "")
            normalized_detail_value = detail.get('value', '').lower().replace(" ", "")
            
            if (normalized_value == normalized_detail_value or 
                normalized_value in normalized_detail_value or 
                normalized_detail_value in normalized_value):
                
                print(f"[옵션 매처] 텍스트 기반 매칭 성공: detail_value={detail.get('value')}")
                option['is_selected'] = True
                option['selected_id'] = detail.get('id')
                return option
        
        print(f"[옵션 매처] 모든 매칭 실패: option_name={option.get('option_name')}, option_value={option_value}")
        return None