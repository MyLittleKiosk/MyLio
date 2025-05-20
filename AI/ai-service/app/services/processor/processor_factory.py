# app/services/processor/processor_factory.py
from typing import Dict, Any, Optional
from app.models.schemas import IntentType
from app.services.processor.order_processor import OrderProcessor
from app.services.processor.search_processor import SearchProcessor
from app.services.processor.payment_processor import PaymentProcessor
from app.services.processor.detail_processor import DetailProcessor
from app.services.processor.unknown_processor import UnknownProcessor
from app.services.processor.cart_modify_processor import CartModifyProcessor
from app.models.schemas import ResponseStatus

class ProcessorFactory:
    """프로세서 팩토리"""
    
    def __init__(self, order_processor: OrderProcessor, search_processor: SearchProcessor,
                 payment_processor: PaymentProcessor, detail_processor: DetailProcessor,
                 unknown_processor: UnknownProcessor, cart_modify_processor: CartModifyProcessor = None):
        """팩토리 초기화"""
        self.processors = {
            IntentType.ORDER: order_processor,
            IntentType.SEARCH: search_processor,
            IntentType.PAYMENT: payment_processor,
            IntentType.DETAIL: detail_processor,
            IntentType.OPTION_SELECT: order_processor,  
            IntentType.UNKNOWN: unknown_processor,
            IntentType.CART_MODIFY: cart_modify_processor if cart_modify_processor else unknown_processor
        }
    
    def get_processor(self, intent_type: IntentType):
        """의도 유형에 맞는 프로세서 반환"""
        if intent_type not in self.processors:
            return self.processors[IntentType.UNKNOWN]
        return self.processors[intent_type]