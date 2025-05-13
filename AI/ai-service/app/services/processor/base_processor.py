# app/services/processor/base_processor.py
from typing import Dict, Any, Optional
from app.models.schemas import ResponseStatus, ScreenState

class BaseProcessor:
    """기본 프로세서 클래스"""
    
    def process(self, intent_data: Dict[str, Any], text: str, language: str, screen_state: str, store_id: int, session: Dict[str, Any]) -> Dict[str, Any]:
        """의도 처리 메인 함수"""
        raise NotImplementedError("이 메서드는 하위 클래스에서 구현해야 합니다.")
    
    def _build_response(self, intent_data: Dict[str, Any], text: str, language: str, screen_state: str, store_id: int, session: Dict[str, Any], status: ResponseStatus, contents: Any = None, reply: str = "") -> Dict[str, Any]:
        """응답 객체 구성"""
        response = {
            "intent_type": intent_data["intent_type"],
            "confidence": intent_data.get("confidence", 0.5),
            "raw_text": text,
            "screen_state": screen_state,
            "data": {
                "pre_text": text,
                "post_text": intent_data.get("post_text", text),
                "reply": reply,
                "status": status,
                "language": language,
                "session_id": session.get("id", ""),
                "cart": session.get("cart", []),
                "contents": contents if contents is not None else [],
                "store_id": store_id
            }
        }
        
        # 의도별 추가 필드
        if intent_data.get("intent_type") == "SEARCH" and "search_query" in intent_data:
            response["search_query"] = intent_data["search_query"]
        
        if intent_data.get("intent_type") == "PAYMENT" and "payment_method" in intent_data:
            response["payment_method"] = intent_data["payment_method"]
        
        return response