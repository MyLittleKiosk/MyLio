#  app/services/processor/payment_processor.py (CONFIRM 화면 처리 수정)
from typing import Dict, Any, Optional, List
import json
import re
from datetime import datetime

from app.models.schemas import IntentType, ScreenState, Language, ResponseStatus
from app.services.processor.base_processor import BaseProcessor

class PaymentProcessor(BaseProcessor):
    """결제 처리 프로세서"""
    
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
        if screen_state == ScreenState.CONFIRM:
            reply = self.response_service.get_response("order_canceled", language, {})
        elif screen_state == ScreenState.SELECT_PAY:
            reply = self.response_service.get_response("payment_selection_canceled", language, {})
        elif screen_state == ScreenState.PAY:
            reply = self.response_service.get_response("payment_processing_canceled", language, {})
        else:
            reply = self.response_service.get_response("order_canceled", language, {})
        
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
        reply = self.response_service.get_response("order_canceled_for_menu", language, {})
        
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
            # 장바구니 총액 계산
            total_amount = sum(item.get("total_price", 0) for item in cart)
            
            reply = self.response_service.get_response("confirm_order", language, {
                "total_amount": total_amount
            })
            
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
                    #"contents": cart,
                    "total_amount": total_amount,
                    "store_id": store_id
                }
            }
    
    def _process_payment_confirmation(self, intent_data: Dict[str, Any], text: str, language: str, screen_state: str, store_id: int, session: Dict[str, Any]) -> Dict[str, Any]:
        """결제 확인 처리 (CONFIRM -> SELECT_PAY)"""
        # 확인 의도 판단
        confirmation = self._is_confirmation(text, language)
        
        if not confirmation:
            # 확인하지 않은 경우 (취소 또는 불명확한 응답)
            reply = self.response_service.get_response("payment_canceled", language, {})
            return {
                "intent_type": IntentType.PAYMENT,
                "confidence": 0.7,
                "raw_text": text,
                "screen_state": ScreenState.MAIN,  # 메인 화면으로 돌아감
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
        
        # 결제 수단 선택 화면으로 이동
        reply = self.response_service.get_response("select_payment", language, {})
        
        # 결제 수단 목록 
        # payment_methods = [
        #     {"id": "CARD", "name": "신용카드", "name_en": "Card"},
        #     {"id": "MOBILE", "name": "모바일 상품권", "name_en": "Mobile"},
        #     {"id": "GIFT", "name": "기프트 카드", "name_en": "Gift Card"},
        #     {"id": "PAY", "name": "카카오페이", "name_en": "Kakao"}
        # ]
        
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
                #"contents": payment_methods,  # 결제 수단 목록
                "store_id": store_id,
                "total_amount": sum(item.get("total_price", 0) for item in session.get("cart", []))
            }
        }
    
    def _process_payment_method_selection(self, intent_data: Dict[str, Any], text: str, language: str, screen_state: str, store_id: int, session: Dict[str, Any]) -> Dict[str, Any]:
        """결제 수단 선택 처리 (SELECT_PAY -> PAY)"""
        # 결제 수단 파악
        payment_method = self._detect_payment_method(text, language)
        
        if not payment_method:
            # 인식할 수 없는 결제 수단
            reply = self.response_service.get_response("payment_method_unknown", language, {})
            return {
                "intent_type": IntentType.PAYMENT,
                "confidence": 0.6,
                "raw_text": text,
                "screen_state": ScreenState.SELECT_PAY,  # 화면 유지
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
        
        # 결제 진행 화면으로 이동
        reply = self.response_service.get_response("processing_payment", language, {
            "payment_method": payment_method["name"] if language == Language.KR else payment_method["name_en"]
        })
        
        # 세션에 결제 정보 저장
        if "payment_info" not in session:
            session["payment_info"] = {}
        
        session["payment_info"]["method"] = payment_method["id"]
        session["payment_info"]["amount"] = sum(item.get("total_price", 0) for item in session.get("cart", []))
        session["payment_info"]["timestamp"] = datetime.now().isoformat()
        
        # 세션 업데이트
        self.session_manager.update_session(session["id"], session)
        
        return {
            "intent_type": IntentType.PAYMENT,
            "confidence": 0.95,
            "payment_method": payment_method["id"],
            "raw_text": text,
            "screen_state": ScreenState.PAY,  # 결제 진행 화면으로 변경
            "data": {
                "pre_text": text,
                "post_text": text,
                "reply": reply,
                "status": ResponseStatus.PAYMENT_CONFIRM,
                "language": language,
                "session_id": session.get("id", ""),
                "cart": session.get("cart", []),
                #"contents": [payment_method],  # 선택된 결제 수단
                #"payment_info": session["payment_info"],
                "store_id": store_id
            }
        }
    
    def _process_payment_completion(self, intent_data: Dict[str, Any], text: str, language: str, screen_state: str, store_id: int, session: Dict[str, Any]) -> Dict[str, Any]:
        """결제 완료 처리 (PAY -> MAIN)"""
        # 결제 처리 로직
        payment_successful = True  # 가상 결제 처리 (실제로는 결제 모듈 연동 필요)
        
        if not payment_successful:
            # 결제 실패 (가상)
            reply = self.response_service.get_response("payment_failed", language, {})
            return {
                "intent_type": IntentType.PAYMENT,
                "confidence": 0.9,
                "raw_text": text,
                "screen_state": ScreenState.SELECT_PAY,  # 결제 수단 선택 화면으로 돌아감
                "data": {
                    "pre_text": text,
                    "post_text": text,
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
        
        reply = self.response_service.get_response("payment_success", language, {
            "payment_method": payment_method_name
        })
        
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
            "confidence": 0.95,
            "payment_method": payment_method,
            "raw_text": text,
            "screen_state": ScreenState.MAIN,  # 메인 화면으로 돌아감
            "data": {
                "pre_text": text,
                "post_text": text,
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
                "keywords_kr": ["기프트", "기프트 카드", "선물", "선물 카드"],
                "keywords_en": ["gift", "gift card", "present"]
            },
            "PAY": {
                "id": "PAY",
                "name": "카카오페이",
                "name_en": "Kakao",
                "keywords_kr": ["카카오", "카카오페이", "카톡", "카톡페이", "페이"],
                "keywords_en": ["kakao", "kakaopay", "kakao pay", "pay"]
            }
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
        
        # 감지된 결제 수단이 없는 경우
        return None
    
    def _get_payment_method_name(self, method_id: str, language: str) -> str:
        """결제 수단 ID에 해당하는 이름 반환"""
        payment_method_names = {
            "CARD": {"kr": "신용카드", "en": "Card"},
            "MOBILE": {"kr": "모바일 상품권", "en": "Mobile"},
            "GIFT": {"kr": "기프트 카드", "en": "Gift Card"},
            "PAY": {"kr": "카카오페이", "en": "Kakao"}
        }
        
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
    
    def _get_prompt_template(self):
        """프롬프트 템플릿 정의"""
        from langchain.prompts import PromptTemplate
        
        template = """
        당신은 카페 키오스크의 음성 인식 시스템입니다. 사용자의 발화를 분석하고 정확한 의도를 파악해야 합니다.

        ### 현재 상황:
        - 화면 상태: {screen_state}
        - 언어: {language}
        - 이전 대화 기록: {history}

        ### 컨텍스트 정보:
        {context}

        ### 결제 의도 인식 예제:
        {examples}

        ### 사용자 발화:
        "{text}"

        사용자의 발화가 결제 관련 의도인지 판단하세요. 만약 결제 의도라면, 어떤 결제 방식을 선택했는지 파악하세요.

        JSON 형식으로 응답하세요:
        ```json
        {
          "intent_type": "PAYMENT",
          "payment_method": "CARD" 또는 다른 결제 방식,
          "confidence": 0.9
        }
        ```
        """
        
        return PromptTemplate(
            input_variables=["screen_state", "language", "context", "history", "examples", "text"],
            template=template
        )
    
    def _load_examples(self):
        """결제 관련 Few-shot 학습 예제"""
        return {
            "payment": [
                {
                    "input": "결제할게요",
                    "output": {
                        "intent_type": "PAYMENT",
                        "confidence": 0.9
                    }
                },
                {
                    "input": "카드로 결제할게요",
                    "output": {
                        "intent_type": "PAYMENT",
                        "payment_method": "CARD",
                        "confidence": 0.95
                    }
                },
                {
                    "input": "카카오페이로 결제할게요",
                    "output": {
                        "intent_type": "PAYMENT",
                        "payment_method": "PAY",
                        "confidence": 0.95
                    }
                },
                {
                    "input": "모바일 상품권으로 결제할게요",
                    "output": {
                        "intent_type": "PAYMENT",
                        "payment_method": "MOBILE",
                        "confidence": 0.95
                    }
                },
                {
                    "input": "기프트 카드로 결제할게요",
                    "output": {
                        "intent_type": "PAYMENT",
                        "payment_method": "GIFT",
                        "confidence": 0.95
                    }
                },
                {
                    "input": "결제 진행해주세요",
                    "output": {
                        "intent_type": "PAYMENT",
                        "confidence": 0.9
                    }
                },
                {
                    "input": "네, 결제할게요",
                    "output": {
                        "intent_type": "PAYMENT",
                        "confidence": 0.9
                    }
                }
            ]
        }
    
    def _select_examples(self, screen_state, language):
        """화면 상태에 맞는 Few-shot 예제 선택"""
        examples = []
        
        # 화면 상태에 따라 다른 예제 제공
        if screen_state == ScreenState.MAIN or screen_state == ScreenState.ORDER:
            # 결제 시작 관련 예제
            examples.append(self.examples["payment"][0])  # "결제할게요"
            examples.append(self.examples["payment"][5])  # "결제 진행해주세요"
        
        elif screen_state == ScreenState.CONFIRM:
            # 결제 확인 관련 예제
            examples.append(self.examples["payment"][6])  # "네, 결제할게요"
        
        elif screen_state == ScreenState.SELECT_PAY:
            # 결제 수단 선택 관련 예제
            examples.append(self.examples["payment"][1])  # 카드
            examples.append(self.examples["payment"][2])  # 카카오페이
            examples.append(self.examples["payment"][3])  # 모바일 상품권
            examples.append(self.examples["payment"][4])  # 기프트 카드
        
        else:
            # 기본 예제
            examples.append(self.examples["payment"][0])
        
        # 예제 포맷팅
        formatted_examples = []
        for example in examples:
            formatted_examples.append(f"사용자: \"{example['input']}\"\n분석 결과: ```json\n{json.dumps(example['output'], ensure_ascii=False, indent=2)}\n```")
        
        return "\n\n".join(formatted_examples)