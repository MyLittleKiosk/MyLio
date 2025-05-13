# app/services/processor/search_processor.py
from typing import Dict, Any, List
import json
import re

from app.models.schemas import IntentType, ScreenState, Language, ResponseStatus
from app.services.processor.base_processor import BaseProcessor
from app.services.vector_db_service import VectorDBService
from app.services.response.response_generator import ResponseGenerator
from app.models.schemas import ResponseStatus

class SearchProcessor(BaseProcessor):
    """RAG 기반 검색 처리 프로세서"""
    
    def __init__(self, response_generator: ResponseGenerator, menu_service, session_manager):
        """프로세서 초기화"""
        self.response_generator = response_generator
        self.menu_service = menu_service
        self.session_manager = session_manager
        # 벡터 DB 서비스 인스턴스 가져오기
        self.vector_db_service = VectorDBService.get_instance()
    
    def process(self, intent_data: Dict[str, Any], text: str, language: str, screen_state: str, store_id: int, session: Dict[str, Any]) -> Dict[str, Any]:
        """검색 의도 처리"""
        # 검색 쿼리 추출 
        search_query = intent_data.get("search_query", text)

        # LLM을 통한 분석 - 전체 결과 활용
        result = self._analyze_query_with_llm(search_query)
        
        # LLM을 통한 쿼리 최적화
        optimized_query = result.get("optimized_query", search_query)
        attributes = result.get("attributes", {})
        
        # 디카페인 검색 여부 확인
        is_decaf_search = attributes.get("decaf", False) or self._is_decaf_search(search_query)
        item_type = attributes.get("item_type", "all")

        # 매장의 카테고리 정보 로드
        store_categories = self._get_store_categories(store_id)
        
        # 벡터 검색 실행
        vector_results = self.vector_db_service.search(optimized_query, store_id=store_id, k=10)
        
        # 검색 결과 처리
        search_results = []
        if vector_results:
            store_menus = self.menu_service.get_store_menus(store_id)
            for result in vector_results:
                menu_id = result["menu_id"]
                if menu_id in store_menus:
                    menu = store_menus[menu_id].copy()
                    menu["search_score"] = result["similarity"]
                    search_results.append(menu)
        
        # 키워드 기반 필터링 추가 (벡터 검색 결과 정제)
        if search_results:
            direct_match_score = 0.9  # 직접 매칭 시 높은 점수
            
            # 검색어 추출
            query_keywords = search_query.lower().split()
            
            # 검색 결과에서 직접 관련된 결과 필터링
            exact_matches = []
            related_matches = []
            
            for menu in search_results:
                menu_name = menu.get("name_kr", "").lower()
                menu_desc = menu.get("description", "").lower()
                
                # 완전 일치 검사 (에이드 -> "에이드"가 이름에 포함)
                if any(keyword in menu_name for keyword in query_keywords):
                    menu["search_score"] = direct_match_score  # 정확한 매칭에 높은 점수
                    exact_matches.append(menu)
                # 부분 관련 검사 (설명에 포함)
                elif any(keyword in menu_desc for keyword in query_keywords):
                    related_matches.append(menu)
            
            # 정확한 매칭이 있으면 그것을 우선 사용
            if exact_matches:
                search_results = exact_matches + related_matches  # 정확한 매칭을 앞에 배치
                print(f"[검색 필터링] 이름 기반 정확한 매칭: {len(exact_matches)}개, 관련 매칭: {len(related_matches)}개")
        

        # 카테고리 필터링 적용
        if item_type != "all" or is_decaf_search:
            # 디카페인 검색은 항상 음료 카테고리로 제한
            if is_decaf_search:
                item_type = "beverage"
            
            # 해당 타입의 카테고리 ID 목록 가져오기
            category_ids = store_categories.get(item_type, [])
            if category_ids:
                # 카테고리 필터링 적용
                search_results = [menu for menu in search_results if menu.get("category_id") in category_ids]
        
        # 디카페인 검색인 경우 추가 필터링
        if is_decaf_search:
        
            direct_decaf_results = []
            store_menus = self.menu_service.get_store_menus(store_id)
            
            for menu_id, menu in store_menus.items():
                # 디카페인 관련 메뉴 확인
                has_decaf = (
                    "디카페인" in menu.get("name_kr", "").lower() or 
                    "decaf" in menu.get("name_en", "").lower() or
                    "디카페인" in menu.get("description", "").lower() or
                    any("디카페인" in tag.get("tag_kr", "").lower() for tag in menu.get("tags", []))
                )
                
                if has_decaf:
                    # 카테고리 필터링이 있다면 적용
                    if item_type != "all" and category_ids and menu.get("category_id") not in category_ids:
                        continue
                        
                    # 중복 검사 (이미 search_results에 있는 메뉴인지 확인)
                    if not any(result.get("id") == menu.get("id") for result in search_results):
                        menu_copy = menu.copy()
                        menu_copy["search_score"] = 0.9  # 직접 필터링은 높은 점수 부여
                        direct_decaf_results.append(menu_copy)
            
            # 직접 검색한 결과를 기존 결과에 추가
            if direct_decaf_results:
                print(f"[디카페인 검색] 직접 검색 추가 결과: {len(direct_decaf_results)}개")
                search_results.extend(direct_decaf_results)
                
            # 중복 제거 (혹시 모를 중복 방지)
            unique_ids = set()
            unique_results = []
            for menu in search_results:
                if menu.get("id") not in unique_ids:
                    unique_ids.add(menu.get("id"))
                    unique_results.append(menu)
            
            # 중복 제거 후 결과 업데이트
            search_results = unique_results
            
            # 결과 정렬 (점수 높은 순)
            search_results.sort(key=lambda x: x.get("search_score", 0), reverse=True)
            
            print(f"[디카페인 검색] 최종 결과: {len(search_results)}개")
        
        # 에이드 검색인 경우
        if "에이드" in search_query.lower():
            direct_ade_results = []
            store_menus = self.menu_service.get_store_menus(store_id)
            
            for menu_id, menu in store_menus.items():
                # 에이드가 이름에 포함된 메뉴
                if "에이드" in menu.get("name_kr", "").lower() or "ade" in menu.get("name_en", "").lower():
                    # 중복 검사
                    if not any(result.get("id") == menu.get("id") for result in search_results):
                        menu_copy = menu.copy()
                        menu_copy["search_score"] = 0.95  # 직접 매칭 - 높은 점수
                        direct_ade_results.append(menu_copy)
            
            # 에이드 메뉴가 있으면 결과에 추가
            if direct_ade_results:
                print(f"[에이드 검색] 직접 검색 결과: {len(direct_ade_results)}개")
                # 기존 결과를 버리지 말고 합치기
                search_results = direct_ade_results + search_results  # 직접 검색 결과를 앞에 추가
                # 중복 제거
                unique_ids = set()
                unique_results = []
                for menu in search_results:
                    if menu.get("id") not in unique_ids:
                        unique_ids.add(menu.get("id"))
                        unique_results.append(menu)
                search_results = unique_results

        # 디저트 검색인 경우
        if "디저트" in search_query.lower() or "디져트" in search_query.lower() or "케이크" in search_query.lower():
            direct_dessert_results = []
            store_menus = self.menu_service.get_store_menus(store_id)
            
            for menu_id, menu in store_menus.items():
                # 디저트 카테고리 메뉴 (카테고리 ID 예시)
                if menu.get("category_id") == 107:  # 디저트 카테고리 ID 확인 필요
                    # 중복 검사
                    if not any(result.get("id") == menu.get("id") for result in search_results):
                        menu_copy = menu.copy()
                        menu_copy["search_score"] = 0.9
                        direct_dessert_results.append(menu_copy)
            
            # 디저트 메뉴가 있으면 결과에 추가
            if direct_dessert_results:
                print(f"[디저트 검색] 직접 검색 결과: {len(direct_dessert_results)}개")
                search_results = direct_dessert_results  # 벡터 검색보다 직접 검색 우선
        
        # dairy_free 속성이 True일 경우 우유 관련 재료/옵션이 있는 메뉴 제거
        if attributes.get("dairy_free") is True or ("우유" in search_query and ("없" in search_query or "안" in search_query)):
            filtered_results = []
            for menu in search_results:
                has_milk = False
                
                # 이름에 "우유", "밀크", "라떼" 등의 키워드 체크
                menu_name = menu.get("name_kr", "").lower()
                menu_name_en = menu.get("name_en", "").lower() if menu.get("name_en") else ""
                milk_keywords = ["우유", "밀크", "라떼", "milk", "latte", "cream", "크림"]
                
                if any(keyword in menu_name for keyword in milk_keywords) or any(keyword in menu_name_en for keyword in milk_keywords):
                    has_milk = True
                    continue  # 바로 제외
                
                # 태그 확인 강화
                if menu.get("tags"):
                    for tag in menu.get("tags", []):
                        tag_kr = tag.get("tag_kr", "").lower()
                        tag_en = tag.get("tag_en", "").lower()
                        if "우유" in tag_kr or "milk" in tag_en:
                            has_milk = True
                            break
                
                # 원재료 확인 강화
                if menu.get("ingredients"):
                    for ing in menu.get("ingredients", []):
                        ing_name = ing.get("name_kr", "").lower()
                        ing_name_en = ing.get("name_en", "").lower() if ing.get("name_en") else ""
                        if "우유" in ing_name or "milk" in ing_name_en:
                            has_milk = True
                            break
                
                # 우유가 없는 메뉴만 필터링된 결과에 추가
                if not has_milk:
                    filtered_results.append(menu)
            
            # 필터링된 결과로 대체
            search_results = filtered_results

        # 커피 제외 필터링 추가
        if "커피" in search_query and ("없" in search_query or "안" in search_query or "빼" in search_query or "제외" in search_query):
            filtered_results = []
            for menu in search_results:
                has_coffee = False
                
                # 이름에 "커피", "coffee" 등의 키워드 체크
                menu_name = menu.get("name_kr", "").lower()
                menu_name_en = menu.get("name_en", "").lower() if menu.get("name_en") else ""
                coffee_keywords = ["커피", "coffee", "espresso", "에스프레소", "아메리카노", "라떼", "카페"]
                
                if any(keyword in menu_name for keyword in coffee_keywords) or any(keyword in menu_name_en for keyword in coffee_keywords):
                    has_coffee = True
                    continue
                
                # 태그 확인
                if menu.get("tags"):
                    for tag in menu.get("tags", []):
                        tag_kr = tag.get("tag_kr", "").lower()
                        tag_en = tag.get("tag_en", "").lower()
                        if "커피" in tag_kr or "coffee" in tag_en:
                            has_coffee = True
                            break
                
                # 원재료 확인
                if menu.get("ingredients"):
                    for ing in menu.get("ingredients", []):
                        ing_name = ing.get("name_kr", "").lower()
                        ing_name_en = ing.get("name_en", "").lower() if ing.get("name_en") else ""
                        if "커피" in ing_name or "coffee" in ing_name_en or "에스프레소" in ing_name or "espresso" in ing_name_en:
                            has_coffee = True
                            break
                
                # 커피가 없는 메뉴만 필터링된 결과에 추가
                if not has_coffee:
                    filtered_results.append(menu)
            
            # 필터링된 결과로 대체
            search_results = filtered_results
        
        # 컨텍스트 구성
        context = {
            "status": ResponseStatus.SEARCH_RESULTS if search_results else ResponseStatus.UNKNOWN,
            "search_query": search_query,
            "search_results": search_results,
            "attributes": attributes,
            "screen_state": ScreenState.SEARCH
        }
        
        # 응답 상태 결정
        status = ResponseStatus.SEARCH_RESULTS if search_results else ResponseStatus.UNKNOWN
        
        # 검색 결과가 많을 경우 모든 메뉴 이름을 나열하지 않도록 수정
        reply = intent_data.get("reply")
        if not reply:
            if search_results and len(search_results) > 0:
                # 매우 간결한 응답 생성 (메뉴 이름 나열 없이)
                if language == Language.KR:
                    reply = f"'{search_query}'에 대한 검색 결과에요. {len(search_results)}개의 메뉴가 있어요."
                elif language == Language.EN:
                    reply = f"Here are the search results for '{search_query}'. Found {len(search_results)} menu items."
                elif language == Language.JP:
                    reply = f"'{search_query}'の検索結果です。{len(search_results)}個のメニューがあります。"
                elif language == Language.CN:
                    reply = f"'{search_query}'的搜索结果。找到了{len(search_results)}个菜单。"
            else:
                # 검색 결과가 없는 경우
                if language == Language.KR:
                    reply = f"'{search_query}'에 대한 검색 결과가 없어요."
                elif language == Language.EN:
                    reply = f"No results found for '{search_query}'."
                elif language == Language.JP:
                    reply = f"'{search_query}'の検索結果はありません。"
                elif language == Language.CN:
                    reply = f"没有找到'{search_query}'的搜索结果。"

        # 검색 결과 정리 (불필요한 필드 제거)
        cleaned_results = []
        for menu in search_results:
            cleaned_menu = {
                "id": menu.get("id"),
                "name_kr": menu.get("name_kr", ""),
                "name_en": menu.get("name_en", ""),
                "description": menu.get("description", ""),
                "price": menu.get("price", 0),
                "image_url": menu.get("image_url", ""),
                "category_id": menu.get("category_id"),
                "status": menu.get("status", ""),
                "search_score": menu.get("search_score", 0)
            }
            cleaned_results.append(cleaned_menu)
        
        # 응답 구성
        return {
            "intent_type": IntentType.SEARCH,
            "confidence": intent_data.get("confidence", 0.8 if search_results else 0.6),
            "search_query": search_query,
            "raw_text": text,
            "screen_state": ScreenState.SEARCH,
            #"search_results": cleaned_results,  # 정리된 검색 결과 사용
            "data": {
                "pre_text": text,
                "post_text": intent_data.get("post_text", text),
                "reply": reply,
                "status": ResponseStatus.SEARCH_RESULTS if search_results else ResponseStatus.UNKNOWN,
                "language": language,
                "session_id": session.get("id", ""),
                "cart": session.get("cart", []),
                "contents": cleaned_results,  # 정리된 검색 결과 사용
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