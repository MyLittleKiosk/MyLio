# app/services/intent/intent_recognizer.py
from typing import Dict, Any, List,Optional
import json
import re
import traceback
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI

from app.models.schemas import IntentType, ScreenState, Language
from app.services.menu_service import MenuService
from app.models.schemas import ResponseStatus
from app.utils.sanitize import sanitize_menus

class IntentRecognizer:
    """사용자 의도 인식 서비스"""
    
    def __init__(self, api_key: str, menu_service: MenuService):
        """인식기 초기화"""
        self.menu_service = menu_service
        
        # LLM 초기화
        self.llm = ChatOpenAI(
            model_kwargs={"api_key": api_key},
            model_name="gpt-4o", 
            temperature=0.05
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
        examples = self._select_examples(screen_state, language, session)
        
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
        result = self._parse_llm_response(response, store_id, session)
        
        # 디버깅 정보
        print(f"[의도 인식] 입력: '{text}', 인식 결과: {result}")
        
        # 장바구니 수정 키워드 확인 및 의도 오버라이드
        if self._is_cart_modify_intent(text, language) and session.get("cart"):
            result["intent_type"] = IntentType.CART_MODIFY
            
            # 액션 타입 결정
            if self._is_cart_remove_intent(text, language):
                result["action_type"] = "REMOVE"
            elif self._is_cart_quantity_update_intent(text, language):
                result["action_type"] = "QUANTITY"
                # 숫자 추출
                quantity_change = self._extract_quantity_change(text, language)
                result["quantity_change"] = quantity_change
            else:
                result["action_type"] = "UPDATE"
                
            # 메뉴 이름 추출
            menu_name = self._extract_menu_name_from_cart(text, session, language)
            if menu_name:
                result["menu_name"] = menu_name
                
            print(f"[의도 오버라이드] 장바구니 수정 의도 감지: {result}")
        
        # DetailProcessor가 없어도 영양 성분 관련 의도를 인식할 수 있도록
        elif self._is_detail_intent(text, language):
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
    
    # def _build_context(self, screen_state: str, store_id: int, store_menus: Dict[int, Dict[str, Any]], session: Dict[str, Any]) -> str:
    #     """상황에 맞는 컨텍스트 구성"""
    #     context_parts = []
        
    #     # 1. 메뉴 정보 요약 (모든 메뉴 포함)
    #     menu_list = list(store_menus.values())  # 모든 메뉴 포함
        
    #     # 카테고리별로 메뉴 그룹화
    #     categorized_menus = {}
    #     for menu in menu_list:
    #         category_id = menu.get("category_id")
    #         if category_id not in categorized_menus:
    #             categorized_menus[category_id] = []
    #         categorized_menus[category_id].append(menu)
        
    #     # 카테고리별로 메뉴 정보 구성
    #     for category_id, menus in categorized_menus.items():
    #         category_name = self._get_category_name(category_id, store_id) or f"카테고리 {category_id}"
    #         category_items = []
            
    #         for menu in menus:
    #             # 기본 메뉴 정보 (ID만 포함)
    #             menu_info = [f"{menu['name_kr']} [ID:{menu['id']}]"]
                
    #             # 옵션 정보 추가 (옵션 선택 시 필요)
    #             if menu.get('options') and screen_state == ScreenState.ORDER:
    #                 options_info = ["옵션:"]
    #                 for opt in menu['options']:
    #                     opt_id = opt.get('option_id', '')
    #                     opt_name = opt.get('option_name', '')
    #                     required = "필수" if opt.get('required', False) else "선택"
    #                     options_info.append(f"- {opt_name} [ID:{opt_id}] ({required})")
                        
    #                     # 옵션 상세 정보
    #                     if opt.get('option_details'):
    #                         detail_items = []
    #                         for detail in opt['option_details']:
    #                             detail_id = detail.get('id', '')
    #                             value = detail.get('value', '')
    #                             detail_items.append(f"  * {value} [ID:{detail_id}]")
    #                         options_info.extend(detail_items)
                    
    #                 menu_info.append("\n".join(options_info))
                
    #             category_items.append("\n".join(menu_info))
            
    #         context_parts.append(f"## {category_name}\n" + "\n\n".join(category_items))
        
    #     # 2. 장바구니 정보 (있는 경우)
    #     cart = session.get("cart", [])
    #     if cart:
    #         cart_summary = ["## 현재 장바구니"]
    #         for item in cart:
    #             option_text = ""
    #             if item.get("selected_options"):
    #                 option_strs = []
    #                 for opt in item["selected_options"]:
    #                     if opt.get("option_details"):
    #                         opt_value = opt["option_details"][0].get("value", "")
    #                         option_strs.append(f"{opt['option_name']}: {opt_value}")
    #                 if option_strs:
    #                     option_text = f" ({', '.join(option_strs)})"
    #             cart_summary.append(f"- {item['name']}{option_text} x {item['quantity']}개")
    #         context_parts.append("\n".join(cart_summary))
        
    #     # 3. 화면 상태별 추가 컨텍스트
    #     if screen_state == ScreenState.ORDER and session.get("last_state", {}).get("menu"):
    #         menu = session["last_state"]["menu"]
    #         context_parts.append(f"## 현재 선택된 메뉴\n{menu['name_kr']}")
        
    #     return "\n\n".join(context_parts)
    
    def _build_context(
            self,
            screen_state: str,
            store_id: int,
            store_menus: Dict[int, Dict[str, Any]],
            session: Dict[str, Any]
    ) -> str:
        """LLM 프롬프트에 넣을 컨텍스트 텍스트 생성"""

        context_parts: list[str] = []

        # ------------------------------------------------------------------ #
        # 1) 매장 전체 메뉴 + 옵션 요약
        # ------------------------------------------------------------------ #
        menu_list = list(store_menus.values())              # 모든 메뉴
        categorized: dict[int, list[dict]] = {}
        for menu in menu_list:
            categorized.setdefault(menu.get("category_id"), []).append(menu)

        for category_id, menus in categorized.items():
            cat_name = self._get_category_name(category_id, store_id) or f"카테고리 {category_id}"
            cat_lines: list[str] = []

            for menu in menus:
                menu_name = (
                    menu.get("name_kr")
                    or menu.get("name")
                    or menu.get("menu_name")
                    or f"메뉴ID {menu.get('id')}"
                )
                menu_lines = [f"{menu_name} [ID:{menu.get('id')}]"]

                # 옵션 정보 – ORDER 화면일 때만 상세 전송
                if screen_state == ScreenState.ORDER and menu.get("options"):
                    opt_lines = ["옵션:"]
                    for opt in menu["options"]:
                        opt_name = opt.get("option_name", "")
                        opt_id   = opt.get("option_id", "")
                        required = "필수" if opt.get("required") else "선택"
                        opt_lines.append(f"- {opt_name} [ID:{opt_id}] ({required})")

                        # 옵션 상세
                        for d in opt.get("option_details", []):
                            v = d.get("value", "")
                            did = d.get("id", "")
                            opt_lines.append(f"  * {v} [ID:{did}]")
                    menu_lines.append("\n".join(opt_lines))

                cat_lines.append("\n".join(menu_lines))

            context_parts.append(f"## {cat_name}\n" + "\n\n".join(cat_lines))

        # ------------------------------------------------------------------ #
        # 2) 장바구니 요약
        # ------------------------------------------------------------------ #
        cart = session.get("cart", [])
        if cart:
            cart_lines = ["## 현재 장바구니"]
            for item in cart:
                item_name = (
                    item.get("name")
                    or item.get("name_kr")
                    or item.get("menu_name")
                    or f"메뉴ID {item.get('menu_id')}"
                )
                # 옵션 요약
                opt_text = ""
                if item.get("selected_options"):
                    vals = []
                    for opt in item["selected_options"]:
                        if opt.get("option_details"):
                            val = opt["option_details"][0].get("value", "")
                            vals.append(f"{opt.get('option_name')}: {val}")
                    if vals:
                        opt_text = f" ({', '.join(vals)})"
                cart_lines.append(f"- {item_name}{opt_text} x {item.get('quantity', 1)}개")
            context_parts.append("\n".join(cart_lines))

        # ------------------------------------------------------------------ #
        # 3) 주문 화면이라면, 현재 옵션을 고르는 메뉴 정보 추가
        # ------------------------------------------------------------------ #
        if (
            screen_state == ScreenState.ORDER
            and session.get("last_state", {}).get("menu")
        ):
            menu = session["last_state"]["menu"]
            current_name = (
                menu.get("name_kr")
                or menu.get("name")
                or menu.get("menu_name")
                or f"메뉴ID {menu.get('menu_id')}"
            )
            context_parts.append(f"## 현재 선택된 메뉴\n{current_name}")

        # ------------------------------------------------------------------ #
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
    
    def _parse_llm_response(self, response: str, store_id: int = 1,
        session: Dict[str, Any] | None = None) -> Dict[str, Any]:
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
            
            # 결제 수단 표준화 - KAKAOPAY는 PAY로 변환
            if result.get("intent_type") == IntentType.PAYMENT and result.get("payment_method"):
                pm = re.sub(r"[\s_]+", "", str(result["payment_method"]).upper())
                if pm in ("KAKAOPAY", "KAKAO","KAKAO_PAY","KAKAO PAY"):
                    result["payment_method"] = "PAY"

            # OPTION_SELECT 일 때 menu_id / menu_name 이 없어도 버리지 않는다
            if result.get("intent_type") == "OPTION_SELECT":
                # 메뉴 배열이 아예 없으면 빈 dict 하나라도 넣어 옵션을 살림
                if not result.get("menus"):
                    result["menus"] = [{}]

                # ▼ session 이 있을 때만 last_state 보강
                if session and result["menus"] and not result["menus"][0].get("menu_name"):
                    last_menu = session.get("last_state", {}).get("menu", {})
                    result["menus"][0]["menu_name"] = (
                        last_menu.get("name") or last_menu.get("name_kr") or ""
                    )

            # ② menu_name 이 없으면 세션 last_state 에서 보충
            if (
                result.get("intent_type") == "OPTION_SELECT"
                and result["menus"]
                and not result["menus"][0].get("menu_name")
            ):
                last_menu = session.get("last_state", {}).get("menu", {})
                result["menus"][0]["menu_name"] = (
                    last_menu.get("name") or last_menu.get("name_kr") or ""
                )

            # SEARCH 의도일 때 메뉴 처리
            if result.get("intent_type") == "SEARCH":
                # 메뉴 정보 로드
                store_menus = self.menu_service.get_store_menus(store_id)
                
                # LLM이 반환한 menus 배열이 있을 경우
                if "menus" in result and isinstance(result["menus"], list):
                    processed_menus = []
                    
                    for menu in result["menus"]:
                        # menu_id가 이미 있는 경우
                        if "menu_id" in menu:
                            processed_menus.append(menu)
                        # menu_name만 있는 경우, ID 찾아서 추가
                        elif "menu_name" in menu:
                            menu_name = menu["menu_name"]
                            found_menu = self.menu_service.find_menu_by_name(menu_name, store_id)
                            
                            if found_menu:
                                menu["menu_id"] = found_menu["id"]
                                processed_menus.append(menu)
                            else:
                                # 유사한 이름 찾기 시도
                                for menu_id, menu_info in store_menus.items():
                                    if menu_name.lower() in menu_info["name_kr"].lower():
                                        menu["menu_id"] = menu_id
                                        processed_menus.append(menu)
                                        break
                    
                    result["menus"] = processed_menus
                else:
                    result["menus"] = []

            # text
            if result.get("menus"):
                store_menus = self.menu_service.get_store_menus(store_id)
                result["menus"] = sanitize_menus(result["menus"], store_menus)

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
        1. 사용자의 의도 (ORDER, SEARCH, OPTION_SELECT, PAYMENT, CART_MODIFY, DETAIL, UNKNOWN 중 하나)
        2. 주문인 경우:
        - 주문하려는 모든 메뉴를 개별적으로 인식하세요. 
        - 사용자가 "아아 하나랑 카페라떼 하나 주세요"처럼 여러 메뉴를 동시에 주문할 경우, 각 메뉴를 별도 항목으로 추가하세요.
        - 각 메뉴의 수량, 옵션 정보를 정확히 추출하세요.
        - 예: "아메리카노 2개 주는데 하나는 샷추가해줘" -> 두 개의 아메리카노 메뉴 항목 생성, 두 번째 항목에만 샷추가 옵션 적용

        3. 의도별 필요한 추가 정보:
           - ORDER: 주문하려는 메뉴명, 수량, 옵션 정보
           - SEARCH: 검색 쿼리
           - OPTION_SELECT: 선택한 옵션 이름과 값
           - PAYMENT: 결제 방법
           - CART_MODIFY: 수정할 메뉴명, 액션 타입(UPDATE/REMOVE/QUANTITY), 새 옵션 또는 수량 변경값
           - DETAIL: 정보를 요청한 메뉴명, 요청한 정보 유형(영양성분, 원재료 등)

        4. 화면 상태에 따른 의도 인식 규칙:
           - MAIN 화면에서 메뉴 옵션 변경 요청("아메리카노 핫으로 변경해줘" 등)은 항상 CART_MODIFY로 인식
           - MAIN 화면에서 메뉴 삭제/수량 변경 요청도 CART_MODIFY로 인식
           - ORDER 화면에서는 옵션 선택 요청을 OPTION_SELECT로 인식
           - 현재 화면이 MAIN이고 장바구니에 이미 있는 메뉴에 대한 변경 요청은 CART_MODIFY로 인식

        5. 메뉴명 교정 규칙:
        - "아아/아이스아메리카노" → "아메리카노" + 옵션:"ICE"
        - "따아/핫아메리카노" → "아메리카노" + 옵션:"HOT"
        - "카페라떼/카페라테/라떼" → "카페 라떼"
        - "바닐라라떼/바닐라라테" → "바닐라 라떼"
        - "아샷추" -> "복숭아 아이스티"

        6. 옵션 매핑 규칙:
        - "아이스/차가운/아아/아바라/아샷추" → 온도 옵션:"ICE"
        - "따뜻한/뜨거운/따아/하스로" → 온도 옵션:"Hot"
        - "작은/스몰/S" → 사이즈 옵션:"S"
        - "중간/미디엄/M" → 사이즈 옵션:"M"
        - "큰/라지/L" → 사이즈 옵션:"L"
        - json으로 값을 넘길때 반드시 menu context의 내용과 동일한 내용을 전달하세요. "얼음 많이" -> 얼음량 옵션 : "얼음 많이"
        - 새로 만들어낸 숫자(임의의 ID)는 절대로 사용하지 마세요.
        
        7. 취소 규칙:
        - 현재 화면 상태가 "ORDER"이고 아직 선택하지 못한 옵션이 남아있는데 다른 메뉴를 선택하려는 경우 -> "아직 메뉴가 선택되지 않았어요. 옵션을 선택해주세요."
        - screen_state가 OPTION 일 때 "취소","메뉴 추가","그만","삭제"와 같이 로직을 벗어나려고 한다면 "주문하고 있던 메뉴가 사라져요."라고 응답을 내보내고 screen_state는 MAIN으로 해주세요.
        - screen_state가 PAYMENT/SELECT_PAY 일 때 "취소","메뉴 추가","그만","삭제"와 같이 로직을 벗어나려고 한다면 "결제가 취소돼요."라고 응답을 내보내고 screen_State를 MAIN으로 해주세요.
        
        8. 응답 규칙:
        - 메뉴가 여러개인 경우 모든 메뉴에 대해서 응답값을 생성하지 말고 가장 첫번째에 있는 메뉴에 대해 필수 옵션값을 찾아내서 응답값을 만들어주세요.
        - 여려가지 메뉴를 찾아내는 과정에서 만약 여러개의 메뉴가 히스토리에 남아있는 경우 작은거요 한 후에 장바구니에 담았다고 하지 말고 그 다음 메뉴에 대해 옵션값을 적용할 수 있도록 응답값을 생성해주세요.
        - "말씀해 주세요". -> "알려주세요"와 같이 응답을 생성할 때는 꼭 해요체를 써주세요.
        
        9. 검색 규칙:
        - 디카페인을 물어보면 카페인이 들어가지 않은 메뉴를 찾아야해요. 메뉴 명에 "디카페인 아메리카노"와 같이 메뉴명에 디카페인이 들어간 메뉴를 찾아주세요.
        - 디카페인 아메리카노와 아메리카노는 다른 메뉴에요. 디카페인음료를 물어볼때 "아메리카노", "콜드브루"는 제외시키고 "디카페인 아메리카노", "디카페인 콜드브루"와 같은 메뉴를 가져와야 해요.
        - 전체 메뉴를 보여달라고 하면 전체 메뉴 리스트를 전부 보내야 합니다.
        - 검색된 메뉴의 이름과 menu_id를 함께 보내야 합니다.

        10. 결제 규칙:
        - payment_method의 경우 반드시 "CARD","MOBILE", "GIFT", "PAY" 중 하나여야 합니다.
        - 카카오페이, 카카오 페이 경우 PAY로 들어가야 합니다.

        주의: 응답을 생성할 때 템플릿 문자열이 아닌 실제 사용자에게 보여질 자연스러운 응답을 직접 생성해주세요.
        "감자탕 있어?", "화장실이 어디야?" 와 같이 제공된 메뉴 이외의 질문을 한다면 "죄송하지만 대답할 수 없는 질문이네요. 카페와 관련된 질문을 해주시면 대답해드릴 수 있어요."라고 답변하고 screen_state는 MAIN으로 해주세요.
        - 메뉴ID, 옵션ID, 옵션상세ID, 옵션value는 반드시 컨텍스트에서 제공된 값으로 해주세요.
        - 새로 만들어낸 숫자(임의의 ID)는 절대로 사용하지 마세요.

        모든 옵션을 누락 없이 JSON으로 추출해 주세요.
        예시:
        "샷 추가 해서 얼음 많이 큰걸로 두개 줘 우유는 오트 우유로 바꿔줘 뜨거운거"
        → options 필드에 '샷옵션', '얼음량', '사이즈', '우유변경', '온도'가 모두 포함되어야 합니다. 이때 반드시 menu context에서 받은 실제 값으로 전달하세요.
        
        # 복합 주문 예제
        사용자: "아아 두개 주는데 하나는 샷추가해줘"
        분석 결과:
        ```json
        {{
        "intent_type": "ORDER",
        "confidence": 0.9,
        "menus": [
            {{
            "menu_id": 101,
            "menu_name": "아메리카노",
            "quantity": 1,
            "options": [
                {{
                "option_id": 102,
                "option_name": "온도",
                "option_detail_id": 1005,
                "option_value": "Ice"
                }}
            ]
            }},
            {{
            "menu_id": 101,
            "menu_name": "아메리카노",
            "quantity": 1,
            "options": [
                {{
                "option_id": 102,
                "option_name": "온도",
                "option_detail_id": 1005,
                "option_value": "Ice"
                }},
                {{
                "option_id": 105,
                "option_name": "샷옵션"
                "option_detail_id": 1017,
                "option_value": "샷 개 추가"
                }}
            ]
            }}
        ],
        "post_text": "아이스 아메리카노 두개 주는데 하나는 샷추가해줘",
        "reply": "아이스 아메리카노 두 개 중 하나는 샷 추가 맞으신가요? 사이즈는 어떻게 해드릴까요?"
        }}
        ```

        # 응답 형식
        분석 결과를 다음 JSON 형식으로 반환하세요:
        ```json
        {{
          "intent_type": "ORDER/SEARCH/PAYMENT/DETAIL/OPTION_SELECT/UNKNOWN",
          "confidence": 0.0~1.0 사이의 신뢰도 점수,
          "menus": [ // ORDER 의도에만 사용
            {{
              "menu_id": 메뉴 ID, (반드시 메뉴 컨텍스트에 넘긴 메뉴의 id랑 일치해야 함)
              "menu_name": "메뉴 이름",
              "quantity": 수량,
              "options": [
                {{
                  "option_id": 옵션 ID, (반드시 메뉴 컨텍스트에 넘김 옴션의 id랑 일치해야 함)
                  "option_name": "옵션 이름 (예: 온도, 사이즈)",
                  "option_detail_id": 옵션 상세 ID, (반드시 메뉴 컨텍스트에 넘긴 옵션 상세의 id랑 일치해야 함)
                  "option_value": "옵션 값 (예: Ice, Hot, S, M, L)"
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
                                "menu_id": 103,
                                "menu_name": "바닐라라떼",
                                "quantity": 1,
                                "options": [
                                    {
                                        "option_id": 102,
                                        "option_name": "온도",
                                        "option_detail_id": 1005,
                                        "option_value": "Ice"
                                    }
                                ]
                            }
                        ],
                        "post_text": "아바라 하나 주세요",
                        "reply": "바닐라 라떼의 옵션을 선택해주세요."
                    
                    }
                },
                {
                    "input": "아샷추 하나 주세요",
                    "output": {
                        "intent_type": "ORDER",
                        "confidence": 0.9,
                        "menus": [
                            {
                                "menu_id": 113,
                                "menu_name": "아이스티",
                                "quantity": 1,
                                "options": [
                                    {
                                        "option_id": 102,
                                        "option_name": "온도",
                                        "option_detail_id": 1005,
                                        "option_value": "Ice"
                                    },
                                    {
                                        "option_id": 105,
                                        "option_name": "샷옵션",
                                        "option_detail_id": 1017,
                                        "option_value": "샷 1개 추가"
                                    }
                                ]
                            }
                        ],
                        "post_text": "아샷추 하나 주세요",
                        "reply": "아이스티의 옵션을 선택해주세요."
                    }
                },
                {
                    "input": "아아 하나 주세요",
                    "output": {
                        "intent_type": "ORDER",
                        "confidence": 0.9,
                        "menus": [
                            {
                                "menu_id": 101,
                                "menu_name": "아메리카노",
                                "quantity": 1,
                                "options": [
                                    {
                                        "option_id": 102,
                                        "option_name": "온도",
                                        "option_detail_id": 1005,
                                        "option_value": "Ice"
                                    }
                                ]
                            }
                        ],
                        "post_text": "아아 하나 주세요",
                        "reply": "아메리카노의 옵션을 선택해주세요."
                    }
                },
                {
                    "input": "따아 한잔이요",
                    "output": {
                        "intent_type": "ORDER",
                        "confidence": 0.9,
                        "menus": [
                            {
                                "menu_id": 101,
                                "menu_name": "아메리카노",
                                "quantity": 1,
                                "options": [
                                    {
                                        "option_id": 102,
                                        "option_name": "온도",
                                        "option_detail_id": 1006,
                                        "option_value": "Hot"
                                    }
                                ]
                            }
                        ],
                        "post_text": "따뜻한 아메리카노 한 잔이요.",
                        "reply": "아메리카노의 옵션을 선택해주세요."
                    }
                },
                {
                    "input": "큰 사이즈 아아 한잔이요",
                    "output": {
                        "intent_type": "ORDER",
                        "confidence": 0.9,
                        "menus": [
                            {
                                "menu_id": 101,
                                "menu_name": "아메리카노",
                                "quantity": 1,
                                "options": [
                                    {
                                        "option_id": 102,
                                        "option_name": "온도",
                                        "option_detail_id": 1005,
                                        "option_value": "Ice"
                                    },
                                    {
                                        "option_id": 101,
                                        "option_name": "사이즈",
                                        "option_detail_id": 1003,
                                        "option_value": "L"
                                    }
                                ]
                            }
                        ],
                        "post_text": "큰 사이즈 아아 한잔이요",
                        "reply": "주문하신 메뉴를 장바구니에 담았어요."
                    }
                }
            ],
            
            # 옵션 선택 예제
            "option": [
                {
                    "input": "샷 하나 추가해주고 아이스로 해줘",
                    "output": {
                        "intent_type": "OPTION_SELECT",
                        "confidence": 0.9,
                        "menus": [
                            {
                                "options": [
                                    {
                                        "option_id": 102,
                                        "option_name": "온도",
                                        "option_detail_id": 1005,
                                        "option_value": "Ice"
                                    },
                                    {
                                        "option_id": 105,
                                        "option_name": "샷옵션",
                                        "option_detail_id": 1017,
                                        "option_value": "샷 1개 추가"
                                    }
                                ]
                            }
                        ],
                        "post_text": "샷 하나 추가해주고 아이스로 해줘",
                        "reply": "주문하신 메뉴를 장바구니에 담았습니다."
                    }
                },
                {
                    "input": "아이스로 해주세요",
                    "output": {
                        "intent_type": "OPTION_SELECT",
                        "confidence": 0.9,
                        "menus": [
                            {
                                "options": [
                                    {
                                        "option_id": 102,
                                        "option_name": "온도",
                                        "option_detail_id": 1005,
                                        "option_value": "Ice"
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
                                        "option_id": 101,
                                        "option_name": "사이즈",
                                        "option_detail_id": 1003,
                                        "option_value": "L"
                                    }
                                ]
                            }
                        ],
                        "post_text": "라지 사이즈로 주세요.",
                        "reply": "주문하신 메뉴를 장바구니에 담았어요."
                    }
                },
                {
                    "input": "하스로 줘",
                    "output": {
                        "intent_type": "OPTION_SELECT",
                        "confidence": 0.9,
                        "menus": [
                            {
                                "options": [
                                    {
                                        "option_id": 102,
                                        "option_name": "온도",
                                        "option_detail_id": 1004,
                                        "option_value": "HOT"
                                    }
                                ]
                            }
                        ],
                        "post_text": "핫으로 줘",
                        "reply": "핫으로 준비할게요.사이즈는 어떻게 해드릴까요?"
                    }
                },
                {
                    "input": "샷 추가하고 아이스로 얼음 많이 넣어줘, 라지 사이즈로 할게",
                    "output": {
                        "intent_type": "OPTION_SELECT",
                        "confidence": 0.9,
                        "menus": [
                            {
                                "options": [
                                    {
                                        "option_id": 102,
                                        "option_name": "온도",
                                        "option_detail_id": 1005,
                                        "option_value": "Ice"
                                    },
                                    {
                                        "option_id": 105,
                                        "option_name": "샷옵션",
                                        "option_detail_id": 1017,
                                        "option_value": "샷 1개 추가"
                                    },
                                    {
                                        "option_id": 103,
                                        "option_name": "얼음량",
                                        "option_detail_id": 1009,
                                        "option_value": "얼음 많이"
                                    },
                                    {
                                        "option_id": 101,
                                        "option_name": "사이즈",
                                        "option_detail_id": 1003,
                                        "option_value": "L"
                                    }
                                ]
                            }
                        ],
                        "post_text": "샷 추가하고 아이스로 얼음 많이 넣어줘, 엠 사이즈로 할게",
                        "reply": "주문하신 메뉴를 장바구니에 넣었어요."
                    }
                }
            ],
            
            # 검색 예제
            "search": [
                {
                    "input": "전체 메뉴 보여줘",
                    "output": {
                        "intent_type": "SEARCH",
                        "confidence": 0.9,
                        "search_query": "전체 메뉴",
                        "menus": [
                            {"menu_id": 17},
                            {"menu_id": 18},
                            {"menu_id": 19},
                            {"menu_id": 20},
                            {"menu_id": 21},
                            {"menu_id": 22},
                            {"menu_id": 23},
                            {"menu_id": 24},
                            {"menu_id": 25},
                            
                        ],  # 컨텍스트의 모든 메뉴 ID가 들어갈 자리
                        "post_text": "전체 메뉴 보여줘",
                        "reply": "전체 메뉴를 안내해드릴게요."
                    }
                },
                {
                    "input": "디카페인 메뉴 있어?",
                    "output": {
                        "intent_type": "SEARCH",
                        "confidence": 0.9,
                        "search_query": "디카페인 메뉴",
                        "menus": [
                            {"menu_id": 15},  # 디카페인 아메리카노
                            {"menu_id": 16},  # 디카페인 콜드브루
                            {"menu_id": 17}   # 디카페인 콜드브루 라떼
                        ],
                        "post_text": "디카페인 있어?",
                        "reply": "디카페인 메뉴를 보여드릴게요."
                    }
                },
                {
                    "input": "차 종류 있어?",
                    "output": {
                        "intent_type": "SEARCH",
                        "confidence": 0.9,
                        "search_query": "차 종류",
                        "menus": [
                            {"menu_name": "페퍼민트", "menu_id": 114},
                            {"menu_name": "히비스커스", "menu_id": 115},
                            {"menu_name": "녹차", "menu_id": 116},
                            {"menu_name": "얼그레이", "menu_id": 117},
                            {"menu_name": "루이보스", "menu_id": 118},
                            {"menu_name": "한라봉차", "menu_id": 119}
                        ],
                        "post_text": "차 종류 있어?",
                        "reply": "차 종류는 페퍼민트, 히비스커스, 녹차, 얼그레이, 루이보스, 한라봉차가 있어요."
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
            ],
            
            # 장바구니 수정 예제 추가
            "cart_modify": [
                {
                    "input": "장바구니에 담긴거 삭제해줘",
                    "output": {
                        "intent_type": "CART_MODIFY",
                        "confidence": 0.9,
                        "action_type": "REMOVE",
                        "menu_name": "",  # 비어있으면 전체 삭제
                        "post_text": "장바구니에 담긴거 삭제해줘",
                        "reply": "장바구니를 비웠어요."
                    }
                },
                {
                    "input": "아메리카노 빼줘",
                    "output": {
                        "intent_type": "CART_MODIFY",
                        "confidence": 0.9,
                        "action_type": "REMOVE",
                        "menu_name": "아메리카노",
                        "post_text": "아메리카노 빼줘",
                        "reply": "아메리카노를 장바구니에서 삭제했어요."
                    }
                },
                {
                    "input": "방금 담은 음료 핫으로 바꿔줘",
                    "output": {
                        "intent_type": "CART_MODIFY",
                        "confidence": 0.9,
                        "action_type": "UPDATE",
                        "menu_name": "",  # 가장 최근 담긴 메뉴
                        "new_options": [
                            {
                                "option_id": 102,
                                "option_name": "온도",
                                "is_selected": True,
                                "option_details": [
                                    {
                                        "id": 1004,
                                        "value": "HOT",
                                        "additional_price": 0
                                    }
                                ]
                            }
                        ],
                        "post_text": "방금 담은 음료 핫으로 바꿔줘",
                        "reply": "음료의 옵션을 HOT으로 변경했어요."
                    }
                },
                {
                    "input": "아메리카노 2개 더 추가해줘",
                    "output": {
                        "intent_type": "CART_MODIFY",
                        "confidence": 0.9,
                        "action_type": "QUANTITY",
                        "menu_name": "아메리카노",
                        "quantity_change": 2,
                        "post_text": "아메리카노 2개 더 추가해줘",
                        "reply": "아메리카노 2개를 더 추가했어요."
                    }
                },
                {
                    "input": "아메리카노 하스로 변경해줘",
                    "output": {
                        "intent_type": "CART_MODIFY",
                        "confidence": 0.9,
                        "action_type": "UPDATE",
                        "menu_name": "아메리카노",
                        "new_options": [
                            {
                                "option_id": 102,
                                "option_name": "온도",
                                "is_selected": True,
                                "option_details": [
                                    {
                                        "id": 1004,
                                        "value": "HOT",
                                        "additional_price": 0
                                    }
                                ]
                            }
                        ],
                        "post_text": "아메리카노 따뜻하게 변경해줘",
                        "reply": "아메리카노의 온도를 HOT으로 변경했어요."
                    }
                },
                {
                    "input": "블루베리 스무디 작은걸로 변경해줘",
                    "output": {
                        "intent_type": "CART_MODIFY",
                        "confidence": 0.9,
                        "action_type": "UPDATE",
                        "menu_name": "블루베리 스무디",
                        "new_options": [
                            {
                                "option_id": 101,
                                "option_name": "사이즈",
                                "is_selected": True,
                                "option_details": [
                                    {
                                        "id": 1001,
                                        "value": "S",
                                        "additional_price": 0
                                    }
                                ]
                            }
                        ],
                        "post_text": "블루베리 스무디 작은 사이즈로 변경해줘",
                        "reply": "블루베리 스무디의 사이즈를 S로 변경했어요."
                    }
                }
            ]
        }
    
    def _select_examples(self, screen_state: str, language: str, session: Dict[str, Any] = None) -> str:
        """화면 상태에 맞는 Few-shot 예제 선택"""
        examples = []
        
        # 화면 상태에 따른 예제 선택
        if screen_state == ScreenState.MAIN:
            # 메인 화면에서는 주문, 검색, 상세정보, 장바구니 수정 의도 예제
            examples.extend(self.examples["order"][:2])
            examples.append(self.examples["search"][0])
            examples.append(self.examples["detail"][0])
            examples.extend(self.examples["cart_modify"][:2])  # 장바구니 수정 예제 추가
            
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
            examples.append(self.examples["cart_modify"][0])
        
        # 화면 상태와 관계없이 항상 장바구니 수정 예제 포함 (장바구니에 메뉴가 있는 경우)
        if session and session.get("cart"):
            if screen_state != ScreenState.MAIN:  # 메인 화면은 이미 포함했음
                examples.extend(self.examples["cart_modify"][:2])
        
        # 예제 포맷팅
        formatted_examples = []
        for example in examples:
            example_text = f"사용자: \"{example['input']}\"\n"
            example_text += f"분석 결과: ```json\n{json.dumps(example['output'], ensure_ascii=False, indent=2)}\n```"
            formatted_examples.append(example_text)
        
        return "\n\n".join(formatted_examples)

    def generate_option_selection_response(self, menu: Dict[str, Any], option: Dict[str, Any], language: str) -> str:
        """옵션 선택 안내 응답 생성"""
        menu_name = menu.get("name", "")
        option_name = option.get("option_name", "")
        options_str = ", ".join(detail.get("value", "") for detail in option.get("option_details", []))
        
        # 컨텍스트 구성
        context = {
            "menu_name": menu_name,
            "option_name": option_name,
            "options_values": options_str,
            "language": language
        }
        
        # LLM으로 응답 생성
        # 예: "아메리카노를 주문하셨네요. 사이즈를 선택해주세요. (S, M, L 중에서)"
        prompt = f"""
        사용자가 카페에서 {menu_name}를 주문하고 있습니다.
        현재 {option_name} 옵션을 선택해야 합니다.
        선택 가능한 옵션은 {options_str}입니다.
        사용자의 언어는 {language}입니다.
        
        이 상황에서 옵션 선택을 안내하는 자연스러운 메시지를 생성해주세요. 해요체로 응답을 생성해주세요.
        """
        
        # LLM 응답 생성 시도
        try:
            response = self._generate_llm_response(prompt)
            if response and len(response) > 0:
                return response
        except Exception as e:
            print(f"LLM 응답 생성 오류: {e}")
        
        # 실패 시 기본 응답 사용
        return f"{menu_name}를 선택하셨네요. 필수 옵션을 선택해주세요."

    def _is_cart_modify_intent(self, text: str, language: str) -> bool:
        """장바구니 수정 의도인지 확인"""
        text_lower = text.lower()
        
        if language == Language.KR:
            cart_keywords = ["장바구니", "빼줘", "빼", "지워줘", "삭제", "취소", "변경", "바꿔", "수정", "추가"]
            action_keywords = ["빼", "삭제", "취소", "변경", "바꿔", "수정", "하나 더", "한개 더", "두개 더", "2개 더"]
            
            # "방금 담은" 키워드는 장바구니 수정 의도를 강하게 나타냄
            if "방금 담은" in text_lower:
                return True
                
            # 장바구니 키워드와 동작 키워드가 함께 있는 경우
            if any(keyword in text_lower for keyword in cart_keywords) and any(keyword in text_lower for keyword in action_keywords):
                return True
                
            # "빼줘", "삭제해줘"와 같은 직접적인 표현
            remove_phrases = ["빼줘", "빼 줘", "지워줘", "지워 줘", "삭제해줘", "삭제해 줘", "취소해줘", "빼도 돼", "빼도 될까"]
            if any(phrase in text_lower for phrase in remove_phrases):
                return True
                
            # "변경해줘", "바꿔줘"와 같은 표현
            update_phrases = ["변경해줘", "변경해 줘", "바꿔줘", "바꿔 줘", "수정해줘", "핫으로 바꿔", "아이스로 바꿔"]
            if any(phrase in text_lower for phrase in update_phrases):
                return True
                
            # "하나 더", "추가해줘"와 같은 표현
            quantity_phrases = ["하나 더", "한개 더", "두개 더", "2개 더", "추가해줘", "더 넣어줘"]
            if any(phrase in text_lower for phrase in quantity_phrases):
                return True
        
        elif language == Language.EN:
            cart_keywords = ["cart", "remove", "delete", "cancel", "change", "modify", "more"]
            action_keywords = ["remove", "delete", "cancel", "change", "modify", "add one more", "add two more"]
            
            if any(keyword in text_lower for keyword in cart_keywords) and any(keyword in text_lower for keyword in action_keywords):
                return True
                
            remove_phrases = ["remove", "delete", "cancel", "take out", "remove from cart"]
            if any(phrase in text_lower for phrase in remove_phrases):
                return True
                
            update_phrases = ["change", "switch", "make it hot", "make it cold", "make it large"]
            if any(phrase in text_lower for phrase in update_phrases):
                return True
                
            quantity_phrases = ["one more", "add more", "two more", "another"]
            if any(phrase in text_lower for phrase in quantity_phrases):
                return True
                
        return False
        
    def _is_cart_remove_intent(self, text: str, language: str) -> bool:
        """장바구니에서 항목 삭제 의도인지 확인"""
        text_lower = text.lower()
        
        if language == Language.KR:
            remove_keywords = ["빼줘", "빼 줘", "지워줘", "지워 줘", "삭제", "취소", "없애", "지워", "비워"]
            return any(keyword in text_lower for keyword in remove_keywords)
        elif language == Language.EN:
            remove_keywords = ["remove", "delete", "cancel", "take out", "remove from cart"]
            return any(keyword in text_lower for keyword in remove_keywords)
            
        return False
        
    def _is_cart_quantity_update_intent(self, text: str, language: str) -> bool:
        """장바구니 항목 수량 변경 의도인지 확인"""
        text_lower = text.lower()
        
        if language == Language.KR:
            quantity_keywords = ["하나 더", "한개 더", "두개 더", "2개 더", "3개 더", "개 추가", "더 넣어", "추가해"]
            return any(keyword in text_lower for keyword in quantity_keywords)
        elif language == Language.EN:
            quantity_keywords = ["one more", "two more", "add more", "add another", "more of", "additional"]
            return any(keyword in text_lower for keyword in quantity_keywords)
            
        return False
        
    def _extract_quantity_change(self, text: str, language: str) -> int:
        """텍스트에서 수량 변경 추출"""
        text_lower = text.lower()
        
        # 수량 감소 키워드 확인
        decrease = False
        if language == Language.KR and any(k in text_lower for k in ["줄여", "제거", "덜", "하나 뺄게"]):
            decrease = True
        elif language == Language.EN and any(k in text_lower for k in ["reduce", "less", "fewer", "remove one"]):
            decrease = True
            
        # 숫자 추출
        import re
        
        if language == Language.KR:
            # 한국어 숫자 처리
            number_mapping = {
                "한": 1, "하나": 1, "한개": 1, "한잔": 1,
                "두": 2, "둘": 2, "두개": 2, "두잔": 2,
                "세": 3, "셋": 3, "세개": 3, "세잔": 3,
                "네": 4, "넷": 4, "네개": 4, "네잔": 4,
                "다섯": 5, "다섯개": 5, "다섯잔": 5
            }
            
            for word, number in number_mapping.items():
                if word in text_lower:
                    return -number if decrease else number
                    
            # 숫자 형태 추출
            matches = re.findall(r'(\d+)(?:개|잔)?', text_lower)
            if matches:
                return -int(matches[0]) if decrease else int(matches[0])
                
        elif language == Language.EN:
            # 영어 숫자 처리
            number_mapping = {
                "one": 1, "a": 1, "an": 1, "single": 1,
                "two": 2, "couple": 2, "pair": 2,
                "three": 3, "four": 4, "five": 5
            }
            
            for word, number in number_mapping.items():
                if word in text_lower:
                    return -number if decrease else number
                    
            # 숫자 형태 추출
            matches = re.findall(r'(\d+)', text_lower)
            if matches:
                return -int(matches[0]) if decrease else int(matches[0])
                
        # 기본값: 추가는 1, 감소는 -1
        return -1 if decrease else 1
        
    def _extract_menu_name_from_cart(self, text: str, session: Dict[str, Any], language: str) -> Optional[str]:
        """장바구니 수정 요청에서 메뉴 이름 추출"""
        text_lower = text.lower()
        cart = session.get("cart", [])
        
        if not cart:
            return None
        
        # 장바구니에 있는 모든 메뉴 이름
        menu_names = [item.get("name", "").lower() for item in cart]
        
        # "방금 담은" 키워드가 있으면 가장 최근 메뉴 반환
        if language == Language.KR and ("방금" in text_lower or "마지막" in text_lower):
            return cart[-1].get("name")
        elif language == Language.EN and ("last" in text_lower or "recent" in text_lower or "just added" in text_lower):
            return cart[-1].get("name")
            
        # 텍스트에서 메뉴 이름 찾기
        for menu_name in menu_names:
            if menu_name in text_lower:
                # 일치하는 메뉴 찾기
                for item in cart:
                    if item.get("name", "").lower() == menu_name:
                        return item.get("name")
        
        # 부분 일치 시도
        for item in cart:
            name = item.get("name", "").lower()
            for part in name.split():
                if part in text_lower and len(part) > 1:  # 최소 2자 이상인 단어만 고려
                    return item.get("name")
        
        # 메뉴 이름을 추출하지 못한 경우, 가장 최근에 추가된 메뉴 반환
        return cart[-1].get("name") if cart else None