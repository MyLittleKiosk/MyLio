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
            print(f"[카트 추가 실패] 세션 없음: {session_id}")
            return []
        
        # 장바구니 가져오기 및 초기화
        if "cart" not in session:
            session["cart"] = []
        
        print(f"[카트 추가 전] 세션 ID: {session_id}, 장바구니 항목 수: {len(session['cart'])}")

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
        for i, item in enumerate(session["cart"]):
            if self._is_same_menu_item(item, optimized_item):
                # 동일 메뉴 발견 시 수량 증가
                session["cart"][i]["quantity"] += menu_item.get("quantity", 1)
                found = True
                print(f"[카트 업데이트] 기존 항목 수량 증가: {item.get('name')}, 새 수량: {session['cart'][i]['quantity']}")
                break
        
        # 동일 메뉴 없으면 새로 추가
        if not found:
            session["cart"].append(optimized_item)
            print(f"[카트 추가] 새 항목: {optimized_item.get('name')}, 옵션: {[opt.get('option_name') for opt in optimized_item.get('selected_options', [])]}")
        
        # 세션 업데이트
        session["last_accessed"] = datetime.now().isoformat()

        # 저장 전 장바구니 상태 로깅
        print(f"[카트 저장 전] 세션 ID: {session_id}, 장바구니 항목 수: {len(session['cart'])}, 항목: {[item.get('name') for item in session['cart']]}")

        # 세션 저장
        save_result = self._save_session(session_id, session)
        
        # 저장 확인 및 로깅
        if save_result:
            print(f"[카트 업데이트 성공] 세션 ID: {session_id}, 장바구니 항목 수: {len(session['cart'])}, 항목: {[item.get('name') for item in session['cart']]}")
        else:
            print(f"[카트 업데이트 실패] 세션 ID: {session_id}, Redis 저장 오류")
        
        # 변경 후 실제 장바구니 확인
        verify_session = self.get_session(session_id)
        if verify_session:
            verify_cart = verify_session.get("cart", [])
            print(f"[카트 검증] 세션 ID: {session_id}, 실제 장바구니 항목 수: {len(verify_cart)}, 항목: {[item.get('name') for item in verify_cart]}")
        
        return session["cart"]
    
    def get_cart(self, session_id: str) -> List[Dict[str, Any]]:
        """장바구니 조회"""
        session = self.get_session(session_id)
        print(f"[장바구니 조회] 세션 ID: {session_id}, 세션 존재 여부: {session is not None}")
        
        if not session:
            print(f"[장바구니 조회 실패] 세션 없음: {session_id}")
            return []
        
        cart = session.get("cart", [])
        print(f"[장바구니 조회 결과] 세션 ID: {session_id}, 항목 수: {len(cart)}, 항목: {[item.get('name') for item in cart]}")
        
        return cart
    
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
            print(f"[Redis 저장] 세션 ID: {session_id}")
            
            # 정제된 데이터 생성 (깊은 복사 대신 필요한 필드만 선택)
            sanitized_data = self._sanitize_session_data(session_data)
            
            try:
                session_json = json.dumps(sanitized_data)
                print(f"[Redis 저장] JSON 변환 성공: {len(session_json)} 바이트")
            except Exception as json_error:
                print(f"[Redis 저장] JSON 변환 실패: {json_error}")
                # 최소 데이터만 저장
                minimal_data = {
                    "id": session_id,
                    "last_accessed": datetime.now().isoformat(),
                    "cart": session_data.get("cart", []),  # 원본 카트 보존
                    "last_state": {}
                }
                session_json = json.dumps(minimal_data)
                
            # Redis에 저장
            self.redis.setex(session_key, self.timeout, session_json)
            
            return True
                
        except Exception as e:
            print(f"세션 저장 오류: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def _is_same_menu_item(self, item1: Dict[str, Any], item2: Dict[str, Any]) -> bool:
        """두 메뉴 항목이 동일한지 비교 (메뉴 ID와 선택된 옵션 기준)"""
        # 1. 기본 메뉴 ID 비교
        if item1.get("menu_id") != item2.get("menu_id"):
            return False
        
        # 2. 선택된 옵션 비교 (간소화된 비교 방식)
        # 옵션 ID와 첫 번째 옵션 상세 ID만 비교
        selected_options1 = set()
        for opt in item1.get("selected_options", []):
            opt_id = opt.get("option_id")
            if opt.get("option_details") and len(opt.get("option_details")) > 0:
                detail_id = opt.get("option_details")[0].get("id")
                selected_options1.add((opt_id, detail_id))
        
        selected_options2 = set()
        for opt in item2.get("selected_options", []):
            opt_id = opt.get("option_id")
            if opt.get("option_details") and len(opt.get("option_details")) > 0:
                detail_id = opt.get("option_details")[0].get("id")
                selected_options2.add((opt_id, detail_id))
        
        # 옵션 집합이 동일한지 비교
        return selected_options1 == selected_options2
    
    def _sanitize_session_data(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """세션 데이터에서 순환 참조를 제거"""
        # 깊은 복사 대신 필요한 필드만 새 객체로 복사
        sanitized = {}
        
        # 기본 필드 복사
        for key in ["id", "created_at", "last_accessed"]:
            if key in session_data:
                sanitized[key] = session_data[key]
        
        # 장바구니 항목 안전하게 복사
        if "cart" in session_data:
            sanitized["cart"] = []
            for item in session_data["cart"]:
                # 필요한 카트 항목 필드만 복사
                safe_item = {}
                for k in ["cart_id", "menu_id", "quantity", "name", "name_en", 
                        "description", "base_price", "total_price", "image_url"]:
                    if k in item:
                        safe_item[k] = item[k]
                
                # 선택된 옵션 안전하게 복사
                if "selected_options" in item:
                    safe_item["selected_options"] = []
                    for opt in item["selected_options"]:
                        safe_opt = {
                            "option_id": opt.get("option_id"),
                            "option_name": opt.get("option_name"),
                            "option_name_en": opt.get("option_name_en"),
                            "required": opt.get("required", False),
                            "is_selected": opt.get("is_selected", True)
                        }
                        
                        # 옵션 상세 정보 복사
                        if "option_details" in opt and opt["option_details"]:
                            safe_opt["option_details"] = []
                            for detail in opt["option_details"]:
                                safe_detail = {
                                    "id": detail.get("id"),
                                    "value": detail.get("value"),
                                    "additional_price": detail.get("additional_price", 0)
                                }
                                safe_opt["option_details"].append(safe_detail)
                        
                        safe_item["selected_options"].append(safe_opt)
                
                sanitized["cart"].append(safe_item)
        
        # last_state 안전하게 복사
        if "last_state" in session_data:
            sanitized["last_state"] = {}
            last_state = session_data["last_state"]
            
            # pending_option 복사
            if "pending_option" in last_state:
                pending_opt = last_state["pending_option"]
                sanitized["last_state"]["pending_option"] = {
                    "option_id": pending_opt.get("option_id"),
                    "option_name": pending_opt.get("option_name"),
                    "option_name_en": pending_opt.get("option_name_en"),
                    "required": pending_opt.get("required", False)
                }
                
                # 옵션 상세 정보 복사
                if "option_details" in pending_opt:
                    sanitized["last_state"]["pending_option"]["option_details"] = []
                    for detail in pending_opt.get("option_details", []):
                        safe_detail = {
                            "id": detail.get("id"),
                            "value": detail.get("value"),
                            "additional_price": detail.get("additional_price", 0)
                        }
                        sanitized["last_state"]["pending_option"]["option_details"].append(safe_detail)
            
            # menu 복사 
            if "menu" in last_state:
                menu = last_state["menu"]
                sanitized["last_state"]["menu"] = {
                    "menu_id": menu.get("menu_id"),
                    "name": menu.get("name"),
                    "base_price": menu.get("base_price", 0),
                    "total_price": menu.get("total_price", 0),
                    "image_url": menu.get("image_url", ""),
                    "is_corrected": menu.get("is_corrected", False),
                    "original_name": menu.get("original_name", None)
                }
                
                # 옵션 정보 복사 (개선)
                if "options" in menu:
                    sanitized["last_state"]["menu"]["options"] = []
                    for option in menu.get("options", []):
                        safe_option = {
                            "option_id": option.get("option_id"),
                            "option_name": option.get("option_name"),
                            "option_name_en": option.get("option_name_en", ""),
                            "required": option.get("required", False),
                            "is_selected": option.get("is_selected", False),
                            "selected_id": option.get("selected_id")
                        }
                        
                        if "option_details" in option:
                            safe_option["option_details"] = []
                            for detail in option.get("option_details", []):
                                safe_detail = {
                                    "id": detail.get("id"),
                                    "value": detail.get("value"),
                                    "additional_price": detail.get("additional_price", 0)
                                }
                                safe_option["option_details"].append(safe_detail)
                        
                        sanitized["last_state"]["menu"]["options"].append(safe_option)
                
                # 선택된 옵션 정보 복사 (중요 추가)
                if "selected_options" in menu:
                    sanitized["last_state"]["menu"]["selected_options"] = []
                    for option in menu.get("selected_options", []):
                        safe_option = {
                            "option_id": option.get("option_id"),
                            "option_name": option.get("option_name"),
                            "option_name_en": option.get("option_name_en", ""),
                            "required": option.get("required", False),
                            "is_selected": option.get("is_selected", True)
                        }
                        
                        if "option_details" in option:
                            safe_option["option_details"] = []
                            for detail in option.get("option_details", []):
                                safe_detail = {
                                    "id": detail.get("id"),
                                    "value": detail.get("value"),
                                    "additional_price": detail.get("additional_price", 0)
                                }
                                safe_option["option_details"].append(safe_detail)
                        
                        sanitized["last_state"]["menu"]["selected_options"].append(safe_option)
        
        # 대화 기록 복사
        if "history" in session_data:
            sanitized["history"] = []
            for entry in session_data.get("history", [])[:10]:  # 최근 10개만 저장
                safe_entry = {
                    "user_input": entry.get("user_input", ""),
                    "timestamp": entry.get("timestamp", "")
                }
                
                # 시스템 응답에서 필요한 부분만 복사
                if "system_response" in entry:
                    system_resp = entry["system_response"]
                    safe_entry["system_response"] = {
                        "intent_type": system_resp.get("intent_type", ""),
                        "data": {
                            "reply": system_resp.get("data", {}).get("reply", "")
                        }
                    }
                
                sanitized["history"].append(safe_entry)
        
        # 컨텍스트 정보 복사
        if "context" in session_data:
            context = session_data["context"]
            sanitized["context"] = {}
            
            # 화면 및 세션 상태 컨텍스트
            if "current_screen" in context:
                sanitized["context"]["current_screen"] = context["current_screen"]
            if "screen_history" in context:
                sanitized["context"]["screen_history"] = context["screen_history"]
            if "conversation_intent" in context:
                sanitized["context"]["conversation_intent"] = context["conversation_intent"]
            
            # LLM/랭체인 관련 컨텍스트
            if "selected_examples" in context:
                sanitized["context"]["selected_examples"] = context["selected_examples"]
            if "llm_response_keys" in context:
                sanitized["context"]["llm_response_keys"] = context["llm_response_keys"]
            if "prompt_context" in context:
                sanitized["context"]["prompt_context"] = context["prompt_context"]
            
            # 메뉴 및 주문 맥락
            if "menu_keywords" in context:
                sanitized["context"]["menu_keywords"] = context["menu_keywords"]
            if "option_patterns" in context:
                sanitized["context"]["option_patterns"] = context["option_patterns"]
            if "order_intent_state" in context:
                sanitized["context"]["order_intent_state"] = context["order_intent_state"]
            
            # 벡터 검색 관련 컨텍스트
            if "last_search_query" in context:
                sanitized["context"]["last_search_query"] = context["last_search_query"]
            if "search_results" in context:
                # 검색 결과의 핵심 정보만 저장 (전체 문서는 아님)
                sanitized["context"]["search_results"] = [
                    {"menu_id": r.get("menu_id"), "name": r.get("name_kr"), "similarity": r.get("similarity")}
                    for r in context["search_results"][:5]  # 상위 5개만 저장
                ] if isinstance(context["search_results"], list) else []
            
            # 기타 단순 타입의 컨텍스트 정보 보존
            for key, value in context.items():
                if key not in sanitized["context"]:
                    # 직렬화 가능한 단순 타입만 저장
                    if isinstance(value, (str, int, float, bool)):
                        sanitized["context"][key] = value
                    elif isinstance(value, (list, dict)) and len(str(value)) < 1000:  # 크기 제한
                        sanitized["context"][key] = value
        
        return sanitized