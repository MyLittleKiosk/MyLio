# schema.py 대화 상태 관리
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from enum import Enum

class ConversationState(str, Enum):
    MAIN = "MAIN"           # 메인 화면
    SEARCH = "SEARCH"       # 검색 중
    DETAIL = "DETAIL"       # 메뉴 상세
    ORDER = "ORDER"         # 주문 진행 중
    CONFIRM = "CONFIRM"     # 주문 확인
    CART = "CART"           # 장바구니
    PAYMENT = "PAYMENT"     # 결제

class Language(str, Enum):
    KR = "kr"
    EN = "en"
    JA = "ja"  # 일본어 추가
    CN = "cn"  # 중국어 추가
    ES = "es"  # 스페인어 추가
    FR = "fr"  # 프랑스어 추가

class OptionDetail(BaseModel):
    """옵션 상세 정보"""
    id: int
    value: str
    display_name: str
    additional_price: int = 0

class Option(BaseModel):
    """메뉴 옵션 정보"""
    id: int
    name: str
    required: bool = False
    details: List[OptionDetail] = []
    selected_detail_id: Optional[int] = None

class MenuItem(BaseModel):
    """메뉴 기본 정보"""
    id: int
    name: str
    price: int
    options: List[Option] = []

class CurrentOrder(BaseModel):
    """현재 진행 중인 주문"""
    menu_id: Optional[int] = None
    menu_name: Optional[str] = None
    base_price: int = 0
    quantity: int = 1
    options: Dict[str, Dict[str, Any]] = {}  # 선택한 옵션들 -> {key: {value, display_name, additional_price}}
    required_options: List[Option] = []  # 필수 옵션 목록
    missing_options: List[str] = []  # 아직 선택해야 할 옵션
    total_price: int = 0  # 총 가격 (옵션 포함)

class CartItem(BaseModel):
    menuId: int
    menuName: str
    temperature: Optional[str] = None  # 추가: 온도 옵션
    size: Optional[str] = None  # 추가: 사이즈 옵션
    decaf: bool = False  # 추가: 디카페인 여부
    quantity: int = 1
    price: int = 0  # 수정: 총 가격 (옵션 포함)
    base_price: int = 0  # 추가: 기본 가격
    options: Dict[str, Dict[str, Any]] = {}  # 추가 옵션들 -> {key: {value, display_name, additional_price}}
    need: List[str] = []  # 아직 필요한 옵션들

    def calculate_total(self) -> int:
        """옵션 포함 총 가격 계산"""
        option_price = sum(opt.get('additional_price', 0) for opt in self.options.values())
        self.price = (self.base_price + option_price) * self.quantity
        return self.price
    
    def get_display_name(self, lang: str, store_meta: Dict[str, Any] = None) -> str:
        """매장의 실제 옵션 표시값으로 아이템 이름 생성"""
        name = self.menuName
        
        if lang == "kr":
            # 온도 표시
            if self.temperature:
                # 매장 매핑이 있는 경우 사용
                if store_meta and "option_mappings" in store_meta:
                    temp_mappings = store_meta["option_mappings"].get("온도", [])
                    display_temp = self.temperature
                    for mapping in temp_mappings:
                        if mapping["original"] == self.temperature:
                            display_temp = mapping.get("display_kr", self.temperature)
                            break
                    name = f"{display_temp} {name}"
                else:
                    # 기본 매핑
                    temp_map = {"HOT": "따뜻한", "ICE": "차가운"}
                    name = f"{temp_map.get(self.temperature, self.temperature)} {name}"
            
            # 사이즈 표시 (매장별로 다를 수 있음)
            if self.size and store_meta and "option_mappings" in store_meta:
                size_mappings = store_meta["option_mappings"].get("사이즈", [])
                display_size = self.size
                for mapping in size_mappings:
                    if mapping["original"] == self.size:
                        display_size = mapping.get("display_kr", self.size)
                        break
                name = f"{name} ({display_size})"
            elif self.size:
                name = f"{name} ({self.size})"
            
            # 추가 옵션들 처리
            for key, option_info in self.options.items():
                if key != "size" and key != "temperature":
                    display_value = option_info.get("display_name", option_info.get("value", ""))
                    if display_value:
                        name = f"{name} {display_value}"
            
            # 수량 표시
            if self.quantity > 1:
                name = f"{name} {self.quantity}개"
            
            # 디카페인 표시
            if self.decaf:
                name = f"디카페인 {name}"
        else:
            # 영어 버전도 동일한 방식으로 처리
            if self.decaf:
                name = f"Decaf {name}"
            
            if self.temperature:
                if store_meta and "option_mappings" in store_meta:
                    temp_mappings = store_meta["option_mappings"].get("온도", [])
                    display_temp = self.temperature
                    for mapping in temp_mappings:
                        if mapping["original"] == self.temperature:
                            display_temp = mapping.get("display_en", self.temperature)
                            break
                    name = f"{display_temp} {name}"
                else:
                    temp_map = {"HOT": "Hot", "ICE": "Iced"}
                    name = f"{temp_map.get(self.temperature, self.temperature)} {name}"
            
            if self.size:
                name = f"{name} (Size: {self.size})"
            
            # 추가 옵션들 처리
            for key, option_info in self.options.items():
                if key != "size" and key != "temperature":
                    display_value = option_info.get("display_name", option_info.get("value", ""))
                    if display_value:
                        name = f"{name} with {key.replace('_', ' ')}: {display_value}"
            
            if self.quantity > 1:
                name = f"{self.quantity}x {name}"
        
        return name
    
    def has_same_options(self, other: 'CartItem') -> bool:
        """동일한 메뉴와 옵션인지 확인"""
        if self.menuId != other.menuId:
            return False
            
        if self.temperature != other.temperature:
            return False
            
        if self.size != other.size:
            return False
            
        if self.decaf != other.decaf:
            return False
        
        # 옵션 비교 (값만 비교)
        for key, option_info in self.options.items():
            if key not in other.options:
                return False
                
            if option_info.get("value") != other.options[key].get("value"):
                return False
        
        for key in other.options:
            if key not in self.options:
                return False
        
        return True
    
    def dict(self, *args, **kwargs):
        """커스텀 딕셔너리 변환 (옵션 정보 포맷팅)"""
        result = super().dict(*args, **kwargs)
        # 옵션 정보를 더 보기 좋게 변환
        formatted_options = {}
        for key, option_info in self.options.items():
            formatted_options[key] = {
                "value": option_info.get("value", ""),
                "display_name": option_info.get("display_name", option_info.get("value", "")),
                "additional_price": option_info.get("additional_price", 0)
            }
                
        result["options"] = formatted_options
        return result

