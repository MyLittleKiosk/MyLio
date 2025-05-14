# app/services/intent/intent_recognizer.py
from typing import Dict, Any, List,Optional
import json
import re
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI

from app.models.schemas import IntentType, ScreenState, Language
from app.services.menu_service import MenuService
from app.models.schemas import ResponseStatus

class IntentRecognizer:
    """사용자 의도 인식 서비스"""
    
    def __init__(self, api_key: str, menu_service: MenuService):
        """인식기 초기화"""
        self.menu_service = menu_service
        
        # LLM 초기화
        self.llm = ChatOpenAI(
            model_kwargs={"api_key": api_key},
            model_name="gpt-4.1", 
            temperature=0.3
        )
        
        # Few-shot 학습 예제
        self.examples = self._load_examples()
    
    def recognize_intent(self, text: str, language: str, screen_state: str, store_id: int, session: Dict[str, Any]) -> Dict[str, Any]:
        """Few-shot 학습을 통한 의도 인식"""
        # 메뉴 정보 로드
        store_menus = self.menu_service.get_store_menus(store_id)
        
        # 화면 상태에 따른 컨텍스트 구성
        context = self._build_context(screen_state, store_id, store_menus, session)
        
        # Few-shot 예제 선택
        examples = self._select_examples(screen_state, language)
        
        # 프롬프트 템플릿
        prompt_template = self._get_prompt_template()
        
        # LLM 체인 실행
        chain = LLMChain(llm=self.llm, prompt=prompt_template)
        response = chain.run(
            screen_state=screen_state,
            language=language,
            context=context,
            history=self._format_history(session),
            examples=examples,
            text=text
        )
        
        # LLM 응답 파싱
        result = self._parse_llm_response(response)
        
        # 디버깅 정보
        print(f"[의도 인식] 입력: '{text}', 인식 결과: {result}")
        
        # DetailProcessor가 없어도 영양 성분 관련 의도를 인식할 수 있도록
        if self._is_detail_intent(text, language):
            result["intent_type"] = IntentType.DETAIL
            
            # 메뉴 이름 추출 시도
            menu_name = self._extract_menu_name(text, store_id)
            if menu_name:
                result["menu_name"] = menu_name
                menu = self.menu_service.find_menu_by_name(menu_name, store_id)
                if menu:
                    result["menu_id"] = menu["id"]
        
        return result
    
    def _is_detail_intent(self, text: str, language: str) -> bool:
        """영양 성분 관련 의도인지 확인"""
        text_lower = text.lower()
        
        # 한국어 패턴
        if language == Language.KR:
            detail_keywords = ["영양", "성분", "칼로리", "원재료", "알레르기", "원산지", "정보", "상세"]
            return any(keyword in text_lower for keyword in detail_keywords)
        
        # 영어 패턴
        else:
            detail_keywords = ["nutrition", "calorie", "ingredient", "allergy", "detail", "information"]
            return any(keyword in text_lower for keyword in detail_keywords)
    
    def _extract_menu_name(self, text: str, store_id: int) -> Optional[str]:
        """텍스트에서 메뉴 이름 추출 시도"""
        # 메뉴 이름 목록 가져오기
        store_menus = self.menu_service.get_store_menus(store_id)
        menu_names = [menu["name_kr"] for menu in store_menus.values()]
        menu_names.extend([menu.get("name_en", "") for menu in store_menus.values() if menu.get("name_en")])
        
        # 긴 이름부터 매칭 시도 (짧은 이름이 긴 이름에 포함될 수 있으므로)
        menu_names.sort(key=len, reverse=True)
        
        for name in menu_names:
            if name and name.lower() in text.lower():
                return name
        
        return None
    
    def _build_context(self, screen_state: str, store_id: int, store_menus: Dict[int, Dict[str, Any]], session: Dict[str, Any]) -> str:
        """상황에 맞는 컨텍스트 구성"""
        context_parts = []
        
        # 1. 메뉴 정보 요약 (모든 메뉴 포함)
        menu_list = list(store_menus.values())  # 모든 메뉴 포함
        
        # 카테고리별로 메뉴 그룹화
        categorized_menus = {}
        for menu in menu_list:
            category_id = menu.get("category_id")
            if category_id not in categorized_menus:
                categorized_menus[category_id] = []
            categorized_menus[category_id].append(menu)
        
        # 카테고리별로 메뉴 정보 구성
        for category_id, menus in categorized_menus.items():
            category_name = self._get_category_name(category_id, store_id) or f"카테고리 {category_id}"
            category_items = []
            
            for menu in menus:
                # 기본 메뉴 정보
                menu_info = [f"### {menu['name_kr']} ({menu.get('name_en', '')}): {menu['price']}원"]
                
                if menu.get('description'):
                    menu_info.append(f"설명: {menu['description']}")
                
                # 옵션 정보 추가
                if menu.get('options'):
                    options_info = ["#### 옵션:"]
                    for opt in menu['options']:
                        opt_name = opt.get('option_name', '')
                        required = "필수" if opt.get('required', False) else "선택"
                        options_info.append(f"- {opt_name} ({required})")
                        
                        # 옵션 상세 정보
                        if opt.get('option_details'):
                            detail_items = []
                            for detail in opt['option_details']:
                                value = detail.get('value', '')
                                add_price = detail.get('additional_price', 0)
                                price_info = f"+{add_price}원" if add_price > 0 else ""
                                detail_items.append(f"  * {value} {price_info}")
                            options_info.extend(detail_items)
                    
                    menu_info.append("\n".join(options_info))
                
                # 영양 성분 정보 추가
                if menu.get('nutrition'):
                    nutrition_info = ["#### 영양 성분:"]
                    
                    # nutrition이 리스트인 경우
                    if isinstance(menu['nutrition'], list):
                        for item in menu['nutrition']:
                            name = item.get('name', '')
                            formatted_value = item.get('formatted', '')
                            nutrition_info.append(f"- {name}: {formatted_value}")
                    # nutrition이 딕셔너리인 경우
                    elif isinstance(menu['nutrition'], dict):
                        for key, value in menu['nutrition'].items():
                            nutrition_info.append(f"- {key}: {value}")
                    
                    menu_info.append("\n".join(nutrition_info))
                
                # 원재료 정보 추가
                if menu.get('ingredients'):
                    ingredients = [ing.get('name_kr', '') for ing in menu['ingredients']]
                    if ingredients:
                        menu_info.append(f"#### 원재료: {', '.join(ingredients)}")
                
                category_items.append("\n".join(menu_info))
            
            context_parts.append(f"## {category_name}\n" + "\n\n".join(category_items))
        
        # 2. 장바구니 정보 (있는 경우)
        cart = session.get("cart", [])
        if cart:
            cart_summary = ["## 현재 장바구니"]
            
            for item in cart:
                option_text = ""
                if item.get("selected_options"):
                    option_strs = []
                    for opt in item["selected_options"]:
                        if opt.get("option_details"):
                            opt_value = opt["option_details"][0].get("value", "")
                            option_strs.append(f"{opt['option_name']}: {opt_value}")
                    
                    if option_strs:
                        option_text = f" ({', '.join(option_strs)})"
                
                cart_summary.append(f"- {item['name']}{option_text} x {item['quantity']}개: {item['total_price']}원")
            
            context_parts.append("\n".join(cart_summary))
        
        # 3. 화면 상태별 추가 컨텍스트
        if screen_state == ScreenState.ORDER and session.get("last_state", {}).get("menu"):
            menu = session["last_state"]["menu"]
            context_parts.append(f"## 현재 선택된 메뉴\n{menu['name_kr']} ({menu['price']}원)")
        
        return "\n\n".join(context_parts)
    
    def _format_history(self, session: Dict[str, Any]) -> str:
        """대화 기록 포맷팅"""
        history = session.get("history", [])
        
        if not history:
            return "대화 기록 없음"
        
        # 최근 3개 대화만 포함
        recent_history = history[-3:]
        formatted_history = []
        
        for entry in recent_history:
            formatted_history.append(f"사용자: \"{entry.get('user_input', '')}\"")
            
            response = entry.get("system_response", {})
            formatted_history.append(f"시스템: \"{response.get('data', {}).get('reply', '')}\"")
        
        return "\n".join(formatted_history)
    
    def _parse_llm_response(self, response: str) -> Dict[str, Any]:
        """LLM 응답 파싱"""
        try:
            print(f"파싱할 LLM 응답: {response}")  # 디버깅용
            # JSON 블록 추출
            json_pattern = r'```(?:json)?\s*([\s\S]*?)```'
            match = re.search(json_pattern, response)
            
            if match:
                json_str = match.group(1).strip()
            else:
                # 중괄호로 둘러싸인 부분 추출
                json_pattern = r'{[\s\S]*?}'
                match = re.search(json_pattern, response)
                
                if match:
                    json_str = match.group(0).strip()
                else:
                    json_str = response.strip()
        
            print(f"파싱된 JSON 문자열: {json_str}")  # 디버깅용
            
            # JSON 파싱
            result = json.loads(json_str)
            
            # 필수 필드 확인
            if "intent_type" not in result:
                result["intent_type"] = IntentType.UNKNOWN
            
            # 대소문자 표준화
            if isinstance(result["intent_type"], str):
                result["intent_type"] = result["intent_type"].upper()
            
            # 결제 수단 표준화 - KAKAOPAY는 PAY로 변환 (None 체크 추가)
            if result.get("intent_type") == IntentType.PAYMENT and "payment_method" in result and result["payment_method"] is not None:
                if result["payment_method"].upper() == "KAKAOPAY":
                    result["payment_method"] = "PAY"
            
            return result
        
        except Exception as e:
            print(f"LLM 응답 파싱 오류: {e}")
            print(f"원본 응답: {response}")
            
            # 기본 응답
            return {
                "intent_type": IntentType.UNKNOWN,
                "menus": []
            }
    
    def _get_category_name(self, category_id: int, store_id: int = None) -> str:
        """카테고리 ID에 해당하는 카테고리 이름을 반환"""
        # 메뉴 서비스에서 카테고리 정보 가져오기
        category = self.menu_service.get_category_by_id(category_id)
        
        if category:
            return category.get('name_kr', f"카테고리 {category_id}")
        else:
            return f"카테고리 {category_id}"
    
    def _get_prompt_template(self) -> PromptTemplate:
        """통합 의도 인식 프롬프트 템플릿"""
        template = """
        당신은 음성 키오스크 시스템의 일부입니다. 사용자의 발화를 분석하여 의도와 관련 정보를 인식해야 합니다.

        # 현재 시스템 상태
        - 현재 화면: {screen_state}
        - 사용자 언어: {language}

        # 메뉴 정보 및 컨텍스트
        {context}

        # 대화 기록
        {history}

        # 사용자 발화 분석 예제
        {examples}

        # 현재 입력
        사용자: "{text}"

        # 분석 요구사항
        사용자의 발화에서 다음을 파악하세요:
        1. 사용자의 의도 (ORDER, SEARCH, OPTION_SELECT, PAYMENT, DETAIL, UNKNOWN 중 하나)
        2. 의도별 필요한 추가 정보:
           - ORDER: 주문하려는 메뉴명, 수량, 옵션 정보
           - SEARCH: 검색 쿼리
           - OPTION_SELECT: 선택한 옵션 이름과 값
           - PAYMENT: 결제 방법
           - DETAIL: 정보를 요청한 메뉴명, 요청한 정보 유형(영양성분, 원재료 등)

        3. 메뉴명 교정 규칙:
        - "아아/아이스아메리카노" → "아메리카노" + 옵션:"ICE"
        - "따아/핫아메리카노" → "아메리카노" + 옵션:"HOT"
        - "카페라떼/카페라테/라떼" → "카페 라떼"
        - "바닐라라떼/바닐라라테" → "바닐라 라떼"

        4. 옵션 매핑 규칙:
        - "아이스/차가운/아아" → 온도 옵션:"ICE"
        - "따뜻한/뜨거운/따아" → 온도 옵션:"HOT"
        - "작은/스몰/S" → 사이즈 옵션:"S"
        - "중간/미디엄/M" → 사이즈 옵션:"M"
        - "큰/라지/L" → 사이즈 옵션:"L"

        5. 취소 규칙:
        - 현재 화면 상태가 "ORDER"이고 아직 선택하지 못한 옵션이 남아있는데 다른 메뉴를 선택하려는 경우 -> 아직 메뉴가 선택되지 않았어요. 옵션을 선택해주세요.
        

        주의: 응답을 생성할 때 템플릿 문자열이 아닌 실제 사용자에게 보여질 자연스러운 응답을 직접 생성해주세요.
        꼭 해요체를 써주세요.

        # 응답 형식
        분석 결과를 다음 JSON 형식으로 반환하세요:
        ```json
        {{
          "intent_type": "ORDER/SEARCH/PAYMENT/DETAIL/OPTION_SELECT/UNKNOWN",
          "confidence": 0.0~1.0 사이의 신뢰도 점수,
          "menus": [ // ORDER 의도에만 사용
            {{
              "menu_name": "메뉴 이름",
              "quantity": 수량,
              "options": [
                {{
                  "option_name": "옵션 이름 (예: 온도, 사이즈)",
                  "option_value": "옵션 값 (예: ICE, HOT, S, M, L)"
                }}
              ]
            }}
          ],
          "search_query": "검색 쿼리 (SEARCH 의도에만 사용)",
          "payment_method": "결제 방법 (PAYMENT 의도에만 사용)",
          "menu_name": "메뉴 이름 (DETAIL 의도에만 사용)",
          "attribute": "요청한 정보 유형 (DETAIL 의도에만 사용)",
          "post_text": "사용자 의도를 반영한 후처리된 텍스트",
          "reply": "사용자에게 제공할 응답 메시지"
        }}
        ```
        """
        
        return PromptTemplate(
            input_variables=["screen_state", "language", "context", "history", "examples", "text"],
            template=template
        )
    
    def _load_examples(self) -> Dict[str, List[Dict[str, Any]]]:
        """통합 Few-shot 예제 로드"""
        return {
            # 주문 예제
            "order": [
                {
                    "input": "아바라 하나 주세요",  # 특수 케이스 추가
                    "output": {
                        "intent_type": "ORDER",
                        "menus": [
                            {
                                "menu_name": "바닐라라떼",
                                "quantity": 1,
                                "options": [
                                    {
                                        "option_name": "온도",
                                        "option_value": "ICE"
                                    }
                                ]
                            }
                        ],
                        "post_text": "아바라 하나 주세요",
                        "reply": "바닐라 라떼 (ICE) 사이즈는 어떻게 해드릴까요?(S, M, L)"
                    
                    }
                },
                {
                    "input": "아샷추 하나 주세요",
                    "output": {
                        "intent_type": "ORDER",
                        "confidence": 0.9,
                        "menus": [
                            {
                                "menu_name": "아이스티",
                                "quantity": 1,
                                "options": [
                                    {
                                        "option_name": "온도",
                                        "option_value": "ICE"
                                    },
                                    {
                                        "option_name": "샷추가",
                                        "option_value": "샷1개 추가"
                                    }
                                ]
                            }
                        ],
                        "post_text": "아샷추 하나 주세요",
                        "reply": "아이스티 (샷 1개 추가) 사이즈는 어떻게 해드릴까요?"
                    }
                },
                {
                    "input": "아아 하나 주세요",
                    "output": {
                        "intent_type": "ORDER",
                        "confidence": 0.9,
                        "menus": [
                            {
                                "menu_name": "아메리카노",
                                "quantity": 1,
                                "options": [
                                    {
                                        "option_name": "온도",
                                        "option_value": "ICE"
                                    }
                                ]
                            }
                        ],
                        "post_text": "아아 하나 주세요",
                        "reply": "아메리카노(Ice) 사이즈는 어떻게 해드릴까요?(S, M, L)"
                    }
                },
                {
                    "input": "따아 한잔이요",
                    "output": {
                        "intent_type": "ORDER",
                        "confidence": 0.9,
                        "menus": [
                            {
                                "menu_name": "아메리카노",
                                "quantity": 1,
                                "options": [
                                    {
                                        "option_name": "온도",
                                        "option_value": "HOT"
                                    }
                                ]
                            }
                        ],
                        "post_text": "따뜻한 아메리카노 한 잔이요.",
                        "reply": "따뜻한 아메리카노 사이즈는 어떻게 해드릴까요?"
                    }
                },
                {
                    "input": "큰 사이즈 아아 한잔이요",
                    "output": {
                        "intent_type": "ORDER",
                        "confidence": 0.9,
                        "menus": [
                            {
                                "menu_name": "아메리카노",
                                "quantity": 1,
                                "options": [
                                    {
                                        "option_name": "온도",
                                        "option_value": "ICE"
                                    },
                                    {
                                        "option_name": "사이즈",
                                        "option_value": "L"
                                    }
                                ]
                            }
                        ],
                        "post_text": "큰 사이즈 아아 한잔이요",
                        "reply": "라지 사이즈 아이스 아메리카노 한잔 장바구니에 담았어요."
                    }
                }
            ],
            
            # 옵션 선택 예제
            "option": [
                {
                    "input": "아이스로 해주세요",
                    "output": {
                        "intent_type": "OPTION_SELECT",
                        "confidence": 0.9,
                        "menus": [
                            {
                                "options": [
                                    {
                                        "option_name": "온도",
                                        "option_value": "ICE"
                                    }
                                ]
                            }
                        ],
                        "post_text": "아이스로 해주세요",
                        "reply": "아이스로 준비할게요. 사이즈는 어떻게 해드릴까요?"
                    }
                },
                {
                    "input": "라지 사이즈로 주세요",
                    "output": {
                        "intent_type": "OPTION_SELECT",
                        "confidence": 0.9,
                        "menus": [
                            {
                                "options": [
                                    {
                                        "option_name": "사이즈",
                                        "option_value": "L"
                                    }
                                ]
                            }
                        ],
                        "post_text": "라지 사이즈로 주세요.",
                        "reply": "주문하신 메뉴 장바구니에 담았습니다."
                    }
                }
            ],
            
            # 검색 예제
            "search": [
                {
                    "input": "커피 메뉴 알려주세요",
                    "output": {
                        "intent_type": "SEARCH",
                        "confidence": 0.9,
                        "search_query": "커피",
                        "post_text": "커피 메뉴 알려주세요.",
                        "reply": "커피 메뉴를 찾아볼게요. 총 5개의 메뉴가 있어요." 
                    }
                },
                {
                    "input": "디카페인 메뉴 있어?",
                    "output": {
                        "intent_type": "SEARCH",
                        "confidence": 0.9,
                        "search_query": "디카페인",
                        "post_text": "디카페인 메뉴 있어?",
                        "reply": "디카페인 메뉴는 총 3가지 메뉴가 있어요."
                    }
                }
            ],
            
            # 결제 예제
            "payment": [
                {
                    "input": "결제할게요",
                    "output": {
                        "intent_type": "PAYMENT",
                        "confidence": 0.9,
                        "post_text": "결제할게요.",
                        "reply": "결제를 진행할게요. 결제 방법을 선택해주세요."
                    }
                },
                {
                    "input": "카드로 결제할게요",
                    "output": {
                        "intent_type": "PAYMENT",
                        "confidence": 0.9,
                        "payment_method": "CARD",
                        "post_text": "카드로 결제할게요",
                        "reply": "카드로 결제를 진행할게요. 카드를 넣어주세요."
                    }
                }
            ],
            
            # 상세 정보 조회 예제
            "detail": [
                {
                    "input": "아메리카노 영양 성분 알려줘",
                    "output": {
                        "intent_type": "DETAIL",
                        "confidence": 0.9,
                        "menu_name": "아메리카노",
                        "attribute": "nutrition",
                        "post_text": "아메리카노 영양 성분 알려줘",
                        "reply": "아메리카노의 영양 성분을 알려드릴게요."
                    }
                },
                {
                    "input": "이 메뉴 원재료가 뭐야?",
                    "output": {
                        "intent_type": "DETAIL",
                        "confidence": 0.9,
                        "attribute": "ingredients",
                        "post_text": "이 메뉴 원재료가 뭐야?",
                        "reply": "죄송합니다. 이 메뉴의 원재료 정보가 없네요."
                    }
                }
            ]
        }
    
    def _select_examples(self, screen_state: str, language: str) -> str:
        """화면 상태에 맞는 Few-shot 예제 선택"""
        examples = []
        
        # 화면 상태에 따른 예제 선택
        if screen_state == ScreenState.MAIN:
            # 메인 화면에서는 주문, 검색, 상세정보 의도 예제
            examples.extend(self.examples["order"][:2])
            examples.append(self.examples["search"][0])
            examples.append(self.examples["detail"][0])
            
        elif screen_state == ScreenState.SEARCH:
            # 검색 화면에서는 검색, 주문 의도 예제
            examples.extend(self.examples["search"])
            examples.append(self.examples["order"][0])
            
        elif screen_state == ScreenState.DETAIL:
            # 상세 화면에서는 상세정보, 주문 의도 예제
            examples.extend(self.examples["detail"])
            examples.append(self.examples["order"][0])
            
        elif screen_state == ScreenState.ORDER:
            # 주문 화면에서는 옵션 선택, 주문 의도 예제
            examples.extend(self.examples["option"])
            examples.append(self.examples["order"][3])  # 옵션이 있는 주문 예제
            
        elif screen_state == ScreenState.CONFIRM:
            # 주문 확인 화면에서는 결제, 취소 의도 예제
            examples.extend(self.examples["payment"])
            
        elif screen_state == ScreenState.SELECT_PAY:
            # 결제 수단 선택 화면에서는 결제 의도 예제
            examples.extend(self.examples["payment"])
            
        elif screen_state == ScreenState.PAY:
            # 결제 화면에서는 결제 의도 예제
            examples.extend(self.examples["payment"])
            
        else:
            # 기본적으로 모든 카테고리에서 하나씩
            examples.append(self.examples["order"][0])
            examples.append(self.examples["search"][0])
            examples.append(self.examples["option"][0])
            examples.append(self.examples["payment"][0])
            examples.append(self.examples["detail"][0])
        
        # 예제 포맷팅
        formatted_examples = []
        for example in examples:
            example_text = f"사용자: \"{example['input']}\"\n"
            example_text += f"분석 결과: ```json\n{json.dumps(example['output'], ensure_ascii=False, indent=2)}\n```"
            formatted_examples.append(example_text)
        
        return "\n\n".join(formatted_examples)