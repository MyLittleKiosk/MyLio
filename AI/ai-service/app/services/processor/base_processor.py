# app/services/processor/base_processor.py
from typing import Dict, Any, Optional, List
import json
import re
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI

from app.models.schemas import IntentType, ScreenState, Language, ResponseStatus
from app.services.menu_service import MenuService
from app.services.response_service import ResponseService
from app.services.redis_session_manager import RedisSessionManager

class BaseProcessor:
    """기본 프로세서 클래스"""
    
    def __init__(self, api_key: str, menu_service: MenuService, response_service: ResponseService, session_manager: RedisSessionManager):
        """프로세서 초기화"""
        self.menu_service = menu_service
        self.response_service = response_service
        self.session_manager = session_manager
        
        # LLM 초기화
        self.llm = ChatOpenAI(
            model_kwargs={"api_key": api_key},
            model_name="gpt-4.1", 
            temperature=0.3
        )
        
        # Few-shot 학습 예제
        self.examples = self._load_examples()
    
    def process(self, intent_data: Dict[str, Any], text: str, language: str, screen_state: str, store_id: int, session: Dict[str, Any]) -> Dict[str, Any]:
        """의도 처리 메인 함수"""
        raise NotImplementedError("이 메서드는 하위 클래스에서 구현해야 합니다.")
    
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
    
    def _get_prompt_template(self) -> PromptTemplate:
        """프롬프트 템플릿 정의"""
        raise NotImplementedError("이 메서드는 하위 클래스에서 구현해야 합니다.")
    
    def _load_examples(self) -> Dict[str, List[Dict[str, Any]]]:
        """Few-shot 학습 예제 로드"""
        raise NotImplementedError("이 메서드는 하위 클래스에서 구현해야 합니다.")
    
    def _select_examples(self, screen_state: str, language: str) -> str:
        """화면 상태에 맞는 Few-shot 예제 선택"""
        raise NotImplementedError("이 메서드는 하위 클래스에서 구현해야 합니다.")
    
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
            
            return result
        
        except Exception as e:
            print(f"LLM 응답 파싱 오류: {e}")
            print(f"원본 응답: {response}")
            
            # 기본 응답
            return {
                "intent_type": IntentType.UNKNOWN,
                "menus": []
            }
    
    def process_unknown(self, text: str, language: str, screen_state: str, store_id: int, session: Dict[str, Any]) -> Dict[str, Any]:
        """알 수 없는 의도 처리"""
        reply = self.response_service.get_response("unknown", language)
        return {
            "intent_type": IntentType.UNKNOWN,
            "confidence": 0.3,
            "raw_text": text,
            "screen_state": screen_state,
            "data": {
                "pre_text": text,
                "post_text": text,
                "reply": reply,
                "status": ResponseStatus.UNKNOWN,
                "language": language,
                "session_id": session.get("id", ""),
                "cart": session.get("cart", []),
                "contents": [],
                "store_id": store_id
            }
        }
    
    def _get_category_name(self, category_id: int, store_id: int = None) -> str:
        """카테고리 ID에 해당하는 카테고리 이름을 반환"""
        # 메뉴 서비스에서 카테고리 정보 가져오기
        # menu_service는 이미 BaseProcessor 클래스에 주입되어 있음
        category = self.menu_service.get_category_by_id(category_id)
        
        if category:
            return category.get('name_kr', f"카테고리 {category_id}")
        else:
            return f"카테고리 {category_id}"