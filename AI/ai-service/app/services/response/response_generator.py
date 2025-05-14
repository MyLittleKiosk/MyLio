# app/services/response/response_generator.py
from typing import Dict, Any, Optional
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from app.models.schemas import Language, ResponseStatus, IntentType
from app.services.response_service import ResponseService

class ResponseGenerator:
    """LLM 기반 응답 생성 서비스"""
    
    def __init__(self, api_key: str, response_service: ResponseService):
        """초기화"""
        self.response_service = response_service
        
        # LLM 초기화
        self.llm = ChatOpenAI(
            model_kwargs={"api_key": api_key},
            model_name="gpt-4.1", 
            temperature=0.7  # 응답 생성에는 더 높은 temperature 사용
        )
    
    def generate_response(self, intent_data: Dict[str, Any], language: str, context: Dict[str, Any]) -> str:
        """의도 데이터 기반 응답 생성"""
        # 언어 확인 및 실제 적용 로직 강화
        if language not in [Language.KR, Language.EN, Language.JP, Language.CN]:
            language = Language.KR  # 기본값
        
        # 프롬프트에 언어 지시 강화
        if language == Language.KR:
            prompt_instruction = "반드시 한국어로만 응답하세요."
        elif language == Language.EN:
            prompt_instruction = "You MUST respond ONLY in English."
        elif language == Language.JP:
            prompt_instruction = "必ず日本語のみで応答してください。"
        elif language == Language.CN:
            prompt_instruction = "必须只用中文回答。"

        # 의도에 따른 템플릿 키 선택
        template_key = self._get_template_key(intent_data, context)
        
        # 템플릿 기반 응답 생성 시도
        if template_key:
            params = self._extract_template_params(intent_data, context)
            template_response = self.response_service.get_response(template_key, language, params)
            
            # 템플릿 응답이 있으면 반환
            if template_response:
                # 템플릿 변수가 남아있는지 확인하고 처리
                if "{" in template_response and "}" in template_response:
                    # 컨텍스트에서 메뉴 정보 추출
                    if "menus" in context and context["menus"]:
                        menu = context["menus"][0]
                        if "{menu_name}" in template_response:
                            menu_name = menu.get("name", "")
                            template_response = template_response.replace("{menu_name}", menu_name)
                        
                        if "{options_summary}" in template_response:
                            option_strs = []
                            for opt in menu.get("selected_options", []):
                                if opt.get("option_details"):
                                    option_name = opt.get("option_name", "")
                                    option_value = opt["option_details"][0].get("value", "")
                                    option_strs.append(f"{option_name}: {option_value}")
                            
                            options_summary = f" ({', '.join(option_strs)})" if option_strs else ""
                            template_response = template_response.replace("{options_summary}", options_summary)
                return template_response
        
        # LLM 기반 응답 생성
        return self._generate_llm_response(intent_data, language, context)
    
    def _get_template_key(self, intent_data: Dict[str, Any], context: Dict[str, Any]) -> Optional[str]:
        """의도 데이터에 따른 템플릿 키 결정"""
        intent_type = intent_data.get("intent_type", "UNKNOWN")
        status = context.get("status", ResponseStatus.UNKNOWN)
        
        # 의도별 템플릿 키 매핑
        intent_template_map = {
            "ORDER": {
                ResponseStatus.CORRECTED: "menu_corrected",
                ResponseStatus.RECOMMENDATION: "menu_recommendation",
                ResponseStatus.MISSING_REQUIRED_OPTIONS: "select_option",
                ResponseStatus.READY_TO_ADD_CART: "added_to_cart",
                ResponseStatus.UNKNOWN: "menu_not_found"
            },
            "SEARCH": {
                ResponseStatus.SEARCH_RESULTS: "search_results",
                ResponseStatus.UNKNOWN: "no_search_results"
            },
            "PAYMENT": {
                ResponseStatus.PAYMENT_CONFIRM: "confirm_order",
                ResponseStatus.PAYMENT_SUCCESS: "payment_success",
                ResponseStatus.PAYMENT_FAILED: "payment_failed",
                ResponseStatus.UNKNOWN: "select_payment"
            },
            "DETAIL": {
                ResponseStatus.DETAIL: "menu_detail",
                ResponseStatus.UNKNOWN: "no_nutrition_info"
            },
            "OPTION_SELECT": {
                ResponseStatus.MISSING_REQUIRED_OPTIONS: "select_option",
                ResponseStatus.UNKNOWN: "option_not_understood"
            },
            "UNKNOWN": {
                ResponseStatus.UNKNOWN: "unknown"
            }
        }
        
        # 해당 의도와 상태에 맞는 템플릿 키 반환
        if intent_type in intent_template_map and status in intent_template_map[intent_type]:
            return intent_template_map[intent_type][status]
        
        return None
    
    def _extract_template_params(self, intent_data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """템플릿 파라미터 추출"""
        params = {}
        
        # 메뉴 정보 추출
        if "menus" in intent_data and intent_data["menus"]:
            menu = intent_data["menus"][0]
            params["menu_name"] = menu.get("menu_name", "")
            params["original_name"] = menu.get("original_name", "")
            params["options"] = ", ".join(opt.get("option_value", "") for opt in menu.get("options", []))
            
            # 옵션 요약
            option_strs = []
            for opt in menu.get("options", []):
                option_strs.append(f"{opt.get('option_name')}: {opt.get('option_value')}")
            params["options_summary"] = f" ({', '.join(option_strs)})" if option_strs else ""
            
        # 검색 정보 추출
        if "search_query" in intent_data:
            params["query"] = intent_data["search_query"]
        
        # 검색 결과 정보 추출
        if "search_results" in context:
            search_results = context["search_results"]
            params["count"] = len(search_results)
            
            if search_results:
                params["menu_names"] = ", ".join([result.get("name_kr", "") for result in search_results[:3]])
                
                if len(search_results) == 1:
                    params["description"] = search_results[0].get("description", "")
                    params["price"] = search_results[0].get("price", 0)
        
        # 상세 정보 추출
        if intent_data.get("intent_type") == "DETAIL":
            params["menu_name"] = intent_data.get("menu_name", "")
            
            if "nutrition" in context:
                nutrition_items = []
                for item in context["nutrition"]:
                    nutrition_items.append(f"{item['name']}: {item['formatted']}")
                params["nutrition_text"] = ", ".join(nutrition_items)
            
            if "ingredients" in context:
                ingredients = [ing["name_kr"] for ing in context["ingredients"]]
                params["ingredients_text"] = ", ".join(ingredients)
        
        # 결제 정보 추출
        if intent_data.get("intent_type") == "PAYMENT":
            if "total_amount" in context:
                params["total_amount"] = context["total_amount"]
            
            if "payment_method" in intent_data:
                params["payment_method"] = intent_data["payment_method"]
        
        return params
    
    def _generate_llm_response(self, intent_data: Dict[str, Any], language: str, context: Dict[str, Any]) -> str:
        """LLM을 사용한 동적 응답 생성"""
        # 언어별 프롬프트 설정
        language_instruction = ""
        language_example = ""
        
        if language == "KR" or language == "":
            language_text = "한국어"
            language_instruction = "응답은 반드시 한국어로만 작성하세요."
            language_example = "예시: '아메리카노를 장바구니에 담았습니다. 더 필요한 것이 있으신가요?'"
        elif language == "EN":
            language_text = "영어 (English)"
            language_instruction = "The response MUST be in English only."
            language_example = "Example: 'Americano has been added to your cart. Would you like anything else?'"
        elif language == "JP":
            language_text = "일본어 (日本語)"
            language_instruction = "必ず日本語だけで応答してください。"
            language_example = "例: 'アメリカーノをカートに追加しました。他に何かご入用ですか？'"
        elif language == "CN":
            language_text = "중국어 (中文)"
            language_instruction = "回答必须仅使用中文。"
            language_example = "例如: '美式咖啡已添加到购物车。您还需要其他东西吗？'"
        else:
            # 기본값은 한국어
            language_text = "한국어"
            language_instruction = "응답은 반드시 한국어로만 작성하세요."
            language_example = "예시: '아메리카노를 장바구니에 담았습니다. 더 필요한 것이 있으신가요?'"
        
        # 프롬프트 템플릿 - 사용 언어를 명확히 지정
        template = f"""
        당신은 음성 키오스크 시스템의 응답 생성 모듈입니다. 
        사용자의 의도와 컨텍스트 정보를 바탕으로 자연스러운 응답을 생성해야 합니다.

        # 사용자 의도 정보
        {{intent_info}}

        # 컨텍스트 정보
        {{context_info}}

        # 응답 요구사항
        1. 응답 언어: {language_text}
        2. {language_instruction}
        3. 간결하고 명확한 응답 생성 (25단어 이내로 짧게)
        4. 의도에 맞는 적절한 안내 제공
        5. 친절하고 공손한 톤 유지
        6. {language_example}

        # 중요
        - 다른 언어를 섞지 말고 반드시 {language_text}로만 응답하세요.
        - 템플릿 변수({menu_name} 같은 형식)를 사용하지 않고 실제 값을 직접 사용하세요.
        - 영양 정보나 원재료 정보를 요청받은 경우, 반드시 컨텍스트에서 제공된 실제 데이터만 사용하세요.
        - 영양 정보나 원재료 정보가 없는 경우, 임의로 생성하지 말고 정보가 없다고 안내하세요.

        # 응답 생성
        {language_text}로 자연스러운 응답을 생성해주세요:
        """
        
        # 의도 정보 형식화
        intent_info = f"의도 유형: {intent_data.get('intent_type', 'UNKNOWN')}\n"
        
        # 메뉴 정보가 있는 경우 상세 추가
        if "menus" in intent_data and intent_data["menus"]:
            menu = intent_data["menus"][0]
            intent_info += f"메뉴: {menu.get('menu_name', '')}\n"
            intent_info += f"수량: {menu.get('quantity', 1)}\n"
            
            options = []
            for opt in menu.get("options", []):
                options.append(f"{opt.get('option_name', '')}: {opt.get('option_value', '')}")
            
            if options:
                intent_info += f"옵션: {', '.join(options)}\n"
        
        # context에서 메뉴 정보가 있는 경우 추가
        if "menus" in context and context["menus"]:
            menu = context["menus"][0]
            intent_info += f"선택한 메뉴: {menu.get('name', '')}\n"
            
            options = []
            for opt in menu.get("selected_options", []):
                if opt.get("option_details"):
                    option_name = opt.get("option_name", "")
                    option_value = opt["option_details"][0].get("value", "")
                    options.append(f"{option_name}: {option_value}")
            
            if options:
                intent_info += f"선택한 옵션: {', '.join(options)}\n"
        
        # 검색 정보 추가
        if "search_query" in intent_data:
            intent_info += f"검색 쿼리: {intent_data['search_query']}\n"
        
        if "menu_name" in intent_data:
            intent_info += f"메뉴: {intent_data['menu_name']}\n"
        
        if "attribute" in intent_data:
            intent_info += f"속성: {intent_data['attribute']}\n"
        
        if "payment_method" in intent_data:
            intent_info += f"결제 방법: {intent_data['payment_method']}\n"
        
        # 컨텍스트 정보 형식화
        context_info = f"화면 상태: {context.get('screen_state', 'MAIN')}\n"
        context_info += f"응답 상태: {context.get('status', 'UNKNOWN')}\n"
        
        # 메뉴 상세 정보 추가
        if "menu" in context:
            menu = context["menu"]
            context_info += f"\n메뉴 상세 정보:\n"
            context_info += f"이름: {menu.get('name_kr', '')}\n"
            context_info += f"설명: {menu.get('description', '')}\n"
            
            # 영양 정보 추가
            if "nutrition" in context:
                nutrition_data = context["nutrition"]
                if nutrition_data:
                    context_info += "영양 성분:\n"
                    for item in nutrition_data:
                        name = item.get("name", "")
                        formatted = item.get("formatted", "")
                        context_info += f"- {name}: {formatted}\n"
                else:
                    context_info += "영양 성분 정보 없음\n"
            
            # 원재료 정보 추가
            if "ingredients" in context:
                ingredients = context["ingredients"]
                if ingredients:
                    ingredient_names = [ing.get("name_kr", "") for ing in ingredients]
                    context_info += f"원재료: {', '.join(ingredient_names)}\n"
                else:
                    context_info += "원재료 정보 없음\n"
        
        # 장바구니 정보 추가
        if "cart" in context and context["cart"]:
            cart_items = []
            for item in context["cart"]:
                cart_items.append(f"{item.get('name', '')} x {item.get('quantity', 1)}개")
            
            context_info += f"\n장바구니: {', '.join(cart_items)}\n"
        
        # 검색 결과 정보 추가
        if "search_results" in context and context["search_results"]:
            results = context["search_results"]
            context_info += f"검색 결과 수: {len(results)}\n"
            
            if len(results) > 0:
                result_names = [result.get("name_kr", "") for result in results[:3]]
                context_info += f"검색 결과: {', '.join(result_names)}" + ("..." if len(results) > 3 else "") + "\n"
                
                if language == "EN":
                    en_names = [result.get("name_en", result.get("name_kr", "")) for result in results[:3]]
                    context_info += f"검색 결과(영어): {', '.join(en_names)}" + ("..." if len(results) > 3 else "") + "\n"
        
        # LLM 체인 실행
        chain = LLMChain(
            llm=self.llm,
            prompt=PromptTemplate(
                template=template,
                input_variables=["intent_info", "context_info"]
            )
        )
        
        response = chain.run(
            intent_info=intent_info,
            context_info=context_info
        )
        
        # 응답 내에 템플릿 변수가 포함되어 있는지 확인하고 제거
        if "{" in response and "}" in response:
            import re
            response = re.sub(r'\{[^}]+\}', '', response)
        
        return response.strip()