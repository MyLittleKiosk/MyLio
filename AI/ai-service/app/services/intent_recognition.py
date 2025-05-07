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
        print(f"RAG 결과 처리: {rag_result}")  # 디버깅 로그 추가
        
        # rag_result에서 이미 메뉴 정보가 설정되어 있는지 확인
        recognized_menus = rag_result.get("recognized_menus", [])
        
        # 메뉴 정보가 있지만 menu_id가 없는 경우에만 추가 검색 수행
        processed_menus = []
        for menu_data in recognized_menus:
            # 이미 menu_id가 있는 경우 그대로 사용
            if "menu_id" in menu_data:
                processed_menus.append(menu_data)
                continue
            
            menu_name = menu_data.get("menu_name", "")
            if not menu_name:
                continue
            
            # 벡터 DB에서 메뉴 검색
            menu_search_results = self.rag_service.vector_store.search_menu(menu_name, store_id, top_k=1)
            
            if menu_search_results:
                # 검색된 메뉴 정보
                menu_info = menu_search_results[0]
                
                # 기본 메뉴 정보
                enriched_menu = {
                    "menu_id": menu_info.get("id"),
                    "quantity": menu_data.get("quantity", 1),
                    "name": menu_info.get("name_kr", menu_name),
                    "name_en": menu_info.get("name_en", ""),
                    "description": menu_info.get("description", ""),
                    "base_price": menu_info.get("price", 0),
                    "total_price": menu_info.get("price", 0),
                    "image_url": menu_info.get("image_url", ""),
                    "options": menu_data.get("options", [])  # 원래 옵션 정보 유지
                }
                
                processed_menus.append(enriched_menu)
        
        print(f"처리된 메뉴 결과: {processed_menus}")  # 디버깅 로그 추가
        
        # 응답 구성
        return {
            "intent_type": "ORDER",
            "raw_text": rag_result.get("raw_text", ""),
            "screen_state": rag_result.get("screen_state", ""),
            "recognized_menus": processed_menus,  # 중요: recognized_menus 필드에 직접 설정
            "success": True,
            "data": {
                "pre_text": rag_result.get("raw_text", ""),
                "post_text": rag_result.get("raw_text", ""),
                "reply": f"{len(processed_menus)}개의 메뉴를 주문하셨습니다.",
                "status": "ORDER",
                "language": rag_result.get("language", "ko"),
                "session_id": "",
                "cart": [],
                "contents": processed_menus,  # 여기도 processed_menus 사용
                "store_id": store_id
            },
            "error": None,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }