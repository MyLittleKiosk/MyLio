/**
 * @description 옵션 상세 타입
 * @param optionDetailId 옵션 상세 아이디
 * @param optionDetailValue 옵션 상세 값
 * @param additionalPrice 추가 가격
 */
export type OptionDetail = {
  optionDetailId: number;
  optionDetailValue: string;
  additionalPrice: number;
};

/**
 * @description 옵션 타입
 * @param optionId 옵션 아이디
 * @param optionName 옵션 이름
 * @param required 필수 여부
 * @param isSelected 선택 여부
 * @param selectedId 선택된 아이디
 * @param optionDetails 옵션 상세 리스트
 * @param selected 이 속성은 사용되지 않음
 */
export type Option = {
  optionId: number;
  optionName: string;
  required: boolean;
  isSelected: boolean;
  selectedId: number | null;
  optionDetails: OptionDetail[];
  selected: boolean;
};

/**
 * @description 장바구니 아이템 타입
 * @param cartId 장바구니 아이디
 * @param menuId 메뉴 아이디
 * @param quantity 수량
 * @param name 이름
 * @param description 설명
 * @param basePrice 기본 가격
 */
export type CartItem = {
  cartId: string;
  menuId: number;
  quantity: number;
  name: string;
  description: string;
  basePrice: number;
  totalPrice: number;
  imageUrl: string;
  selectedOptions: Option[];
};

/**
 * @description 컨텐츠 아이템 타입
 * @param menuId 메뉴 아이디
 * @param quantity 수량
 * @param name 이름
 * @param description 설명
 * @param basePrice 기본 가격
 */
export type ContentItem = {
  menuId: number;
  quantity: number;
  name: string;
  description: string;
  basePrice: number;
  totalPrice: number;
  imageUrl: string;
  options: Option[];
  selectedOption: Option[];
  nutritionInfo: NutritionInfo[];
};

/**
 * @description 영양 정보 타입
 * @param nutritionId 영양 아이디
 * @param nutritionName 영양 이름
 * @param nutritionValue 영양 값
 * @param nutritionType 영양 타입
 */
export type NutritionInfo = {
  nutritionId: number;
  nutritionName: string;
  nutritionValue: number;
  nutritionType: string;
};

/**
 * @description 주문 타입
 * @param preText 전문
 * @param postText 후문
 * @param reply 답변
 * @param screenState 상태
 */
export type OrderResponse = {
  preText: string | null;
  postText: string | null;
  reply: string | null;
  storeId: number | null;
  screenState:
    | 'MAIN'
    | 'ORDER'
    | 'SEARCH'
    | 'CONFIRM'
    | 'SELECT_PAY'
    | 'PAY'
    | 'DETAIL';
  language: 'KR' | 'EN' | 'JP' | 'CN';
  sessionId: string;
  cart: CartItem[];
  contents: ContentItem[];
  payment: 'MOBILE' | 'PAY' | 'GIFT' | 'CARD' | null;
};

/**
 * @description 주문 요청 타입
 * @param text 텍스트
 * @param screenState 상태
 * @param language 언어
 * @param sessionId 세션 아이디 (null 일 경우 새로운 세션 생성)
 * @param storeId 매장 아이디 (null 일 경우 기본 매장 사용)
 * @param cart 장바구니 아이템
 * @param contents 컨텐츠 아이템
 * @param payment 결제 방법
 */
export type OrderRequest = {
  text: string | null;
  screenState:
    | 'MAIN'
    | 'ORDER'
    | 'SEARCH'
    | 'CONFIRM'
    | 'SELECT_PAY'
    | 'PAY'
    | 'DETAIL';
  language: 'KR' | 'EN' | 'JP' | 'CN';
  sessionId: string | null;
  storeId: number | null;
  cart: CartItem[];
  contents: ContentItem[];
  payment: 'MOBILE' | 'PAY' | 'GIFT' | 'CARD' | null;
};

/**
 * @description 음료 상세 타입
 * @param menuId 메뉴 아이디
 * @param quantity 수량
 * @param name 이름
 * @param description 설명
 * @param basePrice 기본 가격
 */
export type BeverageDetail = {
  menuId: number;
  quantity: number;
  name: string;
  description: string;
  basePrice: number; //원래 가격
  totalPrice: number; //옵션값이 포함된 가격
  imageUrl: string;
  options: Option[];
  selectedOption: Option[];
  nutritionInfo: NutritionInfo[];
};

/**
 * @description 음료 타입
 * @param menuId 메뉴 아이디
 * @param quantity 수량
 * @param name 이름
 * @param description 설명
 * @param basePrice 기본 가격
 */
export type Beverage = {
  menuId: number;
  quantity: number;
  name: string;
  description: string;
  basePrice: number; //원래 가격
  totalPrice: number; //옵션값이 포함된 가격
  imageUrl: string;
  options: Option[];
  selectedOption: Option[];
  nutritionInfo: NutritionInfo[];
};
