# app/services/option/option_handler.py
from typing import Dict, Any, Optional, List

from app.models.schemas import ResponseStatus
from app.services.option.option_matcher import OptionMatcher

class OptionHandler:
    """옵션 처리 핸들러"""
    
    def __init__(self):
        self.option_matcher = OptionMatcher()
    
    def process_option_selection(self, text: str, pending_option: Dict[str, Any], menu: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """사용자 응답에서 옵션 처리"""
        # 옵션 파싱
        selected_option = self.option_matcher.parse_option_response(text, pending_option, menu)
        if selected_option:
             self.option_matcher.apply_option_to_menu(menu, selected_option)
        
        for opt in menu.get("options", []):
            if opt is pending_option or opt.get("is_selected"):
                continue
            extra_sel = self.option_matcher.parse_option_response(text, opt, menu)
            if extra_sel:
                self.option_matcher.apply_option_to_menu(menu, extra_sel)

        return selected_option
    
    def get_next_required_option(self, menu: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """다음 필수 옵션 가져오기"""
        return self.option_matcher.get_next_required_option(menu)
    
    def determine_menu_status(self, menu: Dict[str, Any]) -> ResponseStatus:
        """메뉴 상태 판단"""
        return self.option_matcher.determine_menu_status(menu)
    
    def calculate_total_price(self, menu: Dict[str, Any]) -> int:
        """총 가격 계산"""
        return self.option_matcher.calculate_total_price(menu)

    def apply_option_to_menu(self, menu: Dict[str, Any], selected_option: Dict[str, Any]) -> None:
        """메뉴에 옵션 적용"""
        self.option_matcher.apply_option_to_menu(menu, selected_option)