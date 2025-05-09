# app/services/processor/detail_processor.py
from typing import Dict, Any, List
from app.models.schemas import IntentType, ScreenState, Language, ResponseStatus
from app.services.processor.base_processor import BaseProcessor

class DetailProcessor(BaseProcessor):
    """메뉴 상세 정보 처리 프로세서"""
    
    def process(self, intent_data: Dict[str, Any], text: str, language: str, screen_state: str, store_id: int, session: Dict[str, Any]) -> Dict[str, Any]:
        """상세 정보 의도 처리"""
        
        # 1. 세션에서 현재 선택된 메뉴 확인
        current_menu = None
        menu_id = None
        
        # 상세 조회할 메뉴 결정 로직:
        # a. intent_data에 메뉴 ID가 있으면 해당 메뉴 정보 사용
        if "menu_id" in intent_data and intent_data["menu_id"]:
            menu_id = intent_data["menu_id"]
        
        # b. 현재 화면에 표시된 메뉴가 있으면 해당 메뉴 사용
        elif session.get("last_state", {}).get("menu"):
            current_menu = session["last_state"]["menu"]
            menu_id = current_menu.get("id")
        
        # c. 사용자가 명시적으로 메뉴 이름을 언급했으면 해당 메뉴 검색
        elif "menu_name" in intent_data and intent_data["menu_name"]:
            menu_name = intent_data["menu_name"]
            found_menu = self.menu_service.find_menu_by_name(menu_name, store_id)
            if found_menu:
                current_menu = found_menu
                menu_id = found_menu.get("id")
        
        # 메뉴를 찾지 못한 경우
        if not menu_id:
            return self.process_unknown(text, language, screen_state, store_id, session)
        
        # 2. 메뉴 정보 조회
        store_menus = self.menu_service.get_store_menus(store_id)
        if menu_id not in store_menus:
            return self.process_unknown(text, language, screen_state, store_id, session)
        
        menu = store_menus[menu_id]
        
        # 3. 메뉴 상세 정보 구성
        # 영양 성분 정보가 있는지 확인
        has_nutrition = "nutrition" in menu and menu["nutrition"]
        has_ingredients = "ingredients" in menu and menu["ingredients"]
        
        # 4. 응답 메시지 생성
        if has_nutrition or has_ingredients:
            # 원재료 정보
            ingredients_text = ""
            if has_ingredients:
                ingredient_names = [ing.get("name_kr", "") for ing in menu.get("ingredients", [])]
                ingredients_text = ", ".join(ingredient_names)
            
            # 영양 성분 정보는 reply에 포함시키지 않고 메뉴 상세 정보에만 포함
            if has_ingredients:
                reply = f"{menu['name_kr']}의 원재료는 {ingredients_text}입니다."
            else:
                reply = f"{menu['name_kr']}의 상세 정보입니다."
        else:
            # 영양 성분과 원재료 정보 모두 없는 경우
            reply = f"죄송합니다. {menu['name_kr']}의 상세 정보가 없습니다."

        # 5. 옵션 정보를 제외한 필요한 메뉴 정보만 추출
        simplified_menu = {
            "id": menu.get("id"),
            "name_kr": menu.get("name_kr", ""),
            "name_en": menu.get("name_en", ""),
            "description": menu.get("description", ""),
            "price": menu.get("price", 0),
            "category_id": menu.get("category_id"),
            "nutrition": menu.get("nutrition", []),
            "ingredients": menu.get("ingredients", []),
        }
        
        # 5. 응답 반환
        return {
            "intent_type": IntentType.DETAIL,
            "confidence": 0.9,
            "raw_text": text,
            "screen_state": ScreenState.DETAIL,
            "data": {
                "pre_text": text,
                "post_text": text,
                "reply": reply,
                "status": ResponseStatus.DETAIL,  # 적절한 상태로 변경 가능
                "language": language,
                "session_id": session.get("id", ""),
                "cart": session.get("cart", []),
                #"contents": [menu],  # 메뉴 정보를 contents에 포함
                #"contents": [simplified_menu], 
                "contents": {
                    "menu_id": menu_id,
                    "name": menu["name_kr"],
                    "name_en": menu.get("name_en", ""),
                    "nutrition": menu.get("nutrition", {}),
                    "ingredients": menu.get("ingredients", []),
                    "description": menu.get("description", "")
                },
                "store_id": store_id
            }
        }
    
    def recognize_intent(self, text: str, language: str, screen_state: str, store_id: int, session: Dict[str, Any]) -> Dict[str, Any]:
        """메뉴 상세 정보 관련 의도 인식"""
        # Few-shot 기반 의도 인식 (상위 클래스 구현 활용)
        result = super().recognize_intent(text, language, screen_state, store_id, session)
        
        # 추가 규칙 기반 검사
        if self._is_detail_query(text, language):
            result["intent_type"] = IntentType.DETAIL
            
            # 현재 화면의 메뉴를 기본으로 사용
            if session.get("last_state", {}).get("menu"):
                result["menu_id"] = session["last_state"]["menu"].get("id")
                result["menu_name"] = session["last_state"]["menu"].get("name_kr")
            
            # 사용자가 언급한 메뉴가 있는지 확인
            # (간단한 메뉴 이름 추출 로직, 실제 구현에서는 더 정교한 NLP 사용 가능)
            store_menus = self.menu_service.get_store_menus(store_id)
            for menu_id, menu in store_menus.items():
                menu_name = menu["name_kr"].lower()
                if menu_name in text.lower():
                    result["menu_id"] = menu_id
                    result["menu_name"] = menu["name_kr"]
                    break
        
        return result
    
    def _is_detail_query(self, text: str, language: str) -> bool:
        """상세 정보 조회 의도인지 확인하는 간단한 규칙 기반 함수"""
        text_lower = text.lower()
        
        # 한국어 패턴
        if language == Language.KO:
            detail_keywords = ["영양", "성분", "칼로리", "원재료", "알레르기", "원산지", "정보", "상세"]
            return any(keyword in text_lower for keyword in detail_keywords)
        
        # 영어 패턴
        else:
            detail_keywords = ["nutrition", "calorie", "ingredient", "allergy", "detail", "information"]
            return any(keyword in text_lower for keyword in detail_keywords)
    
    def _load_examples(self):
        """상세 정보 조회 관련 Few-shot 예제"""
        return {
            "detail": [
                {
                    "input": "아메리카노 영양 성분 알려줘",
                    "output": {
                        "intent_type": "DETAIL",
                        "menu_name": "아메리카노",
                        "attribute": "nutrition"
                    }
                },
                {
                    "input": "이 메뉴 원재료가 뭐야?",
                    "output": {
                        "intent_type": "DETAIL",
                        "menu_name": None,  # 현재 화면의 메뉴
                        "attribute": "ingredients"
                    }
                },
                {
                    "input": "카페 라테 칼로리 얼마야?",
                    "output": {
                        "intent_type": "DETAIL",
                        "menu_name": "카페 라테",
                        "attribute": "calories"
                    }
                },
                {
                    "input": "바닐라 라떼에 알레르기 유발 성분 있어?",
                    "output": {
                        "intent_type": "DETAIL",
                        "menu_name": "바닐라 라떼",
                        "attribute": "allergy"
                    }
                }
            ]
        }
    
    def _get_prompt_template(self):
        """프롬프트 템플릿 정의"""
        from langchain.prompts import PromptTemplate
        
        template = """
        당신은 카페 키오스크의 음성 인식 시스템입니다. 사용자의 발화를 분석하고 정확한 의도를 파악해야 합니다.

        ### 현재 상황:
        - 화면 상태: {screen_state}
        - 언어: {language}
        - 이전 대화 기록: {history}

        ### 컨텍스트 정보:
        {context}

        ### 상세 정보 의도 인식 예제:
        {examples}

        ### 사용자 발화:
        "{text}"

        사용자의 발화가 메뉴의 영양 성분, 원재료, 알레르기 정보 등 상세 정보를 요청하는 것인지 판단하세요.
        만약 상세 정보 요청이라면, 어떤 메뉴에 대한 어떤 정보를 요청하는지 파악하세요.

        JSON 형식으로 응답하세요:
        ```json
        {
          "intent_type": "DETAIL" 또는 다른 의도,
          "menu_name": "요청한 메뉴 이름" 또는 null,
          "attribute": "요청한 속성(nutrition, ingredients, allergy 등)" 또는 null
        }
        ```
        """
        
        return PromptTemplate(
            input_variables=["screen_state", "language", "context", "history", "examples", "text"],
            template=template
        )