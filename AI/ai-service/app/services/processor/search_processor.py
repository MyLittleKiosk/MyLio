# app/services/processor/search_processor.py
from typing import Dict, Any, List
import json

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
        attributes = intent_data.get("attributes", {})
        
        # # 특수 검색 처리
        # is_decaf_search = attributes.get("decaf", False) or self._is_decaf_search(search_query)
        # is_dairy_free_search = attributes.get("dairy_free", False) or self._is_dairy_free_search(search_query)
        
        # # 검색어 최적화
        # optimized_query = self._optimize_query(search_query, is_decaf_search, is_dairy_free_search)
        
        # LLM을 통한 쿼리 최적화
        optimized_query = self._optimize_query_with_llm(search_query)
        
        # 벡터 검색 실행
        vector_results = self.vector_db_service.search(optimized_query, store_id=store_id, k=5)
        
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

        # dairy_free 속성이 True일 경우 우유 관련 재료/옵션이 있는 메뉴 제거
        if attributes.get("dairy_free") is True:
            search_results = [
                r for r in search_results
                if not any("우유" in ing.get("name_kr", "") for ing in r.get("ingredients", []))
                and not any("milk" in ing.get("name_en", "").lower() for ing in r.get("ingredients", []))
                and not any("우유" in opt.get("option_name", "") for opt in r.get("options", []))
            ]
        
        # 응답 메시지 생성
        if search_results:
            if len(search_results) == 1:
                # 결과가 하나인 경우 상세 정보 응답
                menu = search_results[0]
                reply = self.response_service.get_response("search_single_result", language, {
                    "menu_name": menu["name_kr"],
                    "description": menu.get("description", ""),
                    "price": menu["price"]
                })
                status = ResponseStatus.SEARCH_SINGLE_RESULT
            else:
                # 여러 결과가 있는 경우 목록 응답
                reply = self.response_service.get_response("search_results", language, {
                    "query": search_query,
                    "count": len(search_results),
                    "menu_names": ", ".join([menu["name_kr"] for menu in search_results[:3]]) + \
                                 ("..." if len(search_results) > 3 else "")
                })
                status = ResponseStatus.SEARCH_RESULTS
        else:
            # 검색 결과가 없는 경우
            reply = self.response_service.get_response("no_search_results", language, {
                "query": search_query
            })
            status = ResponseStatus.UNKNOWN
        
        # 응답 구성
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
