# app/services/processor/search_processor.py
from typing import Dict, Any, List
import json
import re

from app.models.schemas import IntentType, ScreenState, Language, ResponseStatus
from app.services.processor.base_processor import BaseProcessor
from app.services.vector_db_service import VectorDBService

class SearchProcessor(BaseProcessor):
    """RAG 기반 검색 처리 프로세서"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
            decaf_results = []
            
            # 벡터 검색 결과에서 디카페인 메뉴 찾기
            for menu in search_results:
                # 디카페인 관련 메뉴 확인
                has_decaf_name = ("디카페인" in menu.get("name_kr", "").lower() or 
                                "decaf" in menu.get("name_en", "").lower())
                has_decaf_desc = ("디카페인" in menu.get("description", "").lower() or 
                                "decaf" in menu.get("description", "").lower())
                has_decaf_tag = any("디카페인" in tag.get("tag_kr", "").lower() or 
                                "decaf" in tag.get("tag_en", "").lower() 
                                for tag in menu.get("tags", []))
                
                if has_decaf_name or has_decaf_desc or has_decaf_tag:
                    decaf_results.append(menu)
            
            # 디카페인 메뉴가 있으면 결과 대체
            if decaf_results:
                search_results = decaf_results
            # 벡터 검색으로 디카페인 메뉴가 없으면 직접 검색
            elif not decaf_results and category_ids:
                store_menus = self.menu_service.get_store_menus(store_id)
                for menu_id, menu in store_menus.items():
                    # 카테고리 필터링
                    if menu.get("category_id") not in category_ids:
                        continue
                    
                    # 디카페인 관련 메뉴 확인
                    has_decaf = (
                        "디카페인" in menu.get("name_kr", "").lower() or 
                        "decaf" in menu.get("name_en", "").lower() or
                        "디카페인" in menu.get("description", "").lower() or
                        any("디카페인" in tag.get("tag_kr", "").lower() for tag in menu.get("tags", []))
                    )
                    
                    if has_decaf:
                        menu_copy = menu.copy()
                        menu_copy["search_score"] = 1.0  # 직접 필터링은 높은 점수 부여
                        decaf_results.append(menu_copy)
                
                # 직접 검색 결과가 있으면 사용
                if decaf_results:
                    search_results = decaf_results
        
        # dairy_free 속성이 True일 경우 우유 관련 재료/옵션이 있는 메뉴 제거 (기존 코드)
        if attributes.get("dairy_free") is True:
            search_results = [
                r for r in search_results
                if not any("우유" in ing.get("name_kr", "") for ing in r.get("ingredients", []))
                and not any("milk" in ing.get("name_en", "").lower() for ing in r.get("ingredients", []))
                and not any("우유" in opt.get("option_name", "") for opt in r.get("options", []))
            ]
        
        # 응답 메시지 생성 (기존 코드와 동일)
        if search_results:
            if len(search_results) == 1:
                menu = search_results[0]
                reply = self.response_service.get_response("search_single_result", language, {
                    "menu_name": menu["name_kr"],
                    "description": menu.get("description", ""),
                    "price": menu["price"]
                })
                status = ResponseStatus.SEARCH_RESULTS  
            else:
                reply = self.response_service.get_response("search_results", language, {
                    "query": search_query,
                    "count": len(search_results),
                    "menu_names": ", ".join([menu["name_kr"] for menu in search_results[:3]]) + \
                                ("..." if len(search_results) > 3 else "")
                })
                status = ResponseStatus.SEARCH_RESULTS
        else:
            reply = self.response_service.get_response("no_search_results", language, {
                "query": search_query
            })
            status = ResponseStatus.UNKNOWN
        
        # 디카페인 검색이지만 결과가 없는 경우 특별 메시지
        if is_decaf_search and not search_results:
            reply = "죄송합니다. 현재 디카페인 음료 메뉴가 없습니다."
        
        # 응답 구성 (기존 코드와 동일)
        return {
            "intent_type": IntentType.SEARCH,
            "confidence": 0.8 if search_results else 0.6,
            "search_query": search_query,
            "raw_text": text,
            "screen_state": ScreenState.SEARCH,
            "search_results": search_results,
            "data": {
                "pre_text": text,
                "post_text": text,
                "reply": reply,
                "status": status,
                "language": language,
                "session_id": session.get("id", ""),
                "cart": session.get("cart", []),
                "contents": search_results,
                "store_id": store_id
            }
        }
    
    import re  # 상단에 이미 있다면 생략 가능

    def _optimize_query_with_llm(self, query: str) -> str:
        """LLM을 사용한 검색 쿼리 최적화"""
        # LLM 프롬프트 구성
        prompt = f"""
        다음은 카페 메뉴를 검색하는 사용자의 질문입니다:
        "{query}"

        당신은 카페 키오스크의 메뉴 검색 시스템입니다. 카페에는 커피(아메리카노, 라떼, 에스프레소 등), 차, 스무디, 디저트 등의 메뉴가 있습니다.

        이 질문에서 중요한 키워드를 추출하고, 다음 속성에 대한 검색 의도가 있는지 판단해주세요:
        1. 디카페인 여부: "디카페인", "카페인 없는", "카페인 제거" 등의 표현이 있는지
        2. 우유/유제품 포함 여부: "우유 없는", "비건", "락토스", "유당", "알레르기" 등의 표현이 있는지
        3. 계절 한정 메뉴 여부: "계절", "시즌", "한정", "신메뉴" 등의 표현이 있는지
        4. 칼로리/다이어트 관련 여부: "저칼로리", "다이어트", "건강한" 등의 표현이 있는지
        5. 기타 중요 속성: 온도(아이스, 핫), 사이즈(크기), 맛(달달한, 쓴맛) 등

        결과를 다음 JSON 형식으로 반환해주세요:
        ```json
        {{
        "keywords": ["핵심 키워드1", "핵심 키워드2", ...],
        "attributes": {{
            "decaf": true/false,
            "dairy_free": true/false,
            "seasonal": true/false,
            "low_calorie": true/false,
            "other": ["기타 속성1", "기타 속성2", ...]
        }},
        "optimized_query": "검색에 최적화된 쿼리"
        }}
        ```

        optimized_query는 벡터 검색에 사용될 최적화된 문자열로, 관련 키워드를 포함해야 합니다.

        JSON만 출력하세요.
        """

        try:
            # LLM 호출
            response = self.llm.predict(prompt)

            # 마크다운 블록 제거
            response_clean = re.sub(r"^```json\s*", "", response.strip())
            response_clean = re.sub(r"\s*```$", "", response_clean)

            # JSON 응답 파싱
            result = json.loads(response_clean)

            return result["optimized_query"]
        
        except Exception as e:
            print(f"LLM 응답 파싱 오류: {e}")
            print(f"원본 응답: {response if 'response' in locals() else 'N/A'}")

            # 오류 발생 시 기존 규칙 기반 최적화
            is_decaf = self._is_decaf_search(query)
            is_dairy_free = self._is_dairy_free_search(query)

            optimized = query.lower().strip()
            if is_decaf and "디카페인" not in optimized:
                optimized += " 디카페인"
            if is_dairy_free and "우유 없는" not in optimized:
                optimized += " 우유 없는 음료"

            return optimized

    
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
    

    def _load_examples(self):
        """검색 관련 Few-shot 예제"""
        return {
            "search": [
                {
                    "input": "커피 뭐 있어?",
                    "output": {
                        "intent_type": "SEARCH",
                        "search_query": "커피",
                        "attributes": {
                            "decaf": False,
                            "dairy_free": False,
                            "seasonal": False,
                            "low_calorie": False,
                            "other": []
                        },
                        "optimized_query": "커피 메뉴"
                    }
                },
                {
                    "input": "디카페인 메뉴 있어?",
                    "output": {
                        "intent_type": "SEARCH",
                        "search_query": "디카페인",
                        "attributes": {
                            "decaf": True,
                            "dairy_free": False,
                            "seasonal": False,
                            "low_calorie": False,
                            "other": []
                        },
                        "optimized_query": "디카페인 커피"
                    }
                },
                {
                    "input": "나 우유 못 먹어, 우유 없는 음료 있어?",
                    "output": {
                        "intent_type": "SEARCH",
                        "search_query": "우유 없는",
                        "attributes": {
                            "decaf": False,
                            "dairy_free": True,
                            "seasonal": False,
                            "low_calorie": False,
                            "other": ["알레르기"]
                        },
                        "optimized_query": "비건 음료 유제품 없는 메뉴"
                    }
                },
                {
                    "input": "새로 나온 시즌 메뉴 뭐야?",
                    "output": {
                        "intent_type": "SEARCH",
                        "search_query": "시즌 메뉴",
                        "attributes": {
                            "decaf": False,
                            "dairy_free": False,
                            "seasonal": True,
                            "low_calorie": False,
                            "other": ["신메뉴"]
                        },
                        "optimized_query": "계절 한정 신메뉴"
                    }
                },
                {
                    "input": "건강한 메뉴나 저칼로리 음료 추천해줘",
                    "output": {
                        "intent_type": "SEARCH",
                        "search_query": "건강한 저칼로리",
                        "attributes": {
                            "decaf": False,
                            "dairy_free": False,
                            "seasonal": False,
                            "low_calorie": True,
                            "other": ["건강"]
                        },
                        "optimized_query": "저칼로리 건강 음료"
                    }
                }
            ],
            "order": [],
            "option": [],
            "payment": []
        }
    
    def _analyze_query_with_llm(self, query: str) -> Dict[str, Any]:
        """LLM을 사용한 쿼리 분석 및 최적화"""
        # LLM 프롬프트 구성
        prompt = f"""
        다음은 카페 메뉴를 검색하는 사용자의 질문입니다:
        "{query}"

        당신은 카페 키오스크의 메뉴 검색 시스템입니다. 카페에는 다음과 같은 메뉴 카테고리가 있습니다:
        1. 커피 - 아메리카노, 라떼, 에스프레소 등
        2. 음료 - 차, 스무디, 에이드 등
        3. 디저트 - 케이크, 브라우니, 쿠키 등

        이 질문에서 중요한 키워드를 추출하고, 다음 속성에 대한 검색 의도가 있는지 판단해주세요:
        1. 디카페인 여부: "디카페인", "카페인 없는", "카페인 제거" 등의 표현이 있는지
        2. 음료 종류 구분: 사용자가 원하는 것이 음료인지, 디저트인지, 아니면 모든 메뉴인지 구분
        3. 우유/유제품 포함 여부: "우유 없는", "비건", "락토스", "유당", "알레르기" 등의 표현이 있는지
        4. 계절 한정 메뉴 여부: "계절", "시즌", "한정", "신메뉴" 등의 표현이 있는지
        5. 칼로리/다이어트 관련 여부: "저칼로리", "다이어트", "건강한" 등의 표현이 있는지
        6. 기타 중요 속성: 온도(아이스, 핫), 사이즈(크기), 맛(달달한, 쓴맛) 등

        결과를 다음 JSON 형식으로 반환해주세요:
        ```json
        {{
        "keywords": ["핵심 키워드1", "핵심 키워드2", ...],
        "attributes": {{
            "decaf": true/false,
            "item_type": "beverage"/"dessert"/"all",
            "dairy_free": true/false,
            "seasonal": true/false,
            "low_calorie": true/false,
            "other": ["기타 속성1", "기타 속성2", ...]
        }},
        "optimized_query": "검색에 최적화된 쿼리"
        }}
        ```

        item_type은 사용자가 찾는 항목 유형으로, "beverage"는 음료(커피, 차, 스무디 등), "dessert"는 디저트(케이크, 쿠키 등), "all"은 모든 메뉴를 의미합니다.

        optimized_query는 벡터 검색에 사용될 최적화된 문자열로, 관련 키워드를 포함해야 합니다.

        JSON만 출력하세요.
        """

        try:
            # LLM 호출
            response = self.llm.predict(prompt)

            # 마크다운 블록 제거
            response_clean = re.sub(r"^```json\s*", "", response.strip())
            response_clean = re.sub(r"\s*```$", "", response_clean)

            # JSON 응답 파싱
            result = json.loads(response_clean)

            # "디카페인" 키워드가 포함된 경우 강제로 음료 타입으로 설정
            if "디카페인" in query.lower() or "decaf" in query.lower():
                result["attributes"]["decaf"] = True
                result["attributes"]["item_type"] = "beverage"  # 디카페인은 항상 음료 카테고리
                
                # 최적화된 쿼리에 "음료" 또는 "커피" 키워드 추가
                if "음료" not in result["optimized_query"].lower() and "커피" not in result["optimized_query"].lower():
                    result["optimized_query"] = "디카페인 커피 음료 " + result["optimized_query"]
            
            return result
        
        except Exception as e:
            print(f"LLM 응답 파싱 오류: {e}")
            print(f"원본 응답: {response if 'response' in locals() else 'N/A'}")

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