# app/services/processor/payment_processor.py
from typing import Dict, Any, Optional, List
import json
import re

from app.models.schemas import IntentType, ScreenState, Language, ResponseStatus
from app.services.processor.base_processor import BaseProcessor

class PaymentProcessor(BaseProcessor):
    """결제 처리 프로세서"""
    
    def process(self, intent_data: Dict[str, Any], text: str, language: str, screen_state: str, store_id: int, session: Dict[str, Any]) -> Dict[str, Any]:
        """결제 의도 처리"""
        # 화면 상태에 따라 다른 처리
        if screen_state == ScreenState.MAIN or screen_state == ScreenState.ORDER:
            # 장바구니에 물건이 있는지 확인
            cart = session.get("cart", [])
            
            if not cart:
                # 장바구니가 비어있는 경우
                reply = self.response_service.get_response("empty_cart", language, {})
                return {
                    "intent_type": IntentType.PAYMENT,
                    "confidence": 0.7,
                    "raw_text": text,
                    "screen_state": screen_state,  # 화면 유지
                    "data": {
                        "pre_text": text,
                        "post_text": text,
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
                reply = self.response_service.get_response("confirm_order", language, {})
                return {
                    "intent_type": IntentType.PAYMENT,
                    "confidence": 0.8,
                    "raw_text": text,
                    "screen_state": ScreenState.CONFIRM,  # 결제 확인 화면으로 변경
                    "data": {
                        "pre_text": text,
                        "post_text": text,
                        "reply": reply,
                        "status": ResponseStatus.PAYMENT_CONFIRM,
                        "language": language,
                        "session_id": session.get("id", ""),
                        "cart": cart,
                        "contents": cart,
                        "store_id": store_id
                    }
                }
        
        elif screen_state == ScreenState.CONFIRM:
            # 결제 수단 선택 화면으로 이동
            reply = self.response_service.get_response("select_payment", language, {})
            return {
                "intent_type": IntentType.PAYMENT,
                "confidence": 0.9,
                "raw_text": text,
                "screen_state": ScreenState.SELECT_PAY,  # 결제 수단 선택 화면으로 변경
                "data": {
                    "pre_text": text,
                    "post_text": text,
                    "reply": reply,
                    "status": ResponseStatus.PAYMENT_CONFIRM,
                    "language": language,
                    "session_id": session.get("id", ""),
                    "cart": session.get("cart", []),
                    "contents": session.get("cart", []),
                    "store_id": store_id
                }
            }
        
        elif screen_state == ScreenState.SELECT_PAY:
            # 결제 진행 화면으로 이동
            payment_method = intent_data.get("payment_method", "card")  # 기본값: 카드
            
            # 결제 성공 가정 (실제로는 결제 처리 로직 필요)
            reply = self.response_service.get_response("payment_success", language, {})
            
            # 장바구니 비우기
            self.session_manager.clear_cart(session["id"])
            
            return {
                "intent_type": IntentType.PAYMENT,
                "confidence": 0.95,
                "payment_method": payment_method,
                "raw_text": text,
                "screen_state": ScreenState.PAY,  # 결제 진행 화면으로 변경
                "data": {
                    "pre_text": text,
                    "post_text": text,
                    "reply": reply,
                    "status": ResponseStatus.PAYMENT_SUCCESS,
                    "language": language,
                    "session_id": session.get("id", ""),
                    "cart": [],  # 장바구니 비움
                    "contents": [],
                    "store_id": store_id
                }
            }
        
        else:
            # 기타 상태에서의 기본 응답
            reply = self.response_service.get_response("unknown", language, {})
            return {
                "intent_type": IntentType.UNKNOWN,
                "confidence": 0.3,
                "raw_text": text,
                "screen_state": screen_state,
                "data": {
                    "pre_text": text,
                    "post_text": text,
                    "reply": reply,
                    "status": ResponseStatus.UNKNOWN,
                    "language": language,
                    "session_id": session.get("id", ""),
                    "cart": session.get("cart", []),
                    "contents": [],
                    "store_id": store_id
                }
            }
    
    def _get_prompt_template(self):
        """결제 의도 인식을 위한 프롬프트 템플릿"""
        # 기본적으로 베이스 프로세서의 프롬프트 템플릿을 사용하되, 결제 관련 부분 강화 가능
        return super()._get_prompt_template()
    
    def _load_examples(self):
        """결제 관련 Few-shot 학습 예제"""
        return {
            "payment": [
                {
                    "input": "결제할게요",
                    "output": {
                        "intent_type": "PAYMENT"
                    }
                },
                {
                    "input": "카드로 결제할게요",
                    "output": {
                        "intent_type": "PAYMENT",
                        "payment_method": "card"
                    }
                },
                {
                    "input": "결제 진행해주세요",
                    "output": {
                        "intent_type": "PAYMENT"
                    }
                }
            ]
        }
    
    def _select_examples(self, screen_state, language):
        """화면 상태에 맞는 Few-shot 예제 선택"""
        examples = []
        
        # 결제 관련 화면에서는 결제 예제 중점적으로 제공
        if screen_state in [ScreenState.CONFIRM, ScreenState.SELECT_PAY, ScreenState.PAY]:
            examples.extend(self.examples["payment"])
        else:
            # 다른 화면에서는 기본 결제 예제 제공
            examples.append(self.examples["payment"][0])
        
        # 예제 포맷팅
        formatted_examples = []
        for example in examples:
            example_text = f"사용자: \"{example['input']}\"\n"
            example_text += f"분석 결과: ```json\n{json.dumps(example['output'], ensure_ascii=False, indent=2)}\n```"
            formatted_examples.append(example_text)
        
        return "\n\n".join(formatted_examples)