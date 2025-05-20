# app/services/response_service.py
from typing import Dict, Any, List
from app.models.schemas import Language, ResponseStatus
from app.models.schemas import ResponseStatus

class ResponseService:
    """다국어 응답 생성 서비스"""
    
    def __init__(self):
        # 템플릿 초기화
        self.templates = self._init_templates()
    
    def _init_templates(self) -> Dict[str, Dict[str, Dict[str, str]]]:
        """언어별 응답 템플릿 초기화"""
        return {
            # 한국어 템플릿
            Language.KR: {
                # 메뉴 관련 응답
                "menu_not_found": "죄송합니다. 주문하신 메뉴를 찾을 수 없습니다.",
                "menu_corrected": "{original_name}을(를) {menu_name}(으)로 이해했습니다. {menu_name}를 주문하시겠습니까?",
                "menu_recommendation": "죄송합니다. {reason} 대신 {menu_name}는 어떠세요?",
                
                # 옵션 관련 응답
                "select_temperature": "{menu_name}를 선택하셨네요. 따뜻한 것으로 드릴까요, 차가운 것으로 드릴까요?",
                "select_size": "{menu_name}를 선택하셨네요. 어떤 사이즈로 드릴까요? ({options})",
                "select_option": "{menu_name}를 선택하셨네요. {option_name}을(를) 선택해주세요. ({options})",
                "select_options": "{menu_name}를 선택하셨네요. {options}을(를) 선택해주세요.",
                "option_not_understood": "{option_name} 선택을 이해하지 못했습니다. {options} 중에서 선택해주세요.",

                # 장바구니 관련 응답
                "added_to_cart": "{menu_name}{options_summary}를 장바구니에 담았습니다. 더 주문하실 건가요?",
                
                # 검색 관련 응답
                "search_results": "'{query}' 검색 결과입니다. {count}개의 메뉴를 찾았습니다.",
                "no_search_results": "'{query}'에 대한 검색 결과가 없습니다.",
                
                # 결제 관련 응답
                "confirm_order": "주문 내역을 확인해 주세요. 결제를 진행하시겠습니까?",
                "select_payment": "결제 방법을 선택해 주세요. 카드, 현금, 모바일 결제가 가능합니다.",
                "payment_success": "결제가 완료되었습니다. 이용해 주셔서 감사합니다.",
                "payment_failed": "결제에 실패했습니다. 다시 시도해 주세요.",
                
                # 오류 응답
                "error": "죄송합니다. 주문 처리 중 오류가 발생했습니다. 다시 시도해주세요.",
                "unknown": "죄송합니다. 명령을 이해하지 못했습니다. 다시 말씀해 주세요.",

                # 메뉴 상세 정보 관련 템플릿 추가
                "menu_detail": "'{menu_name}'의 상세 정보입니다.",
                "nutrition_info": "{menu_name}의 영양 성분: {nutrition_text}",
                "ingredients_info": "{menu_name}의 원재료: {ingredients_text}",
                "allergy_info": "{menu_name}의 알레르기 정보: {allergy_text}",
                "no_nutrition_info": "죄송합니다. {menu_name}의 영양 성분 정보가 없습니다.",
                "no_ingredients_info": "죄송합니다. {menu_name}의 원재료 정보가 없습니다.",
                "search_single_result": "{menu_name} - {description} (가격: {price}원)",

                # 한국어 결제 템플릿 추가
                "empty_cart": "장바구니가 비어있습니다. 메뉴를 먼저 선택해주세요.",
                "confirm_order": "주문 내역을 확인해 주세요. 총 금액은 {total_amount}원입니다. 결제를 진행하시겠습니까?",
                "select_payment": "결제 방법을 선택해 주세요. 카드, 카카오페이, 기프트카드, 모바일일상품권이 가능합니다.",
                "payment_success": "{payment_method}로 결제가 완료되었습니다. 이용해 주셔서 감사합니다.",
                "payment_failed": "결제에 실패했습니다. 다시 시도해 주세요.",
                "payment_canceled": "결제가 취소되었습니다. 다시 주문하시겠어요?",
                "payment_method_unknown": "죄송합니다. 선택하신 결제 방법을 인식할 수 없습니다. 다시 말씀해 주세요.",
                "processing_payment": "{payment_method}로 결제를 진행합니다. 잠시만 기다려주세요.",
                "order_canceled": "주문이 취소되었습니다. 메인 화면으로 돌아갑니다.",
                "payment_selection_canceled": "결제 수단 선택이 취소되었습니다. 메인 화면으로 돌아갑니다.",
                "payment_processing_canceled": "결제 처리가 취소되었습니다. 메인 화면으로 돌아갑니다.",
                "order_canceled_for_menu": "주문이 취소되었습니다. 메뉴 화면으로 돌아갑니다."
            
            
            },
            
            # 영어 템플릿
            Language.EN: {
                # 메뉴 관련 응답
                "menu_not_found": "Sorry, I couldn't find the menu you ordered.",
                "menu_corrected": "I understood {original_name} as {menu_name}. Would you like to order {menu_name}?",
                "menu_recommendation": "Sorry, {reason} How about {menu_name} instead?",
                
                # 옵션 관련 응답
                "select_temperature": "You've selected {menu_name}. Would you like it hot or cold?",
                "select_size": "You've selected {menu_name}. What size would you like? ({options})",
                "select_option": "You've selected {menu_name}. Please choose {option_name}. ({options})",
                "select_options": "You've selected {menu_name}. Please choose {options}.",
                "option_not_understood": "I didn't understand your {option_name} selection. Please choose from {options}.",

                # 장바구니 관련 응답
                "added_to_cart": "{menu_name}{options_summary} has been added to your cart. Would you like to order anything else?",
                
                # 검색 관련 응답
                "search_results": "Here are the search results for '{query}'. Found {count} menus.",
                "no_search_results": "No results found for '{query}'.",
                
                # 결제 관련 응답
                "confirm_order": "Please confirm your order. Would you like to proceed with payment?",
                "select_payment": "Please select your payment method. Card, cash, or mobile payment is available.",
                "payment_success": "Payment completed. Thank you for your order.",
                "payment_failed": "Payment failed. Please try again.",
                
                # 오류 응답
                "error": "Sorry, an error occurred while processing your order. Please try again.",
                "unknown": "Sorry, I didn't understand your command. Please try again.",

                # 메뉴 상세 정보 관련 템플릿 추가
                "menu_detail": "Here is the detailed information for '{menu_name}'.",
                "nutrition_info": "Nutritional information for {menu_name}: {nutrition_text}",
                "ingredients_info": "Ingredients for {menu_name}: {ingredients_text}",
                "allergy_info": "Allergy information for {menu_name}: {allergy_text}",
                "no_nutrition_info": "Sorry, there is no nutritional information available for {menu_name}.",
                "no_ingredients_info": "Sorry, there is no ingredient information available for {menu_name}.",
                "search_single_result": "{menu_name} - {description} (Price: {price} KRW)",

                # 영어 결제 템플릿 추가
                "empty_cart": "Your cart is empty. Please select menu items first.",
                "confirm_order": "Please confirm your order. The total amount is {total_amount} KRW. Would you like to proceed with payment?",
                "select_payment": "Please select your payment method. Credit card, KakaoPay, NaverPay, Cash, or Gift Card are available.",
                "payment_success": "Payment with {payment_method} has been completed. Thank you for your order.",
                "payment_failed": "Payment failed. Please try again.",
                "payment_canceled": "Payment has been canceled. Would you like to order again?",
                "payment_method_unknown": "Sorry, I couldn't recognize your payment method. Please try again.",
                "processing_payment": "Processing payment with {payment_method}. Please wait a moment.",
                "order_canceled": "Your order has been canceled. Returning to the main screen.",
                "payment_selection_canceled": "Payment method selection has been canceled. Returning to the main screen.",
                "payment_processing_canceled": "Payment processing has been canceled. Returning to the main screen.",
                "order_canceled_for_menu": "Your order has been canceled. Returning to the menu screen."
            
            
            },
            
            # 일본어 템플릿
            Language.JP: {
                # 메뉴 관련 응답
                "menu_not_found": "申し訳ありませんが、ご注文のメニューが見つかりませんでした。",
                "menu_corrected": "{original_name}を{menu_name}として理解しました。{menu_name}を注文しますか？",
                "menu_recommendation": "申し訳ありません。{reason} 代わりに{menu_name}はいかがですか？",
                
                # 옵션 관련 응답
                "select_temperature": "{menu_name}を選択しました。温かいものにしますか、冷たいものにしますか？",
                "select_size": "{menu_name}を選択しました。サイズはどうしますか？ ({options})",
                "select_option": "{menu_name}を選択しました。{option_name}を選んでください。 ({options})",
                "select_options": "{menu_name}を選択しました。{options}を選んでください。",
                
                # 장바구니 관련 응답
                "added_to_cart": "{menu_name}{options_summary}をカートに追加しました。他に何か注文しますか？",
                
                # 검색 관련 응답
                "search_results": "'{query}'の検索結果です。{count}個のメニューが見つかりました。",
                "no_search_results": "'{query}'に対する検索結果はありません。",
                
                # 결제 관련 응답
                "confirm_order": "注文内容をご確認ください。決済に進みますか？",
                "select_payment": "お支払い方法を選択してください。カード、現金、モバイル決済が可能です。",
                "payment_success": "決済が完了しました。ご利用ありがとうございます。",
                "payment_failed": "決済に失敗しました。もう一度お試しください。",
                
                # 오류 응답
                "error": "申し訳ありません。注文処理中にエラーが発生しました。もう一度お試しください。",
                "unknown": "申し訳ありません。コマンドを理解できませんでした。もう一度言ってください。",

                # 메뉴 상세 정보 관련 템플릿 추가
                "menu_detail": "'{menu_name}'の詳細情報です。",
                "nutrition_info": "{menu_name}の栄養成分: {nutrition_text}",
                "ingredients_info": "{menu_name}の原材料: {ingredients_text}",
                "allergy_info": "{menu_name}のアレルギー情報: {allergy_text}",
                "no_nutrition_info": "申し訳ありませんが、{menu_name}の栄養成分情報はありません。",
                "no_ingredients_info": "申し訳ありませんが、{menu_name}の原材料情報はありません。",
                "search_single_result": "{menu_name} - {description} (価格: {price}ウォン)",
            },
            
            # 중국어 템플릿
            Language.CN: {
                # 메뉴 관련 응답
                "menu_not_found": "抱歉，找不到您点的菜单。",
                "menu_corrected": "我将{original_name}理解为{menu_name}。您要点{menu_name}吗？",
                "menu_recommendation": "抱歉，{reason} 您要不要试试{menu_name}？",
                
                # 옵션 관련 응답
                "select_temperature": "您选择了{menu_name}。您要热的还是冷的？",
                "select_size": "您选择了{menu_name}。您要什么尺寸？ ({options})",
                "select_option": "您选择了{menu_name}。请选择{option_name}。 ({options})",
                "select_options": "您选择了{menu_name}。请选择{options}。",
                
                # 장바구니 관련 응답
                "added_to_cart": "{menu_name}{options_summary}已添加到购物车。您还需要点其他东西吗？",
                
                # 검색 관련 응답
                "search_results": "这是'{query}'的搜索结果。找到了{count}个菜单。",
                "no_search_results": "没有找到'{query}'的搜索结果。",
                
                # 결제 관련 응답
                "confirm_order": "请确认您的订单。您想继续付款吗？",
                "select_payment": "请选择您的付款方式。可以用卡、现金或移动支付。",
                "payment_success": "付款完成。感谢您的订购。",
                "payment_failed": "付款失败。请再试一次。",
                
                # 오류 응답
                "error": "抱歉，处理订单时出错。请再试一次。",
                "unknown": "抱歉，我不明白您的命令。请再说一次。",
                # 메뉴 상세 정보 관련 템플릿 추가
                "menu_detail": "这是'{menu_name}'的详细信息。",
                "nutrition_info": "{menu_name}的营养成分: {nutrition_text}",
                "ingredients_info": "{menu_name}的原材料: {ingredients_text}",
                "allergy_info": "{menu_name}的过敏原信息: {allergy_text}",
                "no_nutrition_info": "抱歉，没有{menu_name}的营养成分信息。",
                "no_ingredients_info": "抱歉，没有{menu_name}的原材料信息。",
                "search_single_result": "{menu_name} - {description} (价格: {price}韩元)",
            }
        }
    
    def get_response(self, template_key: str, language: str, params: Dict[str, Any] = None) -> str:
        """템플릿 키와 언어에 맞는 응답 생성"""
        # 언어 기본값 설정
        lang = language if language in self.templates else Language.KR
        
        # 템플릿 조회
        template = self.templates.get(lang, {}).get(template_key)
        
        if not template:
            # 템플릿이 없는 경우 영어 또는 한국어 템플릿으로 대체
            template = self.templates.get(Language.EN, {}).get(template_key)
            if not template:
                template = self.templates.get(Language.KR, {}).get(template_key, "")
        
        # 파라미터 적용
        if params:
            try:
                return template.format(**params)
            except KeyError:
                return template
        
        return template
    
    def generate_order_reply(self, menus: List[Dict[str, Any]], language: str, status: ResponseStatus) -> str:
        """주문 상태에 따른 응답 생성"""
        if not menus:
            return self.get_response("menu_not_found", language)
        
        menu = menus[0]
        menu_name = menu.get("name") if language == Language.KR else menu.get("name_en", menu.get("name"))
        
        # 1. 메뉴명 교정 상태
        if status == ResponseStatus.CORRECTED:
            original_name = menu.get("original_name", "")
            # 원본 메뉴명이 비어있는 경우 처리
            original_text = original_name if original_name else "선택하신 메뉴"
            return self.get_response("menu_corrected", language, {
                "original_name": original_text,
                "menu_name": menu_name
            })
        
        # 2. 추천 메뉴 상태
        elif status == ResponseStatus.RECOMMENDATION:
            reason = menu.get("recommendation_reason", "")
            return self.get_response("menu_recommendation", language, {
                "reason": reason,
                "menu_name": menu_name
            })
        
        # 3. 필수 옵션 누락 상태
        elif status == ResponseStatus.MISSING_REQUIRED_OPTIONS:
            missing_options = []
            for option in menu.get("options", []):
                if option.get("required", False) and not option.get("is_selected", False):
                    missing_options.append(option)
            
            if missing_options:
                option = missing_options[0]  # 첫 번째 누락된 옵션에 집중
                option_name = option.get("option_name") if language == Language.KR else option.get("option_name_en", option.get("option_name"))
                
                # 온도 옵션 특별 처리
                if "온도" in option_name.lower() or "temperature" in option_name.lower():
                    return self.get_response("select_temperature", language, {
                        "menu_name": menu_name
                    })
                
                # 사이즈 옵션 특별 처리
                elif "사이즈" in option_name.lower() or "size" in option_name.lower():
                    option_values = [detail.get("value") for detail in option.get("option_details", [])]
                    options_str = ", ".join(option_values)
                    return self.get_response("select_size", language, {
                        "menu_name": menu_name,
                        "options": options_str
                    })
                
                # 일반 옵션 처리
                else:
                    option_values = [detail.get("value") for detail in option.get("option_details", [])]
                    options_str = ", ".join(option_values)
                    return self.get_response("select_option", language, {
                        "menu_name": menu_name,
                        "option_name": option_name,
                        "options": options_str
                    })
        
        # 4. 장바구니 추가 가능 상태
        elif status == ResponseStatus.READY_TO_ADD_CART:
            option_strs = []
            for option in menu.get("selected_options", []):
                option_name = option.get("option_name")
                if option.get("option_details"):
                    option_value = option.get("option_details")[0].get("value")
                    option_strs.append(f"{option_name}: {option_value}")
            
            options_summary = f" ({', '.join(option_strs)})" if option_strs else ""
            return self.get_response("added_to_cart", language, {
                "menu_name": menu_name,
                "options_summary": options_summary
            })
        
        # 5. 기본 상태 - 알 수 없음
        return self.get_response("unknown", language)