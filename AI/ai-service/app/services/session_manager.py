# app/services/session_manager.py
"""
세션 관리
"""
import uuid
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List

class SessionManager:
    """사용자 세션 관리 서비스"""
    
    def __init__(self, session_timeout_minutes: int = 30):
        self.sessions = {}  # 세션 저장소
        self.timeout = timedelta(minutes=session_timeout_minutes)
    
    def create_session(self) -> str:
        """새로운 세션 생성"""
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = {
            "id": session_id,
            "created_at": datetime.now(),
            "last_accessed": datetime.now(),
            "cart": [],
            "last_state": {},
            "context": {},
            "history": []
        }
        return session_id
    
    def create_session_with_id(self, session_id: str) -> str:
        """주어진 ID로 세션 생성"""
        if not session_id:
            return self.create_session()  # ID가 없으면 새로 생성
            
        # 이미 존재하는 세션 ID인지 확인
        if session_id in self.sessions:
            return session_id
            
        # 주어진 ID로 세션 생성
        self.sessions[session_id] = {
            "id": session_id,
            "created_at": datetime.now(),
            "last_accessed": datetime.now(),
            "cart": [],
            "last_state": {},
            "context": {},
            "history": []
        }
        return session_id
    
    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """세션 정보 조회"""
        if not session_id or session_id not in self.sessions:
            return None
        
        # 세션 접근 시간 업데이트
        self.sessions[session_id]["last_accessed"] = datetime.now()
        return self.sessions[session_id]
    
    def update_session(self, session_id: str, session_data: Dict[str, Any]) -> bool:
        """세션 정보 업데이트"""
        if not session_id or session_id not in self.sessions:
            return False
        
        # 세션 정보 업데이트
        self.sessions[session_id].update(session_data)
        self.sessions[session_id]["last_accessed"] = datetime.now()
        return True
    
    def add_to_cart(self, session_id: str, menu_item: Dict[str, Any]) -> List[Dict[str, Any]]:
        """장바구니에 메뉴 추가"""
        if not session_id or session_id not in self.sessions:
            return []
        
        # 메뉴 ID와 옵션 조합으로 동일 메뉴 식별
        cart = self.sessions[session_id].get("cart", [])

        # 최적화된 메뉴 항목 생성
        # optimized_item = self._optimize_menu_item(menu_item)
        # 최적화된 메뉴 항목 생성 (options 배열 없이 selected_options만 포함)
        optimized_item = {
            "cart_id": str(uuid.uuid4()),  # 장바구니 내 고유 ID
            "menu_id": menu_item.get("menu_id"),
            "quantity": menu_item.get("quantity", 1),
            "name": menu_item.get("name"),
            "name_en": menu_item.get("name_en"),
            "description": menu_item.get("description", ""),
            "base_price": menu_item.get("base_price", 0),
            "total_price": menu_item.get("total_price", 0),
            "image_url": menu_item.get("image_url"),
            "selected_options": menu_item.get("selected_options", []),
            # options 배열 자체를 제외
        }
        
        # 기존 장바구니 항목과 비교
        found = False
        for i, item in enumerate(cart):
            if self._is_same_menu_item(item, optimized_item):
                # 동일 메뉴 발견 시 수량 증가
                cart[i]["quantity"] += menu_item.get("quantity", 1)
                found = True
                break
        
        # 동일 메뉴 없으면 새로 추가
        if not found:
            cart.append(optimized_item)
        
        # 세션 업데이트
        self.sessions[session_id]["cart"] = cart
        self.sessions[session_id]["last_accessed"] = datetime.now()
        
        return cart
    
    def _optimize_menu_item(self, menu_item: Dict[str, Any]) -> Dict[str, Any]:
        """메뉴 항목 데이터 최적화"""
        # 기본 정보만 복사
        optimized = {
            "cart_id": str(uuid.uuid4()),  # 장바구니 내 고유 ID
            "menu_id": menu_item.get("menu_id"),
            "quantity": menu_item.get("quantity", 1),
            "name": menu_item.get("name"),
            "name_en": menu_item.get("name_en"),
            "base_price": menu_item.get("base_price", 0),
            "total_price": menu_item.get("total_price", 0),
            "image_url": menu_item.get("image_url")
        }
        
        # 선택된 옵션만 포함
        selected_options = []
        for option in menu_item.get("selected_options", []):
            # 옵션 정보 최적화
            selected_option = {
                "option_id": option.get("option_id"),
                "option_name": option.get("option_name"),
                "option_name_en": option.get("option_name_en", ""),
                "selected_detail": {}
            }
            
            # 첫 번째 선택된 옵션 상세 정보만 추가
            if option.get("option_details") and len(option.get("option_details")) > 0:
                detail = option.get("option_details")[0]
                selected_option["selected_detail"] = {
                    "id": detail.get("id"),
                    "value": detail.get("value"),
                    "additional_price": detail.get("additional_price", 0)
                }
            
            selected_options.append(selected_option)
        
        optimized["selected_options"] = selected_options
        
        return optimized
    
    def get_cart(self, session_id: str) -> List[Dict[str, Any]]:
        """장바구니 조회"""
        if not session_id or session_id not in self.sessions:
            return []
        
        return self.sessions[session_id].get("cart", [])
    
    def clear_cart(self, session_id: str) -> bool:
        """장바구니 비우기"""
        if not session_id or session_id not in self.sessions:
            return False
        
        self.sessions[session_id]["cart"] = []
        return True
    
    def add_to_history(self, session_id: str, user_input: str, system_response: Dict[str, Any]) -> None:
        """대화 기록 추가"""
        session = self.get_session(session_id)
        if not session:
            return
        
        # 기록 추가
        if "history" not in session:
            session["history"] = []
        
        history_entry = {
            "user_input": user_input,
            "system_response": system_response,
            "timestamp": datetime.now().isoformat()
        }
        session["history"].append(history_entry)
        print(f"[대화 기록] 추가됨 - 사용자: '{user_input}', 응답: '{system_response.get('data', {}).get('reply', '')}'")
        print(f"[세션 상태] 업데이트 후 - last_state: {session.get('last_state', {})}")
    
    def get_recent_history(self, session_id: str, count: int = 5) -> List[Dict[str, Any]]:
        """최근 대화 기록 조회"""
        if not session_id or session_id not in self.sessions:
            return []
        
        history = self.sessions[session_id].get("history", [])
        return history[-count:] if len(history) > count else history
    
    def cleanup_expired_sessions(self) -> int:
        """만료된 세션 정리"""
        now = datetime.now()
        expired_sessions = [
            session_id for session_id, session in self.sessions.items()
            if now - session["last_accessed"] > self.timeout
        ]
        
        for session_id in expired_sessions:
            del self.sessions[session_id]
        
        return len(expired_sessions)
    
    def _is_same_menu_item(self, item1: Dict[str, Any], item2: Dict[str, Any]) -> bool:
        """두 메뉴 항목이 동일한지 비교 (메뉴 ID와 선택된 옵션 기준)"""
        if item1.get("menu_id") != item2.get("menu_id"):
            return False
        
        # 선택된 옵션 비교
        selected_options1 = {
            (opt.get("option_id"), opt.get("option_details", [{}])[0].get("id"))
            for opt in item1.get("selected_options", [])
        }
        
        selected_options2 = {
            (opt.get("option_id"), opt.get("option_details", [{}])[0].get("id"))
            for opt in item2.get("selected_options", [])
        }
        
        return selected_options1 == selected_options2