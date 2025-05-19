# app/services/processor/search_processor.py
from typing import Dict, Any, List
import json
import re

from app.models.schemas import IntentType, ScreenState, Language, ResponseStatus
from app.services.processor.base_processor import BaseProcessor
# from app.services.vector_db_service import VectorDBService
from app.services.response.response_generator import ResponseGenerator
from app.models.schemas import ResponseStatus

class SearchProcessor(BaseProcessor):
    """메뉴 검색 처리 프로세서"""
    
    def __init__(self, response_generator: ResponseGenerator, menu_service, session_manager):
        """프로세서 초기화"""
        self.response_generator = response_generator
        self.menu_service = menu_service
        self.session_manager = session_manager
        # 벡터 DB 서비스 인스턴스 가져오기
        # self.vector_db_service = VectorDBService.get_instance()
    
    def process(self, intent_data: Dict[str, Any], text: str, language: str, screen_state: str, store_id: int, session: Dict[str, Any]) -> Dict[str, Any]:
        """검색 의도 처리"""
        try:
            # 매장의 메뉴 정보 로드
            store_menus = self.menu_service.get_store_menus(store_id)
            
            # 검색 결과를 저장할 리스트
            search_results = []
            
            # LLM이 인식한 메뉴 ID로 검색
            menus = intent_data.get("menus", [])
            for menu in menus:
                menu_id = menu.get("menu_id")
                if menu_id and menu_id in store_menus:
                    menu_info = store_menus[menu_id].copy()  # 복사본 생성
                    menu_info["id"] = menu_id  # ID 명시적 설정
                    menu_info["menu_id"] = menu_id  # menu_id도 추가
                    if menu_info not in search_results:
                        search_results.append(menu_info)
            
            # 검색 결과 정리 (필요한 필드만 포함)
            cleaned_results = []
            for menu in search_results:
                cleaned_menu = {
                    "id": menu.get("id"),
                    "menu_id": menu.get("menu_id"),
                    "name_kr": menu.get("name_kr", ""),
                    "name_en": menu.get("name_en", ""),
                    "description": menu.get("description", ""),
                    "price": menu.get("price", 0),
                    "image_url": menu.get("image_url", ""),
                    "category_id": menu.get("category_id"),
                    "status": menu.get("status", "")
                }
                cleaned_results.append(cleaned_menu)
            
            # 응답 메시지 생성
            reply = intent_data.get("reply", "찾으신 메뉴를 보여드릴게요.")
            
            # 응답 구성
            response = {
                "intent_type": IntentType.SEARCH,
                "confidence": intent_data.get("confidence", 0.8 if cleaned_results else 0.6),
                "search_query": text,
                "raw_text": text,
                "screen_state": ScreenState.SEARCH,
                "data": {
                    "pre_text": text,
                    "post_text": intent_data.get("post_text", text),
                    "reply": reply,
                    "status": ResponseStatus.SEARCH_RESULTS if cleaned_results else ResponseStatus.UNKNOWN,
                    "language": language,
                    "session_id": session.get("id", ""),
                    "cart": session.get("cart", []),
                    "contents": cleaned_results,
                    "store_id": store_id
                }
            }
            
            print(f"[검색 처리] 검색 결과 수: {len(cleaned_results)}")
            print(f"[검색 처리] 응답: {json.dumps(response, ensure_ascii=False)}")
            
            return response
            
        except Exception as e:
            print(f"[검색 처리 오류] {e}")
            import traceback
            traceback.print_exc()
            
            # 오류 발생 시 기본 응답
            return {
                "intent_type": IntentType.SEARCH,
                "confidence": 0.3,
                "raw_text": text,
                "screen_state": ScreenState.SEARCH,
                "data": {
                    "pre_text": text,
                    "post_text": text,
                    "reply": "검색 중 오류가 발생했어요. 다시 시도해주세요.",
                    "status": ResponseStatus.UNKNOWN,
                    "language": language,
                    "session_id": session.get("id", ""),
                    "cart": session.get("cart", []),
                    "contents": [],
                    "store_id": store_id
                }
            }
    
    def _analyze_query_with_llm(self, query: str) -> Dict[str, Any]:
        """LLM을 사용한 쿼리 분석 및 최적화"""
        try:
            # 부정 표현 및 대상 추출
            negative_expressions = ["없는", "안들어간", "제외", "빼고", "말고"]
            negative_targets = []
            
            # 커피 없는, 우유 없는 등의 패턴 확인
            coffee_free = False
            dairy_free = self._is_dairy_free_search(query)
            
            # 커피 제외 확인
            if "커피" in query.lower() and any(expr in query.lower() for expr in negative_expressions):
                coffee_free = True
                negative_targets.append("커피")
            
            # 최적화된 쿼리 구성
            optimized = query.lower().strip()
            
            # 결과 구성
            result = {
                "keywords": [query],
                "attributes": {
                    "decaf": self._is_decaf_search(query),
                    "item_type": "all",
                    "dairy_free": dairy_free,
                    "coffee_free": coffee_free,
                    "negative_targets": negative_targets,
                    "seasonal": False,
                    "low_calorie": False,
                    "other": []
                },
                "optimized_query": optimized
            }
            
            # 음료/디저트 구분
            if result["attributes"]["decaf"] or "음료" in query.lower() or "마실" in query.lower():
                result["attributes"]["item_type"] = "beverage"
            elif "디저트" in query.lower() or "먹을" in query.lower() or "케이크" in query.lower():
                result["attributes"]["item_type"] = "dessert"
            
            # 커피 카테고리 필터링 개선
            if coffee_free and "커피" not in optimized:
                optimized += " -커피"  # 부정 검색어 추가
            
            # 최종 최적화된 쿼리 업데이트
            result["optimized_query"] = optimized
            
            return result
            
        except Exception as e:
            print(f"[벡터 DB] 쿼리 분석 오류: {e}")
            
            # 오류 발생 시 기본 분석 결과 제공
            is_decaf = self._is_decaf_search(query)
            is_dairy_free = self._is_dairy_free_search(query)
            
            # 음료/디저트 구분 (기본값은 item_type="all")
            item_type = "all"
            if is_decaf or "음료" in query.lower() or "마실" in query.lower() or "커피" in query.lower():
                item_type = "beverage"
            elif "디저트" in query.lower() or "먹을" in query.lower() or "케이크" in query.lower():
                item_type = "dessert"

            optimized = query.lower().strip()
            if is_decaf and "디카페인" not in optimized:
                optimized = "디카페인 커피 음료 " + optimized
            if is_dairy_free and "우유 없는" not in optimized:
                optimized += " 우유 없는 음료"

            return {
                "keywords": [query],
                "attributes": {
                    "decaf": is_decaf,
                    "item_type": item_type,
                    "dairy_free": is_dairy_free,
                    "seasonal": False,
                    "low_calorie": False,
                    "other": []
                },
                "optimized_query": optimized
            }
    
    def _is_decaf_search(self, query: str) -> bool:
        """디카페인 검색 여부 확인"""
        decaf_keywords = ["디카페인", "카페인 없는", "카페인없는", "카페인 제거", "카페인제거", "decaf"]
        return any(keyword in query.lower() for keyword in decaf_keywords)
    
    def _is_dairy_free_search(self, query: str) -> bool:
        """우유 없는 메뉴 검색 여부 확인"""
        dairy_free_keywords = ["우유 없는", "우유없는", "우유 알레르기", "우유알레르기", "락토스", "유당", "비건", "vegan", "plant"]
        negative_dairy_terms = ["우유", "라떼", "밀크", "크림", "요거트"]
        
        query_lower = query.lower()
        
        # 직접적인 키워드 확인
        has_direct_keyword = any(keyword in query_lower for keyword in dairy_free_keywords)
        
        # '우유 없는' 패턴 확인 (한국어 특성상 부정어가 따로 있을 수 있음)
        negative_pattern = any(term in query_lower and ("없" in query_lower or "안" in query_lower or "말고" in query_lower) 
                              for term in negative_dairy_terms)
        
        return has_direct_keyword or negative_pattern
    
    def _get_store_categories(self, store_id: int) -> Dict[str, List[int]]:
        """매장별 카테고리 정보 로드"""
        # 매장의 카테고리 목록 가져오기
        categories = self.menu_service.get_store_categories(store_id)
        
        # 카테고리 타입별 분류
        beverage_categories = []
        dessert_categories = []
        other_categories = []
        
        # 카테고리 이름으로 음료/디저트 구분
        beverage_keywords = ["커피", "음료", "차", "에이드", "스무디", "티", "주스", "라떼", "아메리카노", "카페"]
        dessert_keywords = ["디저트", "케이크", "빵", "쿠키", "베이커리", "아이스크림", "스낵", "파이"]
        
        for category in categories:
            category_name = category.get("name_kr", "").lower()
            category_id = category.get("id")
            
            # 카테고리 이름으로 음료/디저트 구분
            if any(keyword in category_name for keyword in beverage_keywords):
                beverage_categories.append(category_id)
            elif any(keyword in category_name for keyword in dessert_keywords):
                dessert_categories.append(category_id)
            else:
                other_categories.append(category_id)
        
        # 카테고리가 없는 경우 기본값 추가
        if not beverage_categories:
            # 기본적으로 ID가 100~110 범위의 카테고리는 음료로 가정
            beverage_categories = list(range(100, 110))
        
        if not dessert_categories:
            # 기본적으로 ID가 110~120 범위의 카테고리는 디저트로 가정
            dessert_categories = list(range(110, 120))
        
        return {
            "beverage": beverage_categories,
            "dessert": dessert_categories,
            "other": other_categories,
            "all": beverage_categories + dessert_categories + other_categories
        }