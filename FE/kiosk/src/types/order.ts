/**
 * @description 옵션 상세 타입
 * @param option_detail_id 옵션 상세 아이디
 * @param option_detail_value 옵션 상세 값
 * @param additional_price 추가 가격
 */
export type OptionDetail = {
  option_detail_id: number;
  option_detail_value: string;
  additional_price: number;
};

/**
 * @description 옵션 타입
 * @param optoin_id 옵션 아이디
 * @param option_name 옵션 이름
 * @param required 필수 여부
 * @param is_selected 선택 여부
 * @param selected_id 선택된 아이디
 * @param option_details 옵션 상세 리스트
 */
export type Option = {
  optoin_id: number;
  option_name: string;
  required: boolean;
  is_selected: boolean;
  selected_id: number | null;
  option_details: OptionDetail[];
};

/**
 * @description 장바구니 아이템 타입
 * @param cart_id 장바구니 아이디
 * @param menu_id 메뉴 아이디
 * @param quantity 수량
 * @param name 이름
 * @param description 설명
 * @param base_price 기본 가격
 */
export type CartItem = {
  cart_id: number;
  menu_id: number;
  quantity: number;
  name: string;
  description: string;
  base_price: number;
  total_price: number;
  image_url: string;
  options: Option[];
};

/**
 * @description 컨텐츠 아이템 타입
 * @param menu_id 메뉴 아이디
 * @param quantity 수량
 * @param name 이름
 * @param description 설명
 * @param base_price 기본 가격
 */
export type ContentItem = {
  menu_id: number;
  quantity: number;
  name: string;
  description: string;
  base_price: number;
  total_price: number;
  image_url: string;
  options: Option[];
  selected_option: Option[];
  nutrition_info: NutritionInfo[];
};

/**
 * @description 영양 정보 타입
 * @param nutrition_id 영양 아이디
 * @param nutrition_name 영양 이름
 * @param nutrition_value 영양 값
 * @param nutrition_type 영양 타입
 */
export type NutritionInfo = {
  nutrition_id: number;
  nutrition_name: string;
  nutrition_value: number;
  nutrition_type: string;
};

/**
 * @description 주문 타입
 * @param pre_text 전문
 * @param post_text 후문
 * @param reply 답변
 * @param status 상태
 */
export type Order = {
  pre_text: string | null;
  post_text: string | null;
  reply: string | null;
  status:
    | 'MAIN'
    | 'ORDER'
    | 'SEARCH'
    | 'CONFIRM'
    | 'SELECT_PAY'
    | 'PAY'
    | 'DETAIL';
  language: string;
  session_id: string;
  cart: CartItem[];
  contents: ContentItem[];
  payment: 'MOBILE' | 'PAY' | 'GIFT' | 'CARD' | null;
};

/**
 * @description 음료 상세 타입
 * @param menu_id 메뉴 아이디
 * @param quantity 수량
 * @param name 이름
 * @param description 설명
 * @param base_price 기본 가격
 */
export type BeverageDetail = {
  menu_id: number;
  quantity: number;
  name: string;
  description: string;
  base_price: number; //원래 가격
  total_price: number; //옵션값이 포함된 가격
  image_url: string;
  options: [];
  selected_option: [];
  nutrition_info: [
    {
      nutrition_id: number;
      nutrition_name: string;
      nutrition_value: number;
      nutrition_type: string;
    },
  ];
};

/**
 * @description 음료 타입
 * @param menu_id 메뉴 아이디
 * @param quantity 수량
 * @param name 이름
 * @param description 설명
 * @param base_price 기본 가격
 */
export type Beverage = {
  menu_id: number;
  quantity: number;
  name: string;
  description: string;
  base_price: number; //원래 가격
  total_price: number; //옵션값이 포함된 가격
  image_url: string;
  options: [];
  selected_option: [];
  nutrition_info: [];
};
