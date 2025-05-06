# app/response_generator.py
from .schema import ConversationState, CartItem
from typing import Dict, List, Any, Optional

class ResponseGenerator:
    def __init__(self, language: str):
        self.language = language
        self._templates = self._initialize_templates()

    def _initialize_templates(self) -> Dict[str, Dict[str, str]]:
        """한 번만 템플릿 정의 (다국어 지원)"""
        return {
            "kr": {
                # 메인 화면
                "welcome": "안녕하세요! 주문을 도와드리겠습니다.",
                "return_to_main": "메인 화면으로 돌아왔습니다.",
                
                # 주문 옵션
                "ask_option": "{menu}의 {option}은 어떻게 하시겠어요?",
                "ask_option_with_values": "{menu}의 {option}은 어떻게 하시겠어요? {values} 중에서 선택해주세요.",
                
                # 주문 완료
                "added_to_cart": "{item}을(를) 장바구니에 담았습니다. 더 주문하시겠어요?",
                "multiple_orders_processing": "{current_order_index}번째 주문 진행 중입니다. {remaining}개 주문이 남아있습니다.",
                
                # 검색
                "search_not_found": "'{keyword}'을(를) 찾을 수 없어요. 다른 메뉴를 말씀해주세요.",
                "search_results": "찾아드린 메뉴입니다. 어떤 걸로 드릴까요?",
                "search_instruction": "찾고 싶은 메뉴를 말씀해주세요.",
                
                # 장바구니
                "empty_cart": "장바구니가 비어있습니다.",
                "cart_summary": "총 주문 금액은 {total}원입니다.",
                
                # 주문 확인
                "confirm_order": "주문하신 메뉴는 다음과 같습니다. 결제를 진행하시겠어요?",
                
                # 결제
                "payment_options": "결제 방법을 선택해주세요.",
                "order_complete": "주문이 완료되었습니다. 감사합니다!",
                
                # 에러
                "default_error": "죄송합니다. 다시 시도해주세요.",
                "error": "죄송합니다. 문제가 발생했습니다.",
                "try_again": "죄송합니다. 다시 말씀해 주시겠어요?"
            },
            "en": {
                # Main screen
                "welcome": "Welcome! Let me help you with your order.",
                "return_to_main": "Returned to main menu.",
                
                # Order options
                "ask_option": "How would you like your {option} for {menu}?",
                "ask_option_with_values": "How would you like your {option} for {menu}? Please choose from {values}.",
                
                # Order complete
                "added_to_cart": "{item} added to cart. Anything else?",
                "multiple_orders_processing": "Processing order {current_order_index}. {remaining} orders remaining.",
                
                # Search
                "search_not_found": "Couldn't find '{keyword}'. Please try another item.",
                "search_results": "Here are the results. Which one would you like?",
                "search_instruction": "Please tell me what menu you're looking for.",
                
                # Cart
                "empty_cart": "Your cart is empty.",
                "cart_summary": "Total order amount is {total} won.",
                
                # Order confirmation
                "confirm_order": "Here's your order summary. Would you like to proceed to payment?",
                
                # Payment
                "payment_options": "Please select a payment method.",
                "order_complete": "Your order is complete. Thank you!",
                
                # Error
                "default_error": "Sorry, please try again.",
                "error": "Sorry, there was a problem.",
                "try_again": "Sorry, can you repeat that?"
            },
            "ja": {
                # 메인 화면
                "welcome": "いらっしゃいませ！ご注文をお伺いします。",
                "return_to_main": "メイン画面に戻りました。",
                
                # 주문 옵션
                "ask_option": "{menu}の{option}はどうなさいますか？",
                "ask_option_with_values": "{menu}の{option}はどうなさいますか？{values}から選んでください。",
                
                # 주문 완료
                "added_to_cart": "{item}をカートに追加しました。他にご注文はありますか？",
                "multiple_orders_processing": "{current_order_index}番目の注文を処理中です。残り{remaining}件の注文があります。",
                
                # 검색
                "search_not_found": "「{keyword}」が見つかりませんでした。他のメニューをお試しください。",
                "search_results": "こちらがお探しのメニューです。どれにしますか？",
                "search_instruction": "お探しのメニューを教えてください。",
                
                # 장바구니
                "empty_cart": "カートは空です。",
                "cart_summary": "合計金額は{total}ウォンです。",
                
                # 주문 확인
                "confirm_order": "ご注文内容は以下の通りです。お支払いに進みますか？",
                
                # 결제
                "payment_options": "お支払い方法を選択してください。",
                "order_complete": "ご注文が完了しました。ありがとうございました！",
                
                # 에러
                "default_error": "申し訳ありません。もう一度お試しください。",
                "error": "申し訳ありません。問題が発生しました。",
                "try_again": "すみません、もう一度おっしゃっていただけますか？"
            },
            "cn": {
                # 메인 화면
                "welcome": "欢迎光临！请问需要点什么？",
                "return_to_main": "已返回主菜单。",
                
                # 주문 옵션
                "ask_option": "您想要{menu}的{option}怎么样？",
                "ask_option_with_values": "您想要{menu}的{option}怎么样？请从{values}中选择。",
                
                # 주문 완료
                "added_to_cart": "已将{item}添加到购物车。还需要其他的吗？",
                "multiple_orders_processing": "正在处理第{current_order_index}个订单。还剩{remaining}个订单。",
                
                # 검색
                "search_not_found": "找不到{keyword}。请尝试其他菜单。",
                "search_results": "以下是搜索结果。您想要哪一个？",
                "search_instruction": "请告诉我您想找什么菜单。",
                
                # 장바구니
                "empty_cart": "购物车是空的。",
                "cart_summary": "总金额为{total}韩元。",
                
                # 주문 확인
                "confirm_order": "您的订单如下。要继续付款吗？",
                
                # 결제
                "payment_options": "请选择付款方式。",
                "order_complete": "订单已完成。谢谢！",
                
                # 에러
                "default_error": "抱歉，请重试。",
                "error": "抱歉，出现了问题。",
                "try_again": "对不起，能再说一遍吗？"
            }
        }

    def _get_text(self, key: str, **kwargs) -> str:
        """템플릿 텍스트 반환 (존재하지 않는 언어는 영어로 폴백)"""
        templates = self._templates.get(self.language, self._templates["en"])
        template = templates.get(key, "")
        return template.format(**kwargs)

    def _get_option_key(self, option_name_kr: str) -> str:
        """한글 옵션 이름을 키로 변환"""
        option_mapping = {
            "온도": "temperature",
            "사이즈": "size",
            "얼음량": "ice_amount",
            "당도": "sweetness",
            "휘핑크림": "whipped_cream",
            "샷 추가": "extra_shot",
            "시럽 추가": "extra_syrup",  
            "우유 변경": "milk_change",
        }
        return option_mapping.get(option_name_kr, option_name_kr.lower().replace(" ", "_"))

    def _get_option_suggestions(self, opt_key: str, store_meta: Dict[str, Any] = None) -> List[str]:
        """매장의 실제 옵션값들을 동적으로 가져오기"""
        if not store_meta or not store_meta.get("option_mappings"):
            return []
        
        # opt_key를 한글 옵션명으로 변환
        key_to_kr = {v: k for k, v in {
            "온도": "temperature",
            "사이즈": "size",
            "얼음량": "ice_amount",
            "당도": "sweetness",
            "휘핑크림": "whipped_cream",
            "샷 추가": "extra_shot",
            "시럽 추가": "extra_syrup",
            "우유 변경": "milk_change"
        }.items()}
        
        option_name_kr = key_to_kr.get(opt_key, opt_key)
        mappings = store_meta["option_mappings"].get(option_name_kr, [])
        
        suggestions = []
        seen = set()
        
        # 언어별 표시
        display_key = "display_kr" if self.language == "kr" else "display_en"
        
        for mapping in mappings:
            display_value = mapping.get(display_key, mapping.get("mapped", mapping["original"]))
            
            if display_value not in seen:
                seen.add(display_value)
                suggestions.append(display_value)
        
        return suggestions

    def _translate_option_name(self, option_key: str) -> str:
        """옵션 키를 언어에 맞게 번역"""
        translations = {
            "kr": {
                "temperature": "온도",
                "size": "사이즈",
                "ice_amount": "얼음량",
                "sweetness": "당도",
                "whipped_cream": "휘핑크림",
                "extra_shot": "샷",
                "milk_change": "우유 종류",
                "extra_syrup": "시럽"
            },
            "en": {
                "temperature": "Temperature",
                "size": "Size",
                "ice_amount": "Ice Amount",
                "sweetness": "Sweetness",
                "whipped_cream": "Whipped Cream",
                "extra_shot": "Extra Shot",
                "milk_change": "Milk Type",
                "extra_syrup": "Syrup"
            },
            "ja": {
                "temperature": "温度",
                "size": "サイズ",
                "ice_amount": "氷の量",
                "sweetness": "甘さ",
                "whipped_cream": "ホイップクリーム",
                "extra_shot": "ショット追加",
                "milk_change": "ミルク変更",
                "extra_syrup": "シロップ追加"
            },
            "cn": {
                "temperature": "温度",
                "size": "尺寸",
                "ice_amount": "冰量",
                "sweetness": "甜度",
                "whipped_cream": "奶油",
                "extra_shot": "加浓",
                "milk_change": "换奶",
                "extra_syrup": "糖浆"
            }
        }
        return translations.get(self.language, translations["en"]).get(option_key, option_key)

    def _get_main_suggestions(self) -> List[str]:
        """메인 화면 추천 옵션"""
        suggestions = {
            "kr": ["메뉴 보기", "장바구니", "완료", "취소"],
            "en": ["View Menu", "Cart", "Done", "Cancel"],
            "ja": ["メニュー", "カート", "完了", "キャンセル"],
            "cn": ["查看菜单", "购物车", "完成", "取消"]
        }
        return suggestions.get(self.language, suggestions["en"])

    def _get_search_suggestions(self) -> List[str]:
        """검색 추천 옵션"""
        suggestions = {
            "kr": ["아메리카노", "카페라떼", "디저트", "콜드브루", "스무디"],
            "en": ["Americano", "Cafe Latte", "Dessert", "Cold Brew", "Smoothie"],
            "ja": ["アメリカーノ", "カフェラテ", "デザート", "コールドブリュー", "スムージー"],
            "cn": ["美式咖啡", "拿铁", "甜点", "冷萃咖啡", "思慕雪"]
        }
        return suggestions.get(self.language, suggestions["en"])

    def _calculate_total(self, cart: List[CartItem]) -> int:
        """장바구니 총액 계산"""
        return sum(item.price * item.quantity for item in cart)

    def generate_response(self, 
                         state: ConversationState,
                         need: List[str],
                         current_order: Dict[str, Any],
                         cart: List[CartItem],
                         store_meta: Dict[str, Any] = None,
                         include_meta: bool = False,
                         multiple_orders_info: Dict[str, int] = None) -> Dict[str, Any]:
        """상태와 필요한 정보에 따라 응답 생성"""
        
        if state == ConversationState.MAIN:
            response = {
                "text": self._get_text("welcome") if not cart else self._get_text("return_to_main"),
                "next_state": ConversationState.MAIN,
                "cart": cart,
                "suggestions": self._get_main_suggestions(),
                "actions": {"show_menu": True}
            }
            # 첫 요청 시 매장 메타데이터 포함
            if include_meta and store_meta:
                response["store_meta"] = store_meta
            return response
        
        elif state == ConversationState.ORDER and need:
            # 옵션 선택 필요
            first_need = need[0]
            current_menu = current_order.get("menuName", "")
            
            # 옵션 표시용 이름 가져오기 
            option_display_name = self._translate_option_name(first_need)
            
            # 다중 주문 처리 메시지
            if multiple_orders_info:
                current_idx = multiple_orders_info.get("current_index", 1)
                remaining = multiple_orders_info.get("remaining", 0)
                multi_message = self._get_text("multiple_orders_processing", 
                                            current_order_index=current_idx, 
                                            remaining=remaining) + " "
            else:
                multi_message = ""
            
            # 동적 질문 생성
            if store_meta and store_meta.get("option_mappings"):
                # 유효한 옵션값들 가져오기
                suggestions = self._get_option_suggestions(first_need, store_meta)
                
                # 값들을 포함한 질문
                if suggestions:
                    values_text = ", ".join(suggestions)
                    text = multi_message + self._get_text(
                        "ask_option_with_values", 
                        menu=current_menu, 
                        option=option_display_name,
                        values=values_text
                    )
                else:
                    text = multi_message + self._get_text(
                        "ask_option", 
                        menu=current_menu, 
                        option=option_display_name
                    )
            else:
                text = multi_message + self._get_text(
                    "ask_option", 
                    menu=current_menu, 
                    option=option_display_name
                )
                suggestions = []
            
            return {
                "text": text,
                "next_state": ConversationState.ORDER,
                "cart": cart,
                "suggestions": suggestions,
                "actions": {}
            }
        
        elif state == ConversationState.ORDER and not need:
            # 주문 완료, 장바구니에 추가
            item = CartItem(**current_order)
            display_name = item.get_display_name(self.language, store_meta)
            
            # 다중 주문 메시지 처리
            if multiple_orders_info:
                current_idx = multiple_orders_info.get("current_index", 1)
                remaining = multiple_orders_info.get("remaining", 0)
                
                if remaining > 0:
                    text = self._get_text(
                        "multiple_orders_processing", 
                        current_order_index=current_idx,
                        remaining=remaining
                    )
                    next_state = ConversationState.ORDER
                else:
                    text = self._get_text("added_to_cart", item=display_name)
                    next_state = ConversationState.MAIN
            else:
                text = self._get_text("added_to_cart", item=display_name)
                next_state = ConversationState.MAIN
            
            # 다음 주문을 위한 제안
            continue_suggestions = {
                "kr": ["계속 주문", "완료"],
                "en": ["Continue", "Done"],
                "ja": ["注文を続ける", "完了"],
                "cn": ["继续点餐", "完成"]
            }.get(self.language, ["Continue", "Done"])
            
            return {
                "text": text,
                "next_state": next_state,
                "cart": cart,
                "suggestions": continue_suggestions,
                "actions": {"add_to_cart": True}
            }
        
        elif state == ConversationState.SEARCH:
            # 검색 상태
            return {
                "text": self._get_text("search_instruction"),
                "next_state": ConversationState.SEARCH,
                "cart": cart,
                "suggestions": self._get_search_suggestions(),
                "actions": {"show_search": True}
            }
        
        elif state == ConversationState.CART:
            # 장바구니 확인
            if not cart:
                return {
                    "text": self._get_text("empty_cart"),
                    "next_state": ConversationState.MAIN,
                    "cart": cart,
                    "suggestions": self._get_main_suggestions()[:1],  # "메뉴 보기"만
                    "actions": {"show_menu": True}
                }
            else:
                total = self._calculate_total(cart)
                
                # 언어별 장바구니 버튼
                confirm_suggestions = {
                    "kr": ["주문하기", "계속 쇼핑"],
                    "en": ["Order", "Continue Shopping"],
                    "ja": ["注文する", "ショッピングを続ける"],
                    "cn": ["下单", "继续购物"]
                }.get(self.language, ["Order", "Continue Shopping"])
                
                return {
                    "text": self._get_text("cart_summary", total=total),
                    "next_state": ConversationState.CONFIRM,
                    "cart": cart,
                    "suggestions": confirm_suggestions,
                    "actions": {"show_cart": True}
                }
        
        elif state == ConversationState.CONFIRM:
            # 주문 확인
            
            # 언어별 확인 버튼
            payment_suggestions = {
                "kr": ["결제하기", "수정하기"],
                "en": ["Pay", "Modify"],
                "ja": ["支払う", "修正する"],
                "cn": ["付款", "修改"]
            }.get(self.language, ["Pay", "Modify"])
            
            return {
                "text": self._get_text("confirm_order"),
                "next_state": ConversationState.PAYMENT,
                "cart": cart,
                "suggestions": payment_suggestions,
                "actions": {"show_order_summary": True}
            }
        
        elif state == ConversationState.PAYMENT:
            # 결제 상태
            
            # 언어별 결제 수단
            payment_methods = {
                "kr": ["카드", "현금", "취소"],
                "en": ["Card", "Cash", "Cancel"],
                "ja": ["カード", "現金", "キャンセル"],
                "cn": ["卡", "现金", "取消"]
            }.get(self.language, ["Card", "Cash", "Cancel"])
            
            return {
                "text": self._get_text("payment_options"),
                "next_state": ConversationState.PAYMENT,
                "cart": cart,
                "suggestions": payment_methods,
                "actions": {"show_payment_methods": True}
            }
        
        # 기본 처리
        return {
            "text": self._get_text("default_error"),
            "next_state": ConversationState.MAIN,
            "cart": cart,
            "suggestions": self._get_main_suggestions(),
            "actions": {}
        }