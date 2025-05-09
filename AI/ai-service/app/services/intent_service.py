# app/services/intent_service.py
from fastapi import HTTPException
from typing import Dict, Any, Optional

from app.models.schemas import IntentType
from app.services.processor.order_processor import OrderProcessor
from app.services.processor.search_processor import SearchProcessor
from app.services.processor.payment_processor import PaymentProcessor
from app.services.menu_service import MenuService
from app.services.response_service import ResponseService
from app.services.redis_session_manager import RedisSessionManager
from app.services.processor.detail_processor import DetailProcessor

class IntentService:
    """Few-shot 기반 의도 인식 서비스"""
    
    def __init__(self, api_key: str, menu_service: MenuService, response_service: ResponseService, session_manager: RedisSessionManager):
        """서비스 초기화"""
        self.menu_service = menu_service
        self.response_service = response_service
        self.session_manager = session_manager
        
        # 프로세서 초기화
        self.order_processor = OrderProcessor(api_key, menu_service, response_service, session_manager)
        self.search_processor = SearchProcessor(api_key, menu_service, response_service, session_manager)
        self.payment_processor = PaymentProcessor(api_key, menu_service, response_service, session_manager)
        self.detail_processor = DetailProcessor(api_key, menu_service, response_service, session_manager)

    def process_request(self, text: str, language: str, screen_state: str, store_id: int, session_id: Optional[str] = None) -> Dict[str, Any]:
        """사용자 요청 처리 메인 함수"""
        print(f"[요청 처리] 세션 ID: {session_id}, 텍스트: '{text}', 화면 상태: {screen_state}")

        # 1. 세션 확보
        session_id, session = self._ensure_session(session_id)
        
        # 장바구니 초기화: session.get() 대신 직접 접근 방식 사용
        if "cart" not in session:
            session["cart"] = []
            self.session_manager._save_session(session_id, session)
        
        # 현재 장바구니 상태 출력
        print(f"[요청 처리] 세션 ID: {session_id}, 장바구니 항목 수: {len(session.get('cart', []))}, 항목: {[item.get('name') for item in session.get('cart', [])]}")
        
        # 2. 컨텍스트 기반 옵션 선택 흐름 처리
        if session.get("last_state") and session["last_state"].get("pending_option"):
            print("[요청 처리] 이전 대화 기반 옵션 선택 흐름 진입")
            response = self.order_processor.process_option_selection(text, language, screen_state, store_id, session)
            
            # 응답 후 세션 다시 가져와서 상태 출력
            updated_session = self.session_manager.get_session(session_id)
            print(f"[요청 처리] 옵션 처리 후 장바구니: {len(updated_session.get('cart', []))}, 항목: {[item.get('name') for item in updated_session.get('cart', [])]}")
            
            self.session_manager.add_to_history(session_id, text, response)
            return response
        
        # 3. 의도 인식
        intent_data = self.order_processor.recognize_intent(text, language, screen_state, store_id, session)
        
        # 4. 의도에 따른 처리
        if intent_data["intent_type"] == IntentType.ORDER:
            response = self.order_processor.process(intent_data, text, language, screen_state, store_id, session)
        elif intent_data["intent_type"] == IntentType.SEARCH:
            response = self.search_processor.process(intent_data, text, language, screen_state, store_id, session)
        elif intent_data["intent_type"] == IntentType.PAYMENT:
            response = self.payment_processor.process(intent_data, text, language, screen_state, store_id, session)
        elif intent_data["intent_type"] == IntentType.DETAIL:
            response = self.detail_processor.process(intent_data, text, language, screen_state, store_id, session)
        else:
            response = self.order_processor.process_unknown(text, language, screen_state, store_id, session)
        
        # 프로세서 처리 후 세션 다시 가져와서 상태 출력
        updated_session = self.session_manager.get_session(session_id)
        print(f"[요청 처리] 프로세서 처리 후 장바구니: {len(updated_session.get('cart', []))}, 항목: {[item.get('name') for item in updated_session.get('cart', [])]}")
        
        # 응답에 장바구니 보강 - 세션에서 최신 장바구니 정보를 가져와 응답에 추가
        if "data" in response and "cart" in response["data"]:
            response["data"]["cart"] = updated_session.get("cart", [])
            print(f"[응답 보강] 최종 장바구니 항목 수: {len(response['data']['cart'])}")
        
        # 5. 대화 기록 저장
        self.session_manager.add_to_history(session_id, text, response)
        
        return response
    
    def _ensure_session(self, session_id: Optional[str]) -> tuple:
        """세션 확보 및 검증"""
        if not session_id:
            # 세션 ID가 없으면 새로 생성
            session_id = self.session_manager.create_session()
            print(f"[요청 처리] 새 세션 생성: {session_id}")
        else:
            # 기존 세션이 없으면 외부 ID로 생성
            if not self.session_manager.get_session(session_id):
                self.session_manager.create_session_with_id(session_id)
        
        # 세션 가져오기
        session = self.session_manager.get_session(session_id)
        
        if not session:
            raise HTTPException(status_code=500, detail="세션 생성 실패")
        
        if not isinstance(session, dict):
            raise HTTPException(status_code=500, detail="세션 정보가 유효하지 않습니다.")
            
        return session_id, session