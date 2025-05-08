# app/services/session_manager.py
import json
import uuid
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List, Union

from app.db.redis_connector import RedisConnector

class RedisSessionManager:
    """Redis 기반 사용자 세션 관리 서비스"""
    
    def __init__(self, session_timeout_minutes: int = 30):
        self.redis = RedisConnector().get_client()
        self.timeout = session_timeout_minutes * 60  # 초 단위로 변환
        self.prefix = "session:"
    
    def create_session(self) -> str:
        """새로운 세션 생성"""
        session_id = str(uuid.uuid4())
        session_data = {
            "id": session_id,
            "created_at": datetime.now().isoformat(),
            "last_accessed": datetime.now().isoformat(),
            "cart": [],
            "last_state": {},
            "context": {},
            "history": []
        }
        
        # Redis에 저장
        self._save_session(session_id, session_data)
        
        return session_id
    
    def create_session_with_id(self, session_id: str) -> str:
        """주어진 ID로 세션 생성"""
        if not session_id:
            return self.create_session()  # ID가 없으면 새로 생성
            
        # 이미 존재하는 세션 ID인지 확인
        if self.get_session(session_id):
            return session_id
            
        # 주어진 ID로 세션 생성
        session_data = {
            "id": session_id,
            "created_at": datetime.now().isoformat(),
            "last_accessed": datetime.now().isoformat(),
            "cart": [],
            "last_state": {},
            "context": {},
            "history": []
        }
        
        # Redis에 저장
        self._save_session(session_id, session_data)
        
        return session_id
    
    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """세션 정보 조회"""
        if not session_id:
            return None
        
        # Redis에서 세션 데이터 조회
        session_key = f"{self.prefix}{session_id}"
        session_data = self.redis.get(session_key)
        
        if not session_data:
            return None
        
        try:
            # JSON 디코딩
            session_dict = json.loads(session_data)
            
            # 마지막 접근 시간 업데이트
            session_dict["last_accessed"] = datetime.now().isoformat()
            self._save_session(session_id, session_dict)
            
            return session_dict
        except Exception as e:
            print(f"세션 데이터 파싱 오류: {e}")
            return None
    
    def update_session(self, session_id: str, session_data: Dict[str, Any]) -> bool:
        """세션 정보 업데이트"""
        if not session_id:
            return False
        
        # 기존 세션 조회
        existing_session = self.get_session(session_id)
        if not existing_session:
            return False
        
        # 세션 정보 업데이트
        existing_session.update(session_data)
        existing_session["last_accessed"] = datetime.now().isoformat()
        
        # Redis에 저장
        return self._save_session(session_id, existing_session)
    
    def add_to_cart(self, session_id: str, menu_item: Dict[str, Any]) -> List[Dict[str, Any]]:
        """장바구니에 메뉴 추가"""
        session = self.get_session(session_id)
        if not session:
            return []
        
        # 장바구니 가져오기
        cart = session.get("cart", [])
        
        # 최적화된 메뉴 항목 생성
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
        session["cart"] = cart
        session["last_accessed"] = datetime.now().isoformat()

        self._save_session(session_id, session)
        
        return cart
    
    def get_cart(self, session_id: str) -> List[Dict[str, Any]]:
        """장바구니 조회"""
        session = self.get_session(session_id)
        if not session:
            return []
        
        return session.get("cart", [])
    
    def clear_cart(self, session_id: str) -> bool:
        """장바구니 비우기"""
        session = self.get_session(session_id)
        if not session:
            return False
        
        session["cart"] = []
        return self._save_session(session_id, session)
    
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
        
        # 디버깅 로그
        print(f"[대화 기록] 추가됨 - 사용자: '{user_input}', 응답: '{system_response.get('data', {}).get('reply', '')}'")
        print(f"[세션 상태] 업데이트 후 - last_state: {session.get('last_state', {})}")
        
        # 세션 저장
        self._save_session(session_id, session)
    
    def get_recent_history(self, session_id: str, count: int = 5) -> List[Dict[str, Any]]:
        """최근 대화 기록 조회"""
        session = self.get_session(session_id)
        if not session:
            return []
        
        history = session.get("history", [])
        return history[-count:] if len(history) > count else history
    
    def cleanup_expired_sessions(self) -> int:
        """만료된 세션 정리 (Redis TTL 기능 사용으로 필요 없음)"""
        # Redis에서는 TTL 기능을 사용하여 자동으로 만료되므로 구현 필요 없음
        return 0
    
    def _save_session(self, session_id: str, session_data: Dict[str, Any]) -> bool:
        """세션 데이터를 Redis에 저장"""
        try:
            session_key = f"{self.prefix}{session_id}"
            print(f"[Redis 저장] 세션 ID: {session_id}, last_state 여부: {'last_state' in session_data}")

            session_json = json.dumps(session_data)
            self.redis.setex(session_key, self.timeout, session_json)
            
            # 저장 후 즉시 읽어서 검증
            saved_data = self.redis.get(session_key)
            if saved_data:
                print(f"[Redis 저장 성공] 세션 ID: {session_id}, 크기: {len(saved_data)} 바이트")
                return True
            else:
                print(f"[Redis 저장 실패] 세션 ID: {session_id} - 데이터가 없음")
                return False
            
        except Exception as e:
            print(f"세션 저장 오류: {e}")
            return False
    
    def _is_same_menu_item(self, item1: Dict[str, Any], item2: Dict[str, Any]) -> bool:
        """두 메뉴 항목이 동일한지 비교 (메뉴 ID와 선택된 옵션 기준)"""
        if item1.get("menu_id") != item2.get("menu_id"):
            return False
        
        # 선택된 옵션 비교
        selected_options1 = set()
        for opt in item1.get("selected_options", []):
            if opt.get("option_details") and len(opt.get("option_details")) > 0:
                selected_options1.add((opt.get("option_id"), opt.get("option_details")[0].get("id")))
        
        selected_options2 = set()
        for opt in item2.get("selected_options", []):
            if opt.get("option_details") and len(opt.get("option_details")) > 0:
                selected_options2.add((opt.get("option_id"), opt.get("option_details")[0].get("id")))
        
        return selected_options1 == selected_options2