"""
intent_recognition.py
의도 인식 서비스
"""

from typing import Dict, Any, List
import datetime  # datetime 모듈 추가
from app.models.schemas import IntentType
from app.services.rag_service import RAGService

class IntentRecognitionService:
    def __init__(self, rag_service: RAGService):
        self.rag_service = rag_service
    
    def recognize_intent(self, text: str, language: str, screen_state: str, store_id: int) -> Dict[str, Any]:
        """사용자 음성 입력에서 의도 인식"""
        # RAG 서비스를 통한 의도 인식
        rag_result = self.rag_service.recognize_intent(text, language, screen_state)
        
        # 의도별 추가 처리
        intent_type = rag_result.get("intent_type", "UNKNOWN")
        
        if intent_type == "ORDER":
            return self._process_order_intent(rag_result, store_id)
        elif intent_type == "SEARCH":
            # 검색 구현은 나중에
            return {
                "intent_type": "SEARCH",  # 필수 필드 추가
                "raw_text": text,         # 필수 필드 추가
                "screen_state": screen_state,  # 필수 필드 추가
                "success": True,
                "data": {
                    "pre_text": text,
                    "post_text": text,
                    "reply": "메뉴 검색 기능은 아직 개발 중입니다.",
                    "status": "SEARCH",
                    "language": language,
                    "store_id": store_id
                },
                "error": None,
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        elif intent_type == "PAYMENT":
            # 결제 구현은 나중에
            return {
                "intent_type": "PAYMENT",  # 필수 필드 추가
                "raw_text": text,          # 필수 필드 추가
                "screen_state": screen_state,  # 필수 필드 추가
                "success": True,
                "data": {
                    "pre_text": text,
                    "post_text": text,
                    "reply": "결제 기능은 아직 개발 중입니다.",
                    "status": "PAYMENT",
                    "language": language,
                    "store_id": store_id
                },
                "error": None,
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        else:
            return {
                "intent_type": "UNKNOWN",  # 필수 필드 추가
                "raw_text": text,          # 필수 필드 추가
                "screen_state": screen_state,  # 필수 필드 추가
                "success": True,
                "data": {
                    "pre_text": text,
                    "post_text": text,
                    "reply": "죄송합니다. 명령을 이해하지 못했습니다.",
                    "status": "UNKNOWN",
                    "language": language,
                    "store_id": store_id
                },
                "error": None,
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
    
    def _process_order_intent(self, rag_result: Dict[str, Any], store_id: int) -> Dict[str, Any]:
        """주문 의도 처리"""
        try:
            recognized_menus = []
            
            for menu_data in rag_result.get("recognized_menus", []):
                menu_name = menu_data.get("menu_name", "")
                original_menu_name = menu_data.get("original_menu_name", "")  # 원래 입력한 메뉴명 추출
                
                # 벡터 DB에서 메뉴 검색
                print(f"검색 쿼리: {menu_name}, 매장 ID: {store_id}")
                menu_search_results = self.rag_service.vector_store.search_menu(menu_name, store_id, top_k=3)
                print(f"검색 결과: {menu_search_results}")

                if menu_search_results:
                    # 검색된 메뉴 정보
                    menu_info = menu_search_results[0]
                    menu_id = menu_info.get("id")    
                    # 메뉴의 옵션 정보 조회
                    all_options = self.rag_service.vector_store.mysql.get_menu_options(menu_id, store_id)
                    
                    # 사용자가 언급한 옵션
                    selected_options = []
                    for option_data in menu_data.get("options", []):
                        option_name = option_data.get("option_name", "").lower()
                        option_value = option_data.get("option_value", "").lower()
                        
                        print(f"사용자 지정 옵션: {option_name}={option_value}")
        
                        # 옵션 매핑 (유연한 매핑)
                        matched_option = None
                        matched_option_detail = None
                        
                        # 1. 직접 매핑 시도 (옵션 이름 정확히 일치)
                        for opt in all_options:
                            opt_name = opt.get("option_name", "").lower()
                            if opt_name == option_name or option_name in opt_name or opt_name in option_name:
                                matched_option = opt
                                
                                # # 옵션 값 찾기
                                # for detail in opt.get("option_details", []):
                                #     detail_value = detail.get("value", "").lower()
                                #     if detail_value == option_value or option_value in detail_value or detail_value in option_value:
                                #         matched_option_detail = detail
                                #         break

                                # 옵션 값 매칭에 _match_option_value 함수 사용
                                matched_option_detail = self._match_option_value(option_value, opt.get("option_details", []))
                                
                                if matched_option_detail:
                                    break
                        
                        # 특별한 케이스 처리 (옵션 이름 불일치)
                        if not matched_option or not matched_option_detail:
                            # 예: "아이스 아메리카노" -> "온도" 옵션 자동 매핑
                            for opt in all_options:
                                # 온도 옵션 검색
                                if "온도" in opt.get("option_name", "").lower():
                                    if "아이스" in option_value or "ice" in option_value:
                                        matched_option = opt
                                        matched_option_detail = self._match_option_value("ice", opt.get("option_details", []))
                                    elif "따뜻한" in option_value or "hot" in option_value:
                                        matched_option = opt
                                        matched_option_detail = self._match_option_value("hot", opt.get("option_details", []))
                                    if matched_option_detail:
                                        break
                                
                                # 사이즈 옵션 검색
                                elif "사이즈" in opt.get("option_name", "").lower():
                                    if any(keyword in option_value for keyword in ["작은", "스몰", "small", "s"]):
                                        matched_option = opt
                                        matched_option_detail = self._match_option_value("s", opt.get("option_details", []))
                                    elif any(keyword in option_value for keyword in ["중간", "미디엄", "medium", "m"]):
                                        matched_option = opt
                                        matched_option_detail = self._match_option_value("m", opt.get("option_details", []))
                                    elif any(keyword in option_value for keyword in ["큰", "라지", "large", "l"]):
                                        matched_option = opt
                                        matched_option_detail = self._match_option_value("l", opt.get("option_details", []))
                                    if matched_option_detail:
                                        break
                        
                        # 매칭된 옵션이 있으면 selected_options에 추가
                        if matched_option and matched_option_detail:
                            selected_option = {
                                "option_id": matched_option.get("option_id"),
                                "option_name": matched_option.get("option_name"),
                                "required": matched_option.get("required", False),
                                "is_selected": True,
                                "option_details": [matched_option_detail]
                            }
                            selected_options.append(selected_option)

                            # 2. options 배열의 해당 옵션도 업데이트
                            for option in all_options:
                                if option.get("option_id") == matched_option.get("option_id"):
                                    option["is_selected"] = True
                                    # 선택된 옵션 상세 ID 저장
                                    option["selected_id"] = matched_option_detail.get("id")
                                    break
                            print(f"옵션 매핑 성공: {option_name}={option_value} -> {matched_option.get('option_name')}={matched_option_detail.get('value')}")
                        else:
                            print(f"옵션 매핑 실패: {option_name}={option_value}")
                    
                    # 기본 메뉴 정보
                    enriched_menu = {
                        "menu_id": menu_id,
                        "quantity": menu_data.get("quantity", 1),
                        "name": menu_info.get("name_kr", menu_name),
                        "name_en": menu_info.get("name_en", ""),
                        "description": menu_info.get("description", ""),
                        "base_price": menu_info.get("price", 0),
                        "total_price": menu_info.get("price", 0),  # 추후 옵션 가격 추가
                        "image_url": menu_info.get("image_url", ""),
                        "options": all_options,  # 모든 옵션 정보
                        "selected_options": selected_options,  # 선택된 옵션 정보
                        "is_corrected": menu_name.lower() != menu_info.get("name_kr", "").lower(),  # 메뉴명 교정 여부
                        "original_name": menu_name if menu_name.lower() != menu_info.get("name_kr", "").lower() else None  # 원래 입력한 메뉴명
                    }
                    # 총 가격 업데이트
                    enriched_menu["total_price"] = self._calculate_total_price(enriched_menu)
                    
                    recognized_menus.append(enriched_menu)
                elif menu_search_results:
                    # 검색 결과는 있지만 유사도가 낮은 경우 추천 메뉴로 처리
                    # 카테고리나 메뉴 특성에 따라 관련 메뉴 추천을 위한 로직
                    # 다양한 메뉴 특성 비교하기 (e.g., "바나나" -> 과일 특성이 있는 "딸기 스무디" 추천)
                    
                    # 가장 유사한 결과가 일정 점수 이하인 경우만 표시
                    if menu_search_results[0].get('score', 1.0) <= 0.7:  # 0.7은 조정 가능한 임계값
                        menu_info = menu_search_results[0]
                        menu_id = menu_info.get("id")
                        
                        # 메뉴의 옵션 정보 조회
                        all_options = self.rag_service.vector_store.mysql.get_menu_options(menu_id, store_id)
                        
                        enriched_menu = {
                            "menu_id": menu_id,
                            "quantity": menu_data.get("quantity", 1),
                            "name": menu_info.get("name_kr", menu_name),
                            "name_en": menu_info.get("name_en", ""),
                            "description": menu_info.get("description", ""),
                            "base_price": menu_info.get("price", 0),
                            "total_price": menu_info.get("price", 0),
                            "image_url": menu_info.get("image_url", ""),
                            "options": all_options,
                            "selected_options": [],
                            "is_recommendation": True,
                            "recommendation_reason": f"{menu_name}와(과) 유사한 메뉴입니다."
                        }
                        # 총 가격 업데이트
                        enriched_menu["total_price"] = self._calculate_total_price(enriched_menu)
                        
                        recognized_menus.append(enriched_menu)
                    else:
                        # 관련 메뉴가 없는 경우 - 카테고리별 인기 메뉴 추천
                        popular_menu = self._get_popular_menu(store_id)
                        if popular_menu:
                            menu_id = popular_menu.get("id")
                            all_options = self.rag_service.vector_store.mysql.get_menu_options(menu_id, store_id)
                            
                            enriched_menu = {
                                "menu_id": menu_id,
                                "quantity": menu_data.get("quantity", 1),
                                "name": popular_menu.get("name_kr", ""),
                                "name_en": popular_menu.get("name_en", ""),
                                "description": popular_menu.get("description", ""),
                                "base_price": popular_menu.get("price", 0),
                                "total_price": popular_menu.get("price", 0),
                                "image_url": popular_menu.get("image_url", ""),
                                "options": all_options,
                                "selected_options": [],
                                "is_recommendation": True,
                                "recommendation_reason": f"{menu_name}은(는) 찾을 수 없습니다. 인기 메뉴를 추천해 드립니다."
                            }
                            # 총 가격 업데이트
                            enriched_menu["total_price"] = self._calculate_total_price(enriched_menu)
                            
                            recognized_menus.append(enriched_menu)
                else:
                    # 메뉴를 전혀 찾지 못한 경우 - 인기 메뉴 추천
                    popular_menu = self._get_popular_menu(store_id)
                    if popular_menu:
                        # 인기 메뉴 정보 추가
                        # ...
                        pass
            
            # 응답 메시지 생성
            reply = self._generate_order_reply(recognized_menus)
            
            # 응답 구성
            return {
                "intent_type": "ORDER",  # 필수 필드 
                "raw_text": rag_result.get("raw_text", ""),
                "screen_state": rag_result.get("screen_state", ""),
                "recognized_menus": recognized_menus,  # 중요! 이 필드가 최종 응답에 포함됨
                "success": True,
                "data": {
                    "pre_text": rag_result.get("raw_text", ""),
                    "post_text": rag_result.get("raw_text", ""),
                    "reply": reply,
                    "status": "ORDER",
                    "language": rag_result.get("language", "ko"),
                    "session_id": "",
                    "cart": [],
                    "contents": recognized_menus,
                    "store_id": store_id
                },
                "error": None,
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        except Exception as e:
            print(f"주문 처리 중 오류 발생: {e}")
            return {
                "intent_type": "ERROR",
                "raw_text": rag_result.get("raw_text", ""),
                "screen_state": rag_result.get("screen_state", ""),
                "success": False,
                "data": {
                    "pre_text": rag_result.get("raw_text", ""),
                    "post_text": rag_result.get("raw_text", ""),
                    "reply": "죄송합니다. 주문 처리 중 오류가 발생했습니다. 다시 시도해주세요.",
                    "status": "ERROR",
                    "language": rag_result.get("language", "ko"),
                    "store_id": store_id
                },
                "error": str(e),
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

    def _generate_order_reply(self, recognized_menus: List[Dict[str, Any]]) -> str:
        """주문 응답 메시지 생성"""
        if not recognized_menus:
            return "죄송합니다. 주문하신 메뉴를 찾을 수 없습니다."
        
        # 첫 번째 메뉴 기준으로 응답 메시지 생성
        menu = recognized_menus[0]
        menu_name = menu.get("name", "")
        
        # 메뉴 상태에 따른 응답 생성
        # 1. 메뉴명 교정된 경우
        if menu.get("is_corrected", False):
            original_name = menu.get("original_name", "")
            return f"{original_name}을(를) {menu_name}(으)로 이해했습니다. {menu_name}를 주문하시겠습니까?"
        
        # 2. 추천 메뉴인 경우
        if menu.get("is_recommendation", False):
            reason = menu.get("recommendation_reason", "유사한 메뉴를 찾지 못했습니다.")
            return f"죄송합니다. {reason} 대신 {menu_name}는 어떠세요?"
        
        # 3. 필수 옵션 누락 여부 확인
        missing_required_options = self._validate_required_options(menu)
        
        if missing_required_options:
            # 누락된 옵션이 하나인 경우 구체적인 질문
            if len(missing_required_options) == 1:
                option = missing_required_options[0]
                option_name = option.get("option_name", "")
                option_details = option.get("option_details", [])
                
                # 옵션 값 목록 생성
                option_values = [detail.get("value", "") for detail in option_details]
                
                # 특별한 옵션 유형에 따른 응답
                if "온도" in option_name or "Temperature" in option_name:
                    return f"{menu_name}를 선택하셨네요. 따뜻한 것으로 드릴까요, 차가운 것으로 드릴까요?"
                elif "사이즈" in option_name or "Size" in option_name:
                    return f"{menu_name}를 선택하셨네요. 어떤 사이즈로 드릴까요? ({', '.join(option_values)})"
                else:
                    return f"{menu_name}를 선택하셨네요. {option_name}을(를) 선택해주세요. ({', '.join(option_values)})"
            else:
                # 여러 옵션이 누락된 경우
                option_names = [opt.get("option_name", "") for opt in missing_required_options]
                return f"{menu_name}를 선택하셨네요. {', '.join(option_names)}을(를) 선택해주세요."
        
        # 4. 모든 필수 옵션이 선택된 경우
        # 옵션 내용 요약
        selected_options_desc = []
        for opt in menu.get("selected_options", []):
            opt_name = opt.get("option_name", "")
            opt_details = opt.get("option_details", [])
            if opt_details:
                opt_value = opt_details[0].get("value", "")
                selected_options_desc.append(f"{opt_name}: {opt_value}")
        
        options_summary = ""
        if selected_options_desc:
            options_summary = f" ({', '.join(selected_options_desc)})"
        
        return f"{menu_name}{options_summary}를 장바구니에 담았습니다. 더 주문하실 건가요?"
        
    def _get_popular_menu(self, store_id: int) -> Dict[str, Any]:
        """인기 메뉴 조회 - 임시로 하드코딩된 메뉴 반환"""
        """추 후 구현 예정"""
        # 실제로는 DB에서 인기 메뉴를 조회해야 함
        # 임시 구현: 각 카테고리별 대표 메뉴 리스트
        popular_menus = [
            {"id": 4, "name_kr": "아메리카노", "name_en": "Americano", "description": "깔끔한 맛의 아메리카노", "price": 2500, "category": "커피"},
            {"id": 6, "name_kr": "바닐라 라떼", "name_en": "Vanilla Latte", "description": "바닐라 시럽이 달콤하게 어우러진 라떼", "price": 3000, "category": "커피"},
            {"id": 9, "name_kr": "딸기 스무디", "name_en": "Strawberry Smoothie", "description": "새콤달콤한 딸기 스무디", "price": 3500, "category": "스무디"},
            {"id": 13, "name_kr": "쿠키 프라페", "name_en": "Cookie Frappé", "description": "쿠키 토핑이 올라간 프라페", "price": 4000, "category": "프라페"}
        ]
        
        # 랜덤으로 하나 선택하여 반환
        import random
        return random.choice(popular_menus)
    
    def _match_option_value(self, option_value: str, option_details: List[Dict[str, Any]]) -> Dict[str, Any]:
        """사용자 입력 옵션 값을 시스템 옵션 값과 매핑"""
        # 옵션 값 정규화 (소문자, 공백 제거)
        option_value_norm = option_value.lower().replace(" ", "")
        
        # 1. 직접 매칭
        for detail in option_details:
            detail_value = detail.get("value", "").lower().replace(" ", "")
            if detail_value == option_value_norm:
                return detail
        
        # 2. 유사도 매칭 (포함 관계)
        for detail in option_details:
            detail_value = detail.get("value", "").lower()
            if option_value_norm in detail_value or detail_value in option_value_norm:
                return detail
        
        # 3. 특수 케이스 매핑
        special_mappings = {
            "작은": "S", "스몰": "S", "small": "S", 
            "중간": "M", "미디엄": "M", "medium": "M",
            "큰": "L", "라지": "L", "large": "L",
            "뜨거운": "HOT", "따뜻한": "HOT", "따아": "HOT", "hot": "HOT",
            "차가운": "ICE", "아이스": "ICE", "아아": "ICE", "ice": "ICE"
        }
        
        for keyword, target in special_mappings.items():
            if keyword in option_value_norm:
                for detail in option_details:
                    if detail.get("value", "").lower() == target.lower():
                        return detail
        
        return None  # 매칭 실패

    def _validate_required_options(self, menu: Dict[str, Any]) -> List[Dict[str, Any]]:
        """필수 옵션 검증"""
        missing_options = []
        
        for option in menu.get("options", []):
            if option.get("required", False):
                option_id = option.get("option_id")
                # 선택된 옵션 중에 해당 옵션이 있는지 확인
                found = False
                for selected_opt in menu.get("selected_options", []):
                    if selected_opt.get("option_id") == option_id:
                        found = True
                        break
                
                if not found:
                    missing_options.append(option)
        
        return missing_options

    def _calculate_total_price(self, menu: Dict[str, Any]) -> int:
        """선택된 옵션을 포함한 총 가격 계산"""
        base_price = menu.get("base_price", 0)
        total_additional_price = 0
        
        print(f"계산 전 base_price: {base_price}, total_additional_price: {total_additional_price}")
        
        for selected_option in menu.get("selected_options", []):
            option_details = selected_option.get("option_details", [])

            if option_details:

                ## test
                option_name = selected_option.get("option_name", "")     # ✅ 딕셔너리에서 key로 접근해야 함
                option_value = option_details[0].get("value", "")
                ## -------------

                additional_price = option_details[0].get("additional_price", 0)
                total_additional_price += additional_price

                ## test
                print(f"옵션 이름름: {option_name}, 가격 확인 메뉴 이름름: {option_value},total_additional_price: {additional_price}")
                ## --------------

        print(f"계산 후 base_price: {base_price}, total_additional_price: {total_additional_price}")
        
        return base_price + total_additional_price