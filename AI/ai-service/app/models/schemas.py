"""
schemas.py
API 모델 스키마
"""

from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class IntentType(str, Enum):
    ORDER = "ORDER"
    SEARCH = "SEARCH"
    OPTION_SELECT = "OPTION_SELECT"
    QUESTION = "QUESTION"
    CART = "CART"
    PAYMENT = "PAYMENT"
    CANCEL = "CANCEL"
    UNKNOWN = "UNKNOWN"

class RecognizedOption(BaseModel):
    option_name: str
    option_value: str

class RecognizedMenu(BaseModel):
    menu_name: str
    quantity: int = 1
    options: List[RecognizedOption] = []

class VoiceInputRequest(BaseModel):
    text: str
    language: str = "ko"
    screen_state: str
    store_id: int

class VoiceInputResponse(BaseModel):
    intent_type: str
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    recognized_menus: List[Dict[str, Any]] = []
    search_query: Optional[str] = None
    payment_method: Optional[str] = None
    raw_text: str
    screen_state: str
    search_results: Optional[List[Dict[str, Any]]] = None

class ResponseGenerationRequest(BaseModel):
    status: str
    menus: List[Dict[str, Any]] = []
    raw_text: str
    screen_state: str

class ResponseGenerationResponse(BaseModel):
    response: str