class Context(BaseModel):
    state: ConversationState = ConversationState.MAIN
    language: str = "kr"  # 수정: 더 유연한, 다국어 지원을 위한 string 타입
    cart: List[CartItem] = []
    current_order: Optional[CurrentOrder] = None  # 현재 처리 중인 주문
    last_utterance: Optional[str] = None
    session_id: str
    store_id: int
    multiple_orders: List[Dict[str, Any]] = []  # 다중 주문 처리용

class ParseReq(BaseModel):
    utterance: str
    context: Context
    return_full_meta: bool = False  # 첫 요청 시 True로 매장 전체 메타데이터 받음

class KioskResponse(BaseModel):
    text: str               # 키오스크 응답 텍스트
    next_state: ConversationState
    cart: List[CartItem]
    current_order: Optional[CurrentOrder] = None  # 현재 진행 중인 주문 상태
    suggestions: List[str] = []  # 추천 옵션들
    search_results: List[Dict[str, Any]] = []  # 검색 결과
    actions: Dict[str, Any] = {}  # UI 액션
    store_meta: Optional[Dict[str, Any]] = None  # 매장 메타데이터

class StoreMapping(BaseModel):
    """매장별 값 매핑"""
    original: str  # DB에 저장된 값
    mapped: str  # LLM이 이해하는 값
    display_kr: str  # 한글 표시용 값
    display_en: str  # 영어 표시용 값
    id: Optional[int] = None  # 추가: 옵션 상세 ID
    additional_price: int = 0  # 추가: 옵션 추가 가격

class StoreMetadata(BaseModel):
    """매장별 메타데이터"""
    store_id: int
    option_mappings: Dict[str, List[StoreMapping]]  # 옵션별 값 매핑 (이름 수정)
    size_type: str  # 'SML', 'STARBUCKS', 'CUSTOM'