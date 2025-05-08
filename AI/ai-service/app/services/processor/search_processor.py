# app/services/processor/search_processor.py
from typing import Dict, Any, Optional, List
import json
import re

from app.models.schemas import IntentType, ScreenState, Language, ResponseStatus
from app.services.processor.base_processor import BaseProcessor

class SearchProcessor(BaseProcessor):
    """검색 처리 프로세서"""
    
    def process(self, intent_data: Dict[str, Any], text: str, language: str, screen_state: str, store_id: int, session: Dict[str, Any]) -> Dict[str, Any]:
        """검색 의도 처리"""
        # 임시 구현
        search_query = intent_data.get("search_query", text)
        
        # 검색 결과 (임시)
        search_results = []
        store_menus = self.menu_service.get_store_menus(store_id)
        
        for menu_id, menu in store_menus.items():
            if search_query.lower() in menu["name_kr"].lower() or (menu["name_en"] and search_query.lower() in menu["name_en"].lower()):
                search_results.append(menu)
        
        # 응답 메시지
        if search_results:
            reply = self.response_service.get_response("search_results", language, {
                "query": search_query,
                "count": len(search_results)
            })
            status = ResponseStatus.SEARCH_RESULTS
        else:
            reply = self.response_service.get_response("no_search_results", language, {
                "query": search_query
            })
            status = ResponseStatus.UNKNOWN
        
        # 응답 구성
        return {
            "intent_type": IntentType.SEARCH,
            "confidence": 0.7,
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
    
    def _get_prompt_template(self):
        """검색 의도 인식을 위한 프롬프트 템플릿"""
        # 기본적으로 베이스 프로세서의 프롬프트 템플릿을 사용하되, 검색 관련 부분 강화 가능
        return super()._get_prompt_template()
    
    def _load_examples(self):
        """검색 관련 Few-shot 학습 예제"""
        return {
            "search": [
                {
                    "input": "커피 메뉴 알려주세요",
                    "output": {
                        "intent_type": "SEARCH",
                        "search_query": "커피"
                    }
                },
                {
                    "input": "아메리카노 종류가 뭐가 있나요?",
                    "output": {
                        "intent_type": "SEARCH",
                        "search_query": "아메리카노"
                    }
                },
                {
                    "input": "라떼 메뉴 좀 보여주세요",
                    "output": {
                        "intent_type": "SEARCH",
                        "search_query": "라떼"
                    }
                }
            ]
        }
    
    def _select_examples(self, screen_state, language):
        """화면 상태에 맞는 Few-shot 예제 선택"""
        examples = []
        
        # 검색 화면에서는 검색 예제 중점적으로 제공
        if screen_state == ScreenState.SEARCH:
            examples.extend(self.examples["search"])
        else:
            # 다른 화면에서는 기본 검색 예제 제공
            examples.append(self.examples["search"][0])
        
        # 예제 포맷팅
        formatted_examples = []
        for example in examples:
            example_text = f"사용자: \"{example['input']}\"\n"
            example_text += f"분석 결과: ```json\n{json.dumps(example['output'], ensure_ascii=False, indent=2)}\n```"
            formatted_examples.append(example_text)
        
        return "\n\n".join(formatted_examples)