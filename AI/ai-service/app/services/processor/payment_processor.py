# app/services/processor/payment_processor.py
from typing import Dict, Any, Optional, List
import json
import re
from datetime import datetime

from app.models.schemas import IntentType, ScreenState, Language, ResponseStatus
from app.services.processor.base_processor import BaseProcessor
from app.services.response.response_generator import ResponseGenerator
from app.models.schemas import ResponseStatus
class PaymentProcessor(BaseProcessor):
    """결제 처리 프로세서"""
    
    def __init__(self, response_generator: ResponseGenerator, menu_service, session_manager):
        """프로세서 초기화"""
        self.response_generator = response_generator
        self.menu_service = menu_service
        self.session_manager = session_manager
    
    def process(self, intent_data: Dict[str, Any], text: str, language: str, screen_state: str, store_id: int, session: Dict[str, Any]) -> Dict[str, Any]:
        """결제 의도 처리"""
        # 모든 화면 상태에서 취소 요청인지 먼저 확인
        if self._is_cancel_request(text, language):
            return self._process_cancel_request(text, language, screen_state, store_id, session)
        
        # CONFIRM 화면에서는 메뉴 보기 요청도 취소로 처리
        if screen_state == ScreenState.CONFIRM and self._is_view_menu_request(text, language):
            return self._process_cancel_request(text, language, screen_state, store_id, session)
        
        # SELECT_PAY 또는 PAY 화면에서 메뉴 보기 요청인지 확인
        if screen_state in [ScreenState.SELECT_PAY, ScreenState.PAY] and self._is_view_menu_request(text, language):
            return self._process_view_menu_request(text, language, screen_state, store_id, session)
        
        # 화면 상태에 따른 일반 처리
        if screen_state == ScreenState.MAIN or screen_state == ScreenState.ORDER:
            return self._process_payment_request(intent_data, text, language, screen_state, store_id, session)
        
        elif screen_state == ScreenState.CONFIRM:
            return self._process_payment_confirmation(intent_data, text, language, screen_state, store_id, session)
        
        elif screen_state == ScreenState.SELECT_PAY:
            return self._process_payment_method_selection(intent_data, text, language, screen_state, store_id, session)
        
        elif screen_state == ScreenState.PAY:
            return self._process_payment_completion(intent_data, text, language, screen_state, store_id, session)
        
        else:
            # 기타 상태에서의 기본 응답
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
    
    def _is_cancel_request(self, text: str, language: str) -> bool:
        """취소 요청인지 확인"""
        text_lower = text.lower()
        
        # 한국어 취소 키워드
        if language == Language.KR:
            cancel_keywords = ["취소", "그만", "안할래", "안 할래", "안해", "안 해", "멈춰", "중단", "결제 취소"]
            return any(keyword in text_lower for keyword in cancel_keywords)
        
        # 영어 취소 키워드
        elif language == Language.EN:
            cancel_keywords = ["cancel", "stop", "abort", "nevermind", "never mind", "don't", "do not", "quit"]
            return any(keyword in text_lower for keyword in cancel_keywords)
        
        return False
    
    def _is_view_menu_request(self, text: str, language: str) -> bool:
        """메뉴 보기 요청인지 확인"""
        text_lower = text.lower()
        
        # 한국어 메뉴 보기 키워드
        if language == Language.KR:
            menu_keywords = ["메뉴", "다른 메뉴", "메뉴 보여줘", "메뉴 볼래", "다른거", "다른 거", "다른 것", "주문 변경"]
            return any(keyword in text_lower for keyword in menu_keywords)
        
        # 영어 메뉴 보기 키워드
        elif language == Language.EN:
            menu_keywords = ["menu", "other menu", "show menu", "see menu", "something else", "change order"]
            return any(keyword in text_lower for keyword in menu_keywords)
        
        return False
    
    def _process_cancel_request(self, text: str, language: str, screen_state: str, store_id: int, session: Dict[str, Any]) -> Dict[str, Any]:
        """취소 요청 처리"""
        # 현재 화면 상태에 따른 다른 취소 메시지
        context = {
            "status": ResponseStatus.UNKNOWN,
            "screen_state": ScreenState.MAIN
        }
        
        # 의도 데이터 구성
        intent_data = {
            "intent_type": IntentType.PAYMENT,
            "confidence": 0.9
        }
        
        # 화면 상태에 따른 응답 컨텍스트 구성
        if screen_state == ScreenState.CONFIRM:
            context["cancel_type"] = "order"
        elif screen_state == ScreenState.SELECT_PAY:
            context["cancel_type"] = "payment_selection"
        elif screen_state == ScreenState.PAY:
            context["cancel_type"] = "payment_processing"
        else:
            context["cancel_type"] = "order"
        
        # 응답 생성
        reply = self.response_generator.generate_response(intent_data, language, context)
        
        return {
            "intent_type": IntentType.PAYMENT,
            "confidence": 0.9,
            "raw_text": text,
            "screen_state": ScreenState.MAIN,  # 메인 화면으로 돌아감
            "data": {
                "pre_text": text,
                "post_text": text,
                "reply": reply,
                "status": ResponseStatus.UNKNOWN,
                "language": language,
                "session_id": session.get("id", ""),
                "cart": session.get("cart", []),  # 장바구니는 유지
                "contents": [],
                "store_id": store_id
            }
        }
    
    def _process_view_menu_request(self, text: str, language: str, screen_state: str, store_id: int, session: Dict[str, Any]) -> Dict[str, Any]:
        """메뉴 보기 요청 처리 (SELECT_PAY, PAY 상태에서만 호출)"""
        # 결제 프로세스 중 메뉴 보기 요청이면 주문 취소 안내
        context = {
            "status": ResponseStatus.UNKNOWN,
            "screen_state": ScreenState.MAIN,
            "cancel_type": "order_for_menu"
        }
        
        # 의도 데이터 구성
        intent_data = {
            "intent_type": IntentType.PAYMENT,
            "confidence": 0.9
        }
        
        # 응답 생성
        reply = self.response_generator.generate_response(intent_data, language, context)
        
        return {
            "intent_type": IntentType.PAYMENT,
            "confidence": 0.9,
            "raw_text": text,
            "screen_state": ScreenState.MAIN,  # 메인 화면으로 돌아감
            "data": {
                "pre_text": text,
                "post_text": text,
                "reply": reply,
                "status": ResponseStatus.UNKNOWN,
                "language": language,
                "session_id": session.get("id", ""),
                "cart": session.get("cart", []),  # 장바구니는 유지
                "contents": [],
                "store_id": store_id
            }
        }
    
    def _process_payment_request(self, intent_data: Dict[str, Any], text: str, language: str, screen_state: str, store_id: int, session: Dict[str, Any]) -> Dict[str, Any]:
        """결제 요청 처리 (MAIN/ORDER -> CONFIRM)"""
        # 장바구니에 물건이 있는지 확인
        cart = session.get("cart", [])
        session_id = session.get("id","")

        if not cart:
            # 장바구니가 비어있는 경우
            context = {
                "status": ResponseStatus.UNKNOWN,
                "screen_state": screen_state,
                "cart_status": "empty"
            }
            # 언어에 따른 응답 생성
            if language == Language.KR:
                reply = "장바구니가 비어 있어요. 먼저 메뉴를 선택해주세요."
            elif language == Language.EN:
                reply = "Your cart is empty. Please select menu items first."
            elif language == Language.JP:
                reply = "カートが空です。まずメニューを選択してください。"
            elif language == Language.CN:
                reply = "购物车是空的。请先选择菜单。"
            else:
                reply = intent_data.get("reply") or self.response_generator.generate_response(
                    intent_data, language, context
                )

            return {
                "intent_type": IntentType.PAYMENT,
                "confidence": intent_data.get("confidence", 0.7),
                "raw_text": text,
                "screen_state": screen_state,  # 화면 유지
                "data": {
                    "pre_text": text,
                    "post_text": intent_data.get("post_text", text),
                    "reply": reply,
                    "status": ResponseStatus.UNKNOWN,
                    "language": language,
                    "session_id": session.get("id", ""),
                    "cart": cart,
                    "contents": [],
                    "store_id": store_id
                }
            }
        else:
            # 결제 확인 화면으로 이동
            # 장바구니 총액 계산
            total_amount = sum(item.get("total_price", 0) * item.get("quantity",1) for item in cart)

            # 언어에 따른 장바구니 확인 요청 메시지 생성
            if language == Language.KR:
                cart_items = ", ".join([f"{item.get('name')} {item.get('quantity')}개" for item in cart[:3]])
                if len(cart) > 3:
                    cart_items += f" 외 {len(cart) - 3}개"
                reply = f"장바구니에 {cart_items}가 있어요. 총 금액은 {total_amount}원이에요. 결제를 진행할까요?"
            elif language == Language.EN:
                cart_items = ", ".join([f"{item.get('quantity')} {item.get('name_en') or item.get('name')}" for item in cart[:3]])
                if len(cart) > 3:
                    cart_items += f" and {len(cart) - 3} more items"
                reply = f"Your cart contains {cart_items}. Total amount is {total_amount} won. Would you like to proceed with payment?"
            elif language == Language.JP:
                cart_items = ", ".join([f"{item.get('name')} {item.get('quantity')}個" for item in cart[:3]])
                if len(cart) > 3:
                    cart_items += f" 他 {len(cart) - 3}個"
                reply = f"カートに{cart_items}があります。合計金額は{total_amount}ウォンです。お支払いを続けますか？"
            elif language == Language.CN:
                cart_items = ", ".join([f"{item.get('name')} {item.get('quantity')}个" for item in cart[:3]])
                if len(cart) > 3:
                    cart_items += f" 等 {len(cart) - 3}个"
                reply = f"购物车中有{cart_items}。总金额为{total_amount}韩元。您要继续付款吗？"
            else:
                # 컨텍스트 구성
                context = {
                    "status": ResponseStatus.PAYMENT_CONFIRM,
                    "screen_state": ScreenState.CONFIRM,
                    "total_amount": total_amount,
                    "cart": cart
                }
                
                # 응답 생성
                reply = intent_data.get("reply") or self.response_generator.generate_response(
                    intent_data, language, context
                )
            # 결제 수단이 선택되어있는지 확인
            payment_method = self.session_manager.get_session_value(session_id,
                                                        "payment_method")
            return {
                "intent_type": IntentType.PAYMENT,
                "confidence": intent_data.get("confidence", 0.8),
                "raw_text": text,
                "screen_state": ScreenState.CONFIRM,  # 결제 확인 화면으로 변경
                "payment_method" : payment_method,
                "data": {
                    "pre_text": text,
                    "post_text": intent_data.get("post_text", text),
                    "reply": reply,
                    "status": ResponseStatus.PAYMENT_CONFIRM,
                    "language": language,
                    "session_id": session.get("id", ""),
                    "cart": cart,
                    "total_amount": total_amount,
                    "store_id": store_id
                }
            }
    
    def _process_payment_confirmation(self, intent_data: Dict[str, Any], text: str, language: str, screen_state: str, store_id: int, session: Dict[str, Any]) -> Dict[str, Any]:
        """결제 확인 처리 (CONFIRM -> SELECT_PAY)"""
        # 확인 의도 판단
        confirmation = self._is_confirmation(text, language)
        session_id = session.get("id", "")
        if not confirmation:
            # 확인하지 않은 경우 (취소 또는 불명확한 응답)
            context = {
                "status": ResponseStatus.UNKNOWN,
                "screen_state": ScreenState.MAIN,
                "cancel_type": "payment"
            }
            reply = intent_data.get("reply") or self.response_generator.generate_response(
                intent_data, language, context
            )
            return {
                "intent_type": IntentType.PAYMENT,
                "confidence": intent_data.get("confidence", 0.7),
                "raw_text": text,
                "screen_state": ScreenState.MAIN,  # 메인 화면으로 돌아감
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
        
        # 결제 수단이 선택되어있는지 확인
        payment_method = self.session_manager.get_session_value(session_id,
                                                        "payment_method")

        if payment_method:
            return {
                "intent_type": IntentType.PAYMENT,
                "confidence": intent_data.get("confidence", 0.9),
                "raw_text": text,
                "screen_state": ScreenState.PAY,  # 결제 수단 선택 화면으로 변경
                "payment_method" : payment_method,
                "data": {
                    "pre_text": text,
                    "post_text": intent_data.get("post_text", text),
                    "reply": "결제가 진행중이에요.",
                    "status": ResponseStatus.PAYMENT_CONFIRM,  # 상태도 일관되게 변경
                    "language": language,
                    "session_id": session.get("id", ""),
                    "cart": session.get("cart", []),
                    "store_id": store_id,
                    "total_amount": sum(item.get("total_price", 0) for item in session.get("cart", []))
                }
            }

        # 결제 수단 선택 화면으로 이동
        context = {
            "status": ResponseStatus.SELECT_PAYMENT,  # 상태를 SELECT_PAYMENT로 변경
            "screen_state": ScreenState.SELECT_PAY
        }
        
        # 응답 생성 (intent_data의 reply가 있으면 사용, 없으면 생성)
        reply = intent_data.get("reply")
        if not reply:
            if language == Language.KR:
                reply = "결제 방법을 선택해주세요."
            elif language == Language.EN:
                reply = "Please select your payment method."
            elif language == Language.JP:
                reply = "お支払い方法を選択してください。"
            elif language == Language.CN:
                reply = "请选择支付方式。"
            else:
                reply = self.response_generator.generate_response(intent_data, language, context)
        
        return {
            "intent_type": IntentType.PAYMENT,
            "confidence": intent_data.get("confidence", 0.9),
            "raw_text": text,
            "screen_state": ScreenState.SELECT_PAY,  # 결제 수단 선택 화면으로 변경
            "data": {
                "pre_text": text,
                "post_text": intent_data.get("post_text", text),
                "reply": reply,
                "status": ResponseStatus.SELECT_PAYMENT,  # 상태도 일관되게 변경
                "language": language,
                "session_id": session.get("id", ""),
                "cart": session.get("cart", []),
                "store_id": store_id,
                "total_amount": sum(item.get("total_price", 0) for item in session.get("cart", []))
            }
        }
    
    def _process_payment_method_selection(self, intent_data: Dict[str, Any], text: str, language: str, screen_state: str, store_id: int, session: Dict[str, Any]) -> Dict[str, Any]:
        """결제 수단 선택 처리 (SELECT_PAY -> PAY)"""
        # 결제 수단 파악
        payment_method = intent_data.get("payment_method") or self._detect_payment_method(text, language)
        
        if not payment_method:
            # 인식할 수 없는 결제 수단
            context = {
                "status": ResponseStatus.UNKNOWN,
                "screen_state": ScreenState.SELECT_PAY,
                "error_type": "payment_method_unknown"
            }
            reply = intent_data.get("reply") or self.response_generator.generate_response(
                intent_data, language, context
            )
            return {
                "intent_type": IntentType.PAYMENT,
                "confidence": intent_data.get("confidence", 0.6),
                "raw_text": text,
                "screen_state": ScreenState.SELECT_PAY,  # 화면 유지
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
        
        # 표준화된 결제 수단 ID와 이름 획득
        payment_method_id = "PAY"  # 기본값
        payment_method_name = "카카오페이" if language == Language.KR else "Kakao Pay"  # 기본값
        
        # payment_method가 문자열인 경우와 딕셔너리인 경우 처리
        if isinstance(payment_method, dict):
            payment_method_id = payment_method.get("id", "PAY")
            payment_method_name = payment_method.get("name", "카카오페이") if language == Language.KR else payment_method.get("name_en", "Kakao Pay")
        elif isinstance(payment_method, str):
            # 문자열인 경우 ID로 사용하고 이름 조회
            payment_method_id = payment_method.upper()
            if payment_method_id == "KAKAOPAY":
                payment_method_id = "PAY"  # KAKAOPAY를 PAY로 표준화
            payment_method_name = self._get_payment_method_name(payment_method_id, language)
        
        # 결제 진행 화면으로 이동
        context = {
            "status": ResponseStatus.PAYMENT_CONFIRM,
            "screen_state": ScreenState.PAY,
            "payment_method": payment_method_name
        }
        reply = intent_data.get("reply") or self.response_generator.generate_response(
            intent_data, language, context
        )
        
        # 세션에 결제 정보 저장
        if "payment_info" not in session:
            session["payment_info"] = {}
        
        session["payment_info"]["method"] = payment_method_id  # 표준화된 ID 저장
        session["payment_info"]["amount"] = sum(item.get("total_price", 0) for item in session.get("cart", []))
        session["payment_info"]["timestamp"] = datetime.now().isoformat()
        
        # 세션 업데이트
        self.session_manager.update_session(session["id"], session)
        
        return {
            "intent_type": IntentType.PAYMENT,
            "confidence": intent_data.get("confidence", 0.95),
            "payment_method": payment_method_id,  # 표준화된 ID 반환
            "raw_text": text,
            "screen_state": ScreenState.PAY,  # 결제 진행 화면으로 변경
            "data": {
                "pre_text": text,
                "post_text": intent_data.get("post_text", text),
                "reply": reply,
                "status": ResponseStatus.PAYMENT_CONFIRM,
                "language": language,
                "session_id": session.get("id", ""),
                "cart": session.get("cart", []),
                "store_id": store_id
            }
        }
    
    def _process_payment_completion(self, intent_data: Dict[str, Any], text: str, language: str, screen_state: str, store_id: int, session: Dict[str, Any]) -> Dict[str, Any]:
        """결제 완료 처리 (PAY -> MAIN)"""
        # 결제 처리 로직
        payment_successful = True  # 가상 결제 처리 (실제로는 결제 모듈 연동 필요)
        
        if not payment_successful:
            # 결제 실패 (가상)
            context = {
                "status": ResponseStatus.PAYMENT_FAILED,
                "screen_state": ScreenState.SELECT_PAY
            }
            reply = intent_data.get("reply") or self.response_generator.generate_response(
                intent_data, language, context
            )
            return {
                "intent_type": IntentType.PAYMENT,
                "confidence": intent_data.get("confidence", 0.9),
                "raw_text": text,
                "screen_state": ScreenState.SELECT_PAY,  # 결제 수단 선택 화면으로 돌아감
                "data": {
                    "pre_text": text,
                    "post_text": intent_data.get("post_text", text),
                    "reply": reply,
                    "status": ResponseStatus.PAYMENT_FAILED,
                    "language": language,
                    "session_id": session.get("id", ""),
                    "cart": session.get("cart", []),
                    "contents": [],
                    "store_id": store_id
                }
            }
            
        # 결제 성공
        payment_method = session.get("payment_info", {}).get("method", "CARD")
        payment_method_name = self._get_payment_method_name(payment_method, language)
        
        context = {
            "status": ResponseStatus.PAYMENT_SUCCESS,
            "screen_state": ScreenState.MAIN,
            "payment_method": payment_method_name
        }
        reply = intent_data.get("reply") or self.response_generator.generate_response(
            intent_data, language, context
        )
        
        # 주문 정보 생성
        cart = session.get("cart", [])
        order_number = self._generate_order_number()
        order_info = {
            "order_number": order_number,
            "payment_method": payment_method,
            "total_amount": session.get("payment_info", {}).get("amount", 0),
            "items": cart,
            "timestamp": datetime.now().isoformat()
        }
        
        # 장바구니 비우기
        self.session_manager.clear_cart(session["id"])
        
        # 세션에 주문 기록 추가
        if "orders" not in session:
            session["orders"] = []
        
        session["orders"].append(order_info)
        self.session_manager.update_session(session["id"], session)
        
        return {
            "intent_type": IntentType.PAYMENT,
            "confidence": intent_data.get("confidence", 0.95),
            "payment_method": payment_method,
            "raw_text": text,
            "screen_state": ScreenState.MAIN,  # 메인 화면으로 돌아감
            "data": {
                "pre_text": text,
                "post_text": intent_data.get("post_text", text),
                "reply": reply,
                "status": ResponseStatus.PAYMENT_SUCCESS,
                "language": language,
                "session_id": session.get("id", ""),
                "cart": [],  # 장바구니 비움
                "contents": [order_info],  # 주문 정보
                "order_number": order_number,
                "store_id": store_id
            }
        }
    
    def _is_confirmation(self, text: str, language: str) -> bool:
        """사용자 응답이 확인인지 판단"""
        text_lower = text.lower()
        
        # 한국어 확인 패턴
        if language == Language.KR:
            confirm_keywords = ["네", "예", "맞아", "응", "좋아", "그래", "확인", "진행", "해줘", "결제", "맞습니다", "맞아요"]
            reject_keywords = ["아니", "취소", "돌아가", "잘못", "안돼", "안해", "다시", "싫어"]
            
            # 거절 키워드가 포함되어 있으면 취소로 판단
            if any(keyword in text_lower for keyword in reject_keywords):
                return False
            
            # 확인 키워드가 포함되어 있으면 확인으로 판단
            return any(keyword in text_lower for keyword in confirm_keywords)
        
        # 영어 확인 패턴
        elif language == Language.EN:
            confirm_keywords = ["yes", "yeah", "correct", "right", "ok", "okay", "proceed", "confirm", "sure", "yep"]
            reject_keywords = ["no", "cancel", "back", "wrong", "incorrect", "not", "don't", "stop"]
            
            if any(keyword in text_lower for keyword in reject_keywords):
                return False
            
            return any(keyword in text_lower for keyword in confirm_keywords)
        
        # 기타 언어는 일단 기본값으로 처리
        return True
    
    def _detect_payment_method(self, text: str, language: str) -> Optional[Dict[str, str]]:
        """텍스트에서 결제 수단 감지"""
        text_lower = text.lower()
        
        # 업데이트된 결제 수단 매핑
        payment_methods = {
            "CARD": {
                "id": "CARD",
                "name": "신용카드",
                "name_en": "Card",
                "keywords_kr": ["카드", "신용", "체크", "결제", "신용카드", "체크카드", "카드로"],
                "keywords_en": ["card", "credit", "debit", "visa", "master", "credit card"]
            },
            "MOBILE": {
                "id": "MOBILE",
                "name": "모바일 상품권",
                "name_en": "Mobile",
                "keywords_kr": ["모바일", "상품권", "모바일 상품권", "핸드폰", "스마트폰"],
                "keywords_en": ["mobile", "voucher", "mobile voucher", "phone"]
            },
            "GIFT": {
                "id": "GIFT",
                "name": "기프트 카드",
                "name_en": "Gift Card",
                "keywords_kr": ["기프트", "기프트 카드", "선물", "선물 카드","기프트 카드"],
                "keywords_en": ["gift", "gift card", "present"]
            },
            "PAY": {
                "id": "PAY",
                "name": "카카오페이",
                "name_en": "Kakao Pay",
                "keywords_kr": ["카카오", "카카오페이", "카톡", "카톡페이", "페이", "간편결제", "카페이","카카오 페이"],
                "keywords_en": ["kakao", "kakaopay", "kakao pay", "pay"]
            }
        }
        
        # 직접 카카오페이 체크 (정확한 매칭을 위해) - 항상 PAY 반환
        if "카카오페이" in text_lower or "kakaopay" in text_lower:
            return {
                "id": "PAY",  # 항상 PAY로 표준화
                "name": "카카오페이",
                "name_en": "Kakao Pay"
            }
        
        # 언어에 따라 키워드 선택
        keyword_key = "keywords_kr" if language == Language.KR else "keywords_en"
        
        # 각 결제 수단에 대해 확인
        for method_id, method_info in payment_methods.items():
            keywords = method_info[keyword_key]
            if any(keyword in text_lower for keyword in keywords):
                return {
                    "id": method_id,
                    "name": method_info["name"],
                    "name_en": method_info["name_en"]
                }
        
        # PAYMENT 의도로 인식되었지만 결제 수단이 명확하지 않은 경우
        # 기본값으로 "PAY" 반환 (요구사항에 맞게)
        if "결제" in text_lower or "pay" in text_lower:
            return {
                "id": "PAY",
                "name": "카카오페이",
                "name_en": "Kakao Pay"
            }
        
        # 감지된 결제 수단이 없는 경우
        return None
    
    def _get_payment_method_name(self, method_id: str, language: str) -> str:
        """결제 수단 ID에 해당하는 이름 반환"""
        payment_method_names = {
            "CARD": {"kr": "신용카드", "en": "Card"},
            "MOBILE": {"kr": "모바일 상품권", "en": "Mobile"},
            "GIFT": {"kr": "기프트 카드", "en": "Gift Card"},
            "PAY": {"kr": "카카오페이", "en": "Kakao Pay"}
        }
        
        # 대문자로 표준화
        method_id = method_id.upper()
        
        # KAKAOPAY는 PAY로 표준화
        if method_id == "KAKAOPAY":
            method_id = "PAY"
        
        lang_key = "kr" if language == Language.KR else "en"
        return payment_method_names.get(method_id, {}).get(lang_key, method_id)
    
    def _generate_order_number(self) -> str:
        """주문 번호 생성"""
        import random
        from datetime import datetime
        
        prefix = "ORD"
        timestamp = datetime.now().strftime("%Y%m%d%H%M")
        random_suffix = str(random.randint(1000, 9999))
        
        return f"{prefix}-{timestamp}-{random_suffix}"