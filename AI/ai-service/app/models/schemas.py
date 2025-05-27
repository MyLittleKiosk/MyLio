# app/models/schemas.py
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from enum import Enum

class ScreenState(str, Enum):
    """화면 상태 정의"""
    MAIN = "MAIN"              # 메인 화면 (메뉴 목록 표시)
    SEARCH = "SEARCH"          # 검색 화면
    DETAIL = "DETAIL"          # 메뉴 상세 화면
    ORDER = "ORDER"            # 주문 화면 (옵션 선택)
    CONFIRM = "CONFIRM"        # 주문 확인 화면
    SELECT_PAY = "SELECT_PAY"  # 결제 수단 선택 화면
    PAY = "PAY"                # 결제 진행 화면

class IntentType(str, Enum):
    """사용자 의도 타입 정의"""
    ORDER = "ORDER"            # 주문 의도
    SEARCH = "SEARCH"          # 검색 의도
    OPTION_SELECT = "OPTION_SELECT"  # 옵션 선택 의도
    PAYMENT = "PAYMENT"        # 결제 의도
    CONFIRM = "CONFIRM"        # 확인 의도
    DETAIL = "DETAIL"          # 메뉴 영양 성분 조회
    CART_MODIFY = "CART_MODIFY"  # 장바구니 수정 의도
    UNKNOWN = "UNKNOWN"        # 알 수 없는 의도
    CART_VIEW = "CART_VIEW"

class Language(str, Enum):
    """지원 언어 정의"""
    KR = "KR"  # 한국어
    EN = "EN"  # 영어
    JP = "JP"  # 일본어
    CN = "CN"  # 중국어

class VoiceInputRequest(BaseModel):
    """음성 입력 요청 모델"""
    text: str
    language: Language = Language.KR
    screen_state: ScreenState
    store_id: int
    session_id: Optional[str] = None

    class Config:
        extra = "ignore"  # 모델에 없는 추가 필드는 무시
        
class ResponseStatus(str, Enum):
    """응답 상태 정의"""
    CORRECTED = "CORRECTED"                  # 메뉴명 교정됨
    MISSING_REQUIRED_OPTIONS = "MISSING_REQUIRED_OPTIONS"  # 필수 옵션 누락
    READY_TO_ADD_CART = "READY_TO_ADD_CART"  # 장바구니 추가 가능
    RECOMMENDATION = "RECOMMENDATION"         # 추천 메뉴
    SEARCH_RESULTS = "SEARCH_RESULTS"        # 검색 결과
    PAYMENT_CONFIRM = "PAYMENT_CONFIRM"       # 결제 확인
    SELECT_PAYMENT = "SELECT_PAYMENT"         # 결제 수단 선택
    PAYMENT_SUCCESS = "PAYMENT_SUCCESS"       # 결제 완료
    PAYMENT_FAILED = "PAYMENT_FAILED"         # 결제 실패
    DETAIL = "DETAIL"          # 메뉴 영양 성분 조회
    CART_CLEARED = "CART_CLEARED"             # 장바구니 비움
    ITEM_REMOVED = "ITEM_REMOVED"             # 장바구니 항목 삭제
    QUANTITY_UPDATED = "QUANTITY_UPDATED"     # 장바구니 항목 수량 변경
    OPTIONS_UPDATED = "OPTIONS_UPDATED"       # 장바구니 항목 옵션 변경
    UNKNOWN = "UNKNOWN"                       # 알 수 없음
    CART_VIEWED = "CART_VIEWED"    # 장바구니 보여줌
    
class VoiceInputResponse(BaseModel):
    """음성 입력 응답 모델"""
    intent_type: IntentType
    confidence: float = Field(0.0, ge=0.0, le=1.0)
    search_query: Optional[str] = None
    payment_method: Optional[str] = None
    raw_text: str
    screen_state: ScreenState
    search_results: Optional[List[Dict[str, Any]]] = None
    data: Dict[str, Any] = Field(
        default_factory=lambda: {
            "pre_text": "",
            "post_text": "",
            "reply": "",
            "status": ResponseStatus.UNKNOWN,
            "language": Language.KR,
            "session_id": "",
            "cart": [],
            "contents": [],
            "store_id": 0
        }
    )

# app/models/schemas.py에 추가

class RecognizedMenu(BaseModel):
    """인식된 메뉴 정보 모델"""
    menu_id: int
    quantity: int
    name: str
    name_en: Optional[str]
    description: Optional[str]
    base_price: int
    total_price: int
    image_url: Optional[str]
    options: List[Dict[str, Any]]
    selected_options: List[Dict[str, Any]]
    is_corrected: bool
    original_name: Optional[str]

class FormattedVoiceInputResponse(BaseModel):
    """포맷팅된 음성 입력 응답 모델"""
    intent_type: IntentType
    confidence: float = Field(0.0, ge=0.0, le=1.0)
    recognized_menus: List[RecognizedMenu] = []
    pre_text: str
    post_text: str
    reply: str
    search_query: Optional[str] = None
    payment_method: Optional[str] = None
    raw_text: str
    screen_state: ScreenState
    search_results: Optional[List[Dict[str, Any]]] = None