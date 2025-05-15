# app/services/intent_service.py
from fastapi import HTTPException
from typing import Dict, Any, Optional

from app.models.schemas import IntentType, ScreenState, Language
from app.services.intent_recognizer import IntentRecognizer
from app.services.processor.processor_factory import ProcessorFactory
from app.services.processor.order_processor import OrderProcessor
from app.services.processor.search_processor import SearchProcessor
from app.services.processor.payment_processor import PaymentProcessor
from app.services.processor.detail_processor import DetailProcessor
from app.services.processor.unknown_processor import UnknownProcessor
from app.services.response.response_generator import ResponseGenerator
from app.services.menu_service import MenuService
from app.services.redis_session_manager import RedisSessionManager
from app.models.schemas import ResponseStatus

class IntentService:
    """통합 의도 인식 및 처리 서비스"""
    
    def __init__(self, api_key: str, menu_service: MenuService, response_service, session_manager: RedisSessionManager):
        """서비스 초기화"""
        self.menu_service = menu_service
        self.session_manager = session_manager
        
        # 응답 생성기 초기화
        self.response_generator = ResponseGenerator(api_key, response_service)
        
        # 의도 인식기 초기화
        self.intent_recognizer = IntentRecognizer(api_key, menu_service)
        
        # 프로세서 초기화
        self.order_processor = OrderProcessor(
            self.response_generator, 
            menu_service, 
            session_manager,
            self.intent_recognizer  # 새로운 인자 추가
        )
        
        self.search_processor = SearchProcessor(self.response_generator, menu_service, session_manager)
        self.payment_processor = PaymentProcessor(self.response_generator, menu_service, session_manager)
        self.detail_processor = DetailProcessor(self.response_generator, menu_service, session_manager)
        self.unknown_processor = UnknownProcessor(self.response_generator, menu_service, session_manager)
        
        # 프로세서 팩토리 초기화
        self.processor_factory = ProcessorFactory(
            self.order_processor,
            self.search_processor,
            self.payment_processor,
            self.detail_processor,
            self.unknown_processor
        )

    def process_request(self, text: str, language: str, screen_state: str, store_id: int, session_id: Optional[str] = None) -> Dict[str, Any]:
        """사용자 요청 처리 메인 함수"""
        try:
            # 언어 검증 및 기본값 설정 (추가)
            if language not in [Language.KR, Language.EN, Language.JP, Language.CN]:
                print(f"[요청 처리] 지원하지 않는 언어: {language}, 기본값(KR)으로 설정")
                language = Language.KR
            
            print(f"[요청 처리 시작] 세션 ID: {session_id}, 텍스트: '{text}', 화면 상태: {screen_state}, 언어: {language}")

            print(f"[요청 처리 시작] 세션 ID: {session_id}, 텍스트: '{text}', 화면 상태: {screen_state}")

            # 1. 세션 확보
            session_id, session = self._ensure_session(session_id)
            
            # 장바구니 초기화
            if "cart" not in session:
                session["cart"] = []
                self.session_manager._save_session(session_id, session)
            
            # 현재 장바구니 상태 출력
            print(f"[요청 처리] 세션 ID: {session_id}, 장바구니 항목 수: {len(session.get('cart', []))}")
            
            # "결제" 관련 키워드 직접 처리 추가
            if self._is_payment_request(text, language):
                print("[요청 처리] 결제 요청 키워드 감지, PaymentProcessor로 직접 처리")
                intent_data = {
                    "intent_type": IntentType.PAYMENT,
                    "confidence": 0.95,
                    "post_text": "결제를 진행합니다.",
                    "reply": None  # Reply는 processor에서 생성
                }
                
                response = self.payment_processor.process(intent_data, text, language, screen_state, store_id, session)
                
                # 응답 후 세션 다시 가져와서 상태 출력
                updated_session = self.session_manager.get_session(session_id)
                print(f"[요청 처리] 결제 요청 처리 후 장바구니: {len(updated_session.get('cart', []))}")
                
                # 응답에 장바구니 보강
                if "data" in response and "cart" in response["data"]:
                    response["data"]["cart"] = updated_session.get("cart", [])
                    
                # 대화 기록 저장
                self.session_manager.add_to_history(session_id, text, response)
                return response
            # CONFIRM 화면에서의 확인 응답 특별 처리
            if screen_state == ScreenState.CONFIRM and self._is_confirmation_response(text, language):
                print("[요청 처리] CONFIRM 화면에서 확인 응답 감지, PaymentProcessor로 직접 처리")
                # 직접 결제 처리기로 처리
                intent_data = {
                    "intent_type": IntentType.PAYMENT,
                    "confidence": 0.95,
                    "post_text": "결제를 진행합니다.",
                    "reply": "결제를 진행하겠습니다. 결제 방법을 선택해주세요."
                }
                
                response = self.payment_processor._process_payment_confirmation(intent_data, text, language, screen_state, store_id, session)
                
                # 응답 후 세션 다시 가져와서 상태 출력
                updated_session = self.session_manager.get_session(session_id)
                print(f"[요청 처리] 확인 응답 처리 후 장바구니: {len(updated_session.get('cart', []))}")
                
                # 응답에 장바구니 보강
                if "data" in response and "cart" in response["data"]:
                    response["data"]["cart"] = updated_session.get("cart", [])
                    
                # 대화 기록 저장
                self.session_manager.add_to_history(session_id, text, response)
                return response
            
            # 2. 컨텍스트 기반 옵션 선택 흐름 처리
            if session.get("last_state") and session["last_state"].get("pending_option"):
                print("[요청 처리] 이전 대화 기반 옵션 선택 흐름 진입")
                print(f"[요청 처리] pending_option: {session['last_state']['pending_option'].get('option_name')}")
                
                response = self.order_processor.process_option_selection(text, language, screen_state, store_id, session)
                
                # 응답 후 세션 다시 가져와서 상태 출력
                updated_session = self.session_manager.get_session(session_id)
                print(f"[요청 처리] 옵션 처리 후 장바구니: {len(updated_session.get('cart', []))}")
                
                self.session_manager.add_to_history(session_id, text, response)
                return response
            # 3. 대기열 처리 추가
            # 현재 진행 중인 주문이 없지만 대기열에 주문이 있는 경우
            elif "order_queue" in session and session["order_queue"]:
                next_menu = session["order_queue"][0]
                
                # 대기열에서 첫 번째 메뉴를 꺼내서 옵션 처리 시작
                return self._start_queued_menu_processing(next_menu, text, language, screen_state, store_id, session)
            
            # 3. 의도 인식 - 통합 의도 인식기 사용
            print("[요청 처리] 신규 의도 인식 시작")
            intent_data = self.intent_recognizer.recognize_intent(text, language, screen_state, store_id, session)
            print(f"[요청 처리] 인식된 의도: {intent_data.get('intent_type')}, 신뢰도: {intent_data.get('confidence')}")
            
            # 4. 의도에 따른 프로세서 선택 및 처리
            processor = self.processor_factory.get_processor(intent_data["intent_type"])
            print(f"[요청 처리] 선택된 프로세서: {processor.__class__.__name__}")
            
            response = processor.process(intent_data, text, language, screen_state, store_id, session)
            
            # 프로세서 처리 후 세션 다시 가져와서 상태 출력
            updated_session = self.session_manager.get_session(session_id)
            print(f"[요청 처리] 프로세서 처리 후 장바구니: {len(updated_session.get('cart', []))}")
            
            # 응답에 장바구니 보강 - 세션에서 최신 장바구니 정보를 가져와 응답에 추가
            if "data" in response and "cart" in response["data"]:
                response["data"]["cart"] = updated_session.get("cart", [])
                print(f"[응답 보강] 최종 장바구니 항목 수: {len(response['data']['cart'])}")
            
            # 5. 대화 기록 저장
            self.session_manager.add_to_history(session_id, text, response)
            
            return response
        except Exception as e:
            print(f"[요청 처리 오류] {e}")
            import traceback
            traceback.print_exc()
            
            # 오류 발생 시 안전한 응답 반환
            return {
                "intent_type": IntentType.UNKNOWN,
                "confidence": 0.3,
                "raw_text": text,
                "screen_state": screen_state,
                "data": {
                    "pre_text": text,
                    "post_text": text,
                    "reply": "처리 중 오류가 발생했습니다. 다시 시도해주세요.",
                    "status": ResponseStatus.UNKNOWN,
                    "language": language,
                    "session_id": session_id if session_id else "",
                    "cart": [],
                    "contents": [],
                    "store_id": store_id
                }
            }
    
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
    
    def _is_confirmation_response(self, text: str, language: str) -> bool:
        """주문 확인 화면에서의 확인 응답인지 판단"""
        text_lower = text.lower()
        
        # 한국어 확인 키워드
        if language == Language.KR:
            confirm_keywords = ["네", "예", "맞아", "응", "좋아", "그래", "확인", "진행", "해줘", "결제", "맞습니다", "맞아요"]
            return any(keyword in text_lower for keyword in confirm_keywords)
        
        # 영어 확인 키워드
        elif language == Language.EN:
            confirm_keywords = ["yes", "yeah", "correct", "right", "ok", "okay", "proceed", "confirm", "sure", "yep"]
            return any(keyword in text_lower for keyword in confirm_keywords)
        
        # 기타 언어는 기본값으로 처리
        return False
    
    def _is_payment_request(self, text: str, language: str) -> bool:
        """결제 요청 키워드인지 확인"""
        text_lower = text.lower()
        
        # 한국어 결제 키워드
        if language == Language.KR:
            payment_keywords = ["결제", "계산", "지불", "결제할게", "결제해줘", "계산해줘", "지불할게"]
            return any(keyword in text_lower for keyword in payment_keywords)
        
        # 영어 결제 키워드
        elif language == Language.EN:
            payment_keywords = ["pay", "payment", "checkout", "pay now", "purchase", "buy"]
            return any(keyword in text_lower for keyword in payment_keywords)
        
        # 기타 언어는 기본값으로 처리
        return False
