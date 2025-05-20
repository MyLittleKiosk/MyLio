# app/services/processor/unknown_processor.py
from typing import Dict, Any
from app.models.schemas import IntentType, ResponseStatus
from app.services.processor.base_processor import BaseProcessor
from app.services.response.response_generator import ResponseGenerator
from app.models.schemas import ResponseStatus

class UnknownProcessor(BaseProcessor):
    """알 수 없는 의도 처리 프로세서"""
    
    def __init__(self, response_generator: ResponseGenerator, menu_service, session_manager):
        """프로세서 초기화"""
        self.response_generator = response_generator
        self.menu_service = menu_service
        self.session_manager = session_manager
    
    def process(self, intent_data: Dict[str, Any], text: str, language: str, screen_state: str, store_id: int, session: Dict[str, Any]) -> Dict[str, Any]:
        """알 수 없는 의도 처리"""
        context = {
            "status": ResponseStatus.UNKNOWN,
            "screen_state": screen_state
        }
        
        reply = intent_data.get("reply") or self.response_generator.generate_response(
            intent_data, language, context
        )
        
        return {
            "intent_type": IntentType.UNKNOWN,
            "confidence": intent_data.get("confidence", 0.3),
            "raw_text": text,
            "screen_state": screen_state,
            "data": {
                "pre_text": text,
                "post_text": intent_data.get("post_text", text),
                "reply": reply,
                "status": ResponseStatus.UNKNOWN,
                "language": language,
                "session_id": session.get("id", ""),
                "cart": session.get("cart", []),
                "contents": [],
                "store_id": store_id
            }
        }