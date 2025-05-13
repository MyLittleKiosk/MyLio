# app/services/processor/detail_processor.py
from typing import Dict, Any, List
from app.models.schemas import IntentType, ScreenState, Language, ResponseStatus
from app.services.processor.base_processor import BaseProcessor
from app.services.response.response_generator import ResponseGenerator
from app.models.schemas import ResponseStatus
class DetailProcessor(BaseProcessor):
    """메뉴 상세 정보 처리 프로세서"""
    
    def __init__(self, response_generator: ResponseGenerator, menu_service, session_manager):
        """프로세서 초기화"""
        self.response_generator = response_generator
        self.menu_service = menu_service
        self.session_manager = session_manager
    
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
            context = {
                "status": ResponseStatus.UNKNOWN,
                "screen_state": screen_state
            }
            reply = intent_data.get("reply") or self.response_generator.generate_response(
                intent_data, language, context
            )
            return {
                "intent_type": IntentType.UNKNOWN,
                "confidence": intent_data.get("confidence", 0.3),
                "raw_text": text,
                "screen_state": screen_state,
                "data": {
                    "pre_text": text,
                    "post_text": intent_data.get("post_text", text),
                    "reply": reply,
                    "status": ResponseStatus.UNKNOWN,
                    "language": language,
                    "session_id": session.get("id", ""),
                    "cart": session.get("cart", []),
                    "contents": [],
                    "store_id": store_id
                }
            }
        
        # 2. 메뉴 정보 조회
        store_menus = self.menu_service.get_store_menus(store_id)
        if menu_id not in store_menus:
            context = {
                "status": ResponseStatus.UNKNOWN,
                "screen_state": screen_state
            }
            reply = intent_data.get("reply") or self.response_generator.generate_response(
                intent_data, language, context
            )
            return {
                "intent_type": IntentType.UNKNOWN,
                "confidence": intent_data.get("confidence", 0.3),
                "raw_text": text,
                "screen_state": screen_state,
                "data": {
                    "pre_text": text,
                    "post_text": intent_data.get("post_text", text),
                    "reply": reply,
                    "status": ResponseStatus.UNKNOWN,
                    "language": language,
                    "session_id": session.get("id", ""),
                    "cart": session.get("cart", []),
                    "contents": [],
                    "store_id": store_id
                }
            }
        
        menu = store_menus[menu_id]
        
        # 3. 메뉴 상세 정보 구성
        # 영양 성분 정보가 있는지 확인
        has_nutrition = "nutrition" in menu and menu["nutrition"]
        has_ingredients = "ingredients" in menu and menu["ingredients"]
        
        # 4. 응답 컨텍스트 구성
        context = {
            "status": ResponseStatus.DETAIL,
            "screen_state": ScreenState.DETAIL,
            "menu_name": menu["name_kr"] if language == Language.KR else menu.get("name_en", menu["name_kr"]),
            "menu": menu,
            "nutrition": menu.get("nutrition", []),
            "ingredients": menu.get("ingredients", []),
            "attribute": intent_data.get("attribute", "")
        }
        
        # 5. 응답 생성
        reply = intent_data.get("reply") or self.response_generator.generate_response(
            intent_data, language, context
        )
        
        # 6. 메뉴 상세 정보 구성
        detailed_contents = {
            "menu_id": menu_id,
            "name": menu["name_kr"],
            "name_en": menu.get("name_en", ""),
            "nutrition": menu.get("nutrition", {}),
            "ingredients": menu.get("ingredients", []),
            "description": menu.get("description", "")
        }
        
        # 7. 응답 반환
        return {
            "intent_type": IntentType.DETAIL,
            "confidence": intent_data.get("confidence", 0.9),
            "raw_text": text,
            "screen_state": ScreenState.DETAIL,
            "data": {
                "pre_text": text,
                "post_text": intent_data.get("post_text", text),
                "reply": reply,
                "status": ResponseStatus.DETAIL,
                "language": language,
                "session_id": session.get("id", ""),
                "cart": session.get("cart", []),
                "contents": detailed_contents,
                "store_id": store_id
            }
        }