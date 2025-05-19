# app/services/session_manager.py
import json
import uuid
import copy 
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List, Union

from app.db.redis_connector import RedisConnector
from app.models.schemas import ResponseStatus

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
    
    def add_to_cart(self, session_id: str, menu: Dict[str, Any]) -> bool:
        """장바구니에 메뉴 추가"""
        try:
            # 세션 가져오기
            session = self.get_session(session_id)
            if not session:
                print(f"[카트 추가 실패] 세션 없음: {session_id}")
                return False
            
            # 장바구니 초기화
            if "cart" not in session:
                session["cart"] = []
            
            # 이전 장바구니 항목 수 기록
            previous_count = len(session["cart"])
            
            # 카트 아이템 생성
            cart_item = {
                "cart_id": str(uuid.uuid4()),
                "menu_id": menu.get("id") or menu.get("menu_id"),
                "quantity": menu.get("quantity", 1),
                "name": menu.get("name_kr") or menu.get("name"),
                "name_en": menu.get("name_en"),
                "description": menu.get("description", ""),
                "base_price": menu.get("price") or menu.get("base_price", 0),
                "total_price": menu.get("total_price", 0),
                "image_url": menu.get("image_url"),
                "selected_options": []
            }
            
            # 선택된 옵션 추가
            if "selected_options" in menu and menu["selected_options"]:
                cart_item["selected_options"] = menu["selected_options"]
            else:
                # 옵션 구성
                for option in menu.get("options", []):
                    if option.get("is_selected") or option.get("selected_id") or option.get("option_value"):
                        cart_item["selected_options"].append(_build_selected_option(option))

            # 장바구니에 추가
            print(f"[카트 추가] 카트 아이템: {cart_item}")
            session["cart"].append(cart_item)
            
            # 세션 저장
            success = self._save_session(session_id, session)
            
            # 저장 후 검증
            updated_session = self.get_session(session_id)
            if updated_session and "cart" in updated_session:
                current_count = len(updated_session["cart"])
                if current_count > previous_count:
                    print(f"[카트 추가 성공] 이전: {previous_count}, 현재: {current_count}")
                    return True
                else:
                    print(f"[카트 추가 실패] 항목 수가 증가하지 않음. 이전: {previous_count}, 현재: {current_count}")
                    return False
            
            return success
        except Exception as e:
            print(f"[카트 추가 실패] 예외 발생: {str(e)}")
            return False
    
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
        """세션 데이터를 Redis에 저장 (검증 강화)"""
        if not session_id:
            print("[오류] 세션 저장 실패: 세션 ID가 없습니다.")
            return False
        
        # 세션 ID 일관성 확보
        session_data["id"] = session_id
        session_data["session_id"] = session_id  # 두 필드 모두 설정
        
        try:
            session_key = f"{self.prefix}{session_id}"
            
            # 마지막 접근 시간 업데이트
            session_data["last_accessed"] = datetime.now().isoformat()
            
            # Decimal 타입 변환 (JSON 직렬화 오류 방지)
            def convert_decimal(obj):
                if isinstance(obj, dict):
                    return {k: convert_decimal(v) for k, v in obj.items()}
                elif isinstance(obj, list):
                    return [convert_decimal(item) for item in obj]
                elif hasattr(obj, 'isoformat'):  # datetime 객체
                    return obj.isoformat()
                elif str(type(obj)) == "<class 'decimal.Decimal'>":  # Decimal 타입 체크
                    return float(obj)
                else:
                    return obj
            
            # Decimal 타입 변환 적용
            cleaned_data = convert_decimal(session_data)
            
            # 세션 데이터 정리 (중복 제거 및 최소화)
            sanitized = self._sanitize_session_data(cleaned_data)
            
            # JSON 직렬화
            try:
                session_json = json.dumps(sanitized)
            except Exception as json_error:
                print(f"[세션 저장] JSON 변환 실패: {json_error}")
                
                # 최소 필수 데이터만 저장
                minimal_data = {
                    "id": session_id,
                    "session_id": session_id,
                    "payment_method" : session.get("payment_method",""),
                    "created_at": session_data.get("created_at", datetime.now().isoformat()),
                    "last_accessed": datetime.now().isoformat(),
                    "cart": convert_decimal(session_data.get("cart", [])),  # 카트는 Decimal 변환 후 보존
                    "order_queue": convert_decimal(session_data.get("order_queue", []))  # 대기열도 Decimal 변환 후 보존
                }
                
                session_json = json.dumps(minimal_data)
            
            # Redis에 저장 (TTL 설정)
            result = self.redis.setex(session_key, self.timeout, session_json)
            if not result:
                print(f"[오류] Redis 저장 실패: {session_id}")
                return False
            
            # 저장 결과 검증
            stored_data = self.redis.get(session_key)
            if not stored_data:
                print(f"[오류] 저장 검증 실패: 저장 직후 데이터를 읽을 수 없음. (ID: {session_id})")
                return False
            
            # 장바구니 및 대기열 특별 검증
            if ("cart" in session_data and session_data["cart"]) or ("order_queue" in session_data and session_data["order_queue"]):
                try:
                    stored_data = self.redis.get(session_key)
                    if not stored_data:
                        print(f"[오류] 저장 검증 실패: 저장 직후 데이터를 읽을 수 없음. (ID: {session_id})")
                        return False
                        
                    stored_json = json.loads(stored_data)
                    
                    # 장바구니 검증
                    if "cart" in session_data and session_data["cart"]:
                        if "cart" not in stored_json:
                            print(f"[오류] 장바구니 데이터 손실: 원본에는 있으나 저장된 데이터에 없음")
                            # 다시 저장 시도
                            self.redis.setex(session_key, self.timeout, session_json)
                            return True  # 재시도 후 성공으로 처리
                            
                        if len(stored_json["cart"]) != len(convert_decimal(session_data["cart"])):
                            print(f"[경고] 장바구니 데이터 불일치: 원본={len(session_data['cart'])}, 저장됨={len(stored_json.get('cart', []))}")
                    
                    # 대기열 검증
                    if "order_queue" in session_data and session_data["order_queue"]:
                        if "order_queue" not in stored_json:
                            print(f"[오류] 대기열 데이터 손실: 원본에는 있으나 저장된 데이터에 없음")
                            # 대기열 정보만 다시 저장 (중요)
                            queue_only = {"order_queue": session_data["order_queue"]}
                            queue_json = json.dumps(convert_decimal(queue_only))
                            self.redis.hset(session_key, "order_queue", queue_json)
                            return True  # 재시도 후 성공으로 처리
                
                except Exception as e:
                    print(f"[경고] 저장 후 검증 중 오류: {e}")
                    return True  # 검증 중 오류가 있어도 성공으로 처리
            
            return True
                
        except Exception as e:
            print(f"[세션 저장 오류] {e}")
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
        """세션 데이터에서 중복 데이터 제거 및 최적화"""
        # 깊은 복사 대신 필요한 필드만 새 객체로 복사
        sanitized = {}
        
        # 기본 필드 복사
        for key in ["id", "created_at", "last_accessed", "payment_method"]:
            if key in session_data:
                sanitized[key] = session_data[key]
        
        # 대기열 복사 (더 많은 정보 보존)
        if "order_queue" in session_data and session_data["order_queue"]:
            sanitized["order_queue"] = []
            for queue_item in session_data["order_queue"]:
                # 중요 필드들 더 많이 보존
                sanitized_item = {
                    "id": queue_item.get("id"),
                    "menu_id": queue_item.get("menu_id", queue_item.get("id")),
                    "name_kr": queue_item.get("name_kr", ""),
                    "name": queue_item.get("name", queue_item.get("name_kr", "")),  # name 필드 추가
                    "menu_name": queue_item.get("menu_name", queue_item.get("name_kr", "")),
                    "price": queue_item.get("price", 0),
                    "quantity": queue_item.get("quantity", 1),
                    "image_url": queue_item.get("image_url", "")  # 이미지 URL 추가
                }
                
                # 옵션 정보 완전히 보존 (복사본 생성)
                if "options" in queue_item:
                    sanitized_item["options"] = []
                    for option in queue_item.get("options", []):
                        # 필수 옵션 정보만 복사
                        option_copy = {
                            "option_id": option.get("option_id"),
                            "option_name": option.get("option_name"),
                            "required": option.get("required", False),
                            "is_selected": option.get("is_selected", False)
                        }
                        
                        # 옵션 상세 정보 복사
                        if "option_details" in option:
                            option_copy["option_details"] = []
                            for detail in option.get("option_details", []):
                                option_copy["option_details"].append({
                                    "id": detail.get("id"),
                                    "value": detail.get("value"),
                                    "additional_price": detail.get("additional_price", 0)
                                })
                        
                        sanitized_item["options"].append(option_copy)
                
                sanitized["order_queue"].append(sanitized_item)
        
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
                
                # 선택된 옵션 안전하게 복사 (중복 제거)
                if "selected_options" in item:
                    safe_item["selected_options"] = []
                    added_option_ids = set()  # 중복 옵션 ID 추적
                    
                    for opt in item["selected_options"]:
                        option_id = opt.get("option_id")
                        if option_id in added_option_ids:
                            # 이미 추가된 옵션은 건너뛰기
                            continue
                        
                        added_option_ids.add(option_id)
                        safe_opt = {
                            "option_id": option_id,
                            "option_name": opt.get("option_name"),
                            "is_selected": True
                        }
                        
                        # 옵션 상세 정보 한 개만 복사 (첫번째)
                        if "option_details" in opt and opt["option_details"]:
                            detail = opt["option_details"][0]
                            safe_opt["option_details"] = [{
                                "id": detail.get("id"),
                                "value": detail.get("value"),
                                "additional_price": detail.get("additional_price", 0)
                            }]
                        
                        safe_item["selected_options"].append(safe_opt)
                
                sanitized["cart"].append(safe_item)
        
        # last_state 안전하게 복사
        if "last_state" in session_data:
            sanitized["last_state"] = {}
            last_state = session_data["last_state"]
            
            # pending_option 복사 (간소화)
            if "pending_option" in last_state:
                pending_opt = last_state["pending_option"]
                sanitized["last_state"]["pending_option"] = {
                    "option_id": pending_opt.get("option_id"),
                    "option_name": pending_opt.get("option_name"),
                    "required": pending_opt.get("required", False)
                }
                
                # 옵션 상세 정보 복사 (참조 필요한 최소 정보만)
                if "option_details" in pending_opt:
                    sanitized["last_state"]["pending_option"]["option_details"] = []
                    for detail in pending_opt.get("option_details", []):
                        sanitized["last_state"]["pending_option"]["option_details"].append({
                            "id": detail.get("id"),
                            "value": detail.get("value"),
                            "additional_price": detail.get("additional_price", 0)
                        })
            
            # menu 복사 (중복 제거 및 간소화)
            if "menu" in last_state:
                menu = last_state["menu"]
                sanitized["last_state"]["menu"] = {
                    "menu_id": menu.get("menu_id"),
                    "name": menu.get("name"),
                    "base_price": menu.get("base_price", 0),
                    "total_price": menu.get("total_price", 0)
                }
                
                # 옵션 정보 복사 (필수만 최소화)
                if "options" in menu:
                    sanitized["last_state"]["menu"]["options"] = []
                    required_only = []
                    
                    for option in menu.get("options", []):
                        # 필수 옵션 또는 이미 선택된 옵션만 저장
                        if option.get("required", False) or option.get("is_selected", False):
                            # 중복 필드 제거 및 최소 정보만 포함
                            min_option = {
                                "option_id": option.get("option_id"),
                                "option_name": option.get("option_name"),
                                "required": option.get("required", False),
                                "is_selected": option.get("is_selected", False)
                            }
                            
                            # 선택된 옵션이면 ID 추가
                            if option.get("is_selected", False):
                                min_option["selected_id"] = option.get("selected_id")
                            
                            # 옵션 상세 정보는 최소화
                            if "option_details" in option:
                                min_option["option_details"] = []
                                for detail in option.get("option_details", []):
                                    min_option["option_details"].append({
                                        "id": detail.get("id"),
                                        "value": detail.get("value")
                                    })
                            
                            required_only.append(min_option)
                    
                    sanitized["last_state"]["menu"]["options"] = required_only
                    sanitized["last_state"]["menu"]["options"] = copy.deepcopy(menu.get("options", []))
                
                # 선택된 옵션 정보 복사 (중복 제거)
                if "selected_options" in menu:
                    sanitized["last_state"]["menu"]["selected_options"] = []
                    added_option_ids = set()  # 중복 옵션 ID 추적
                    
                    for option in menu.get("selected_options", []):
                        option_id = option.get("option_id")
                        if option_id in added_option_ids:
                            # 이미 추가된 옵션은 건너뛰기
                            continue
                        
                        added_option_ids.add(option_id)
                        min_option = {
                            "option_id": option_id,
                            "option_name": option.get("option_name"),
                            "is_selected": True
                        }
                        
                        # 옵션 상세 정보 한 개만 복사 (첫번째)
                        if "option_details" in option and option["option_details"]:
                            detail = option["option_details"][0]
                            min_option["option_details"] = [{
                                "id": detail.get("id"),
                                "value": detail.get("value"),
                                "additional_price": detail.get("additional_price", 0)
                            }]
                        
                        sanitized["last_state"]["menu"]["selected_options"].append(min_option)
        
        # 대화 기록 최소화 - 최근 3개만 유지
        if "history" in session_data:
            sanitized["history"] = []
            recent_history = session_data.get("history", [])[-3:]  # 최근 3개만
            
            for entry in recent_history:
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
        
        # 컨텍스트 정보 저장 안함 (대부분 불필요)
        # 세션 크기 축소를 위해 제외
        
        return sanitized
    
    def delete_session(self, session_id: str) -> bool:
        """세션 명시적 삭제"""
        if not session_id:
            return False
        
        try:
            # 세션 키 구성
            session_key = f"{self.prefix}{session_id}"
            
            # Redis에서 세션 삭제
            deleted = self.redis.delete(session_key)
            
            # 인메모리 캐시가 있는 경우 캐시에서도 삭제
            if hasattr(self, '_session_cache') and session_id in self._session_cache:
                del self._session_cache[session_id]
            
            print(f"[세션 삭제] 세션 ID: {session_id}, 결과: {deleted > 0}")
            return deleted > 0
        
        except Exception as e:
            print(f"[세션 삭제 오류] 세션 ID: {session_id}, 오류: {e}")
            return False

    def cleanup_expired_sessions(self, max_idle_time_minutes: int = 60) -> int:
        """오래된 세션 정리"""
        try:
            import time
            from datetime import datetime, timedelta
            
            # 현재 시간
            current_time = datetime.now()
            cutoff_time = current_time - timedelta(minutes=max_idle_time_minutes)
            cutoff_time_iso = cutoff_time.isoformat()
            
            # 모든 세션 키 조회
            session_keys = self.redis.keys(f"{self.prefix}*")
            
            deleted_count = 0
            for key in session_keys:
                try:
                    # 세션 데이터 로드
                    session_data = self.redis.get(key)
                    if not session_data:
                        continue
                    
                    # JSON 파싱
                    session = json.loads(session_data)
                    
                    # 마지막 접근 시간 확인
                    last_accessed = session.get("last_accessed")
                    if not last_accessed:
                        continue
                    
                    # 마지막 접근 시간이 기준 시간보다 오래된 경우 삭제
                    if last_accessed < cutoff_time_iso:
                        session_id = key.decode('utf-8').replace(self.prefix, "")
                        if self.delete_session(session_id):
                            deleted_count += 1
                
                except Exception as e:
                    # 개별 세션 처리 중 오류 무시하고 계속 진행
                    print(f"[세션 정리 중 오류] 키: {key}, 오류: {e}")
                    continue
            
            print(f"[세션 정리 완료] 삭제된 세션 수: {deleted_count}")
            return deleted_count
        
        except Exception as e:
            print(f"[세션 정리 오류] {e}")
            return 0

    def get_all_sessions_info(self) -> Dict[str, Any]:
        """모든 세션 정보 요약"""
        try:
            # 모든 세션 키 조회
            session_keys = self.redis.keys(f"{self.prefix}*")
            
            total_count = len(session_keys)
            active_sessions = []
            total_size = 0
            
            # 샘플링 (최대 100개)
            sample_keys = session_keys[:100] if len(session_keys) > 100 else session_keys
            
            for key in sample_keys:
                try:
                    # 세션 데이터 로드
                    session_data = self.redis.get(key)
                    if not session_data:
                        continue
                    
                    # 데이터 크기 측정
                    size = len(session_data)
                    total_size += size
                    
                    # 세션 ID 추출
                    session_id = key.decode('utf-8').replace(self.prefix, "")
                    
                    # JSON 파싱
                    session = json.loads(session_data)
                    
                    # 세션 요약 정보
                    active_sessions.append({
                        "id": session_id,
                        "last_accessed": session.get("last_accessed", ""),
                        "cart_items": len(session.get("cart", [])),
                        "history_count": len(session.get("history", [])),
                        "data_size": size,
                    })
                
                except Exception as e:
                    # 개별 세션 처리 중 오류 무시하고 계속 진행
                    print(f"[세션 정보 수집 중 오류] 키: {key}, 오류: {e}")
                    continue
            
            # 평균 세션 크기 계산
            avg_size = total_size / len(sample_keys) if sample_keys else 0
            estimated_total_size = avg_size * total_count
            
            return {
                "total_sessions": total_count,
                "sampled_sessions": len(sample_keys),
                "avg_session_size_bytes": avg_size,
                "estimated_total_size_mb": estimated_total_size / (1024 * 1024),
                "active_sessions": active_sessions
            }
        
        except Exception as e:
            print(f"[세션 정보 수집 오류] {e}")
            return {
                "error": str(e),
                "total_sessions": 0,
                "active_sessions": []
            }

    def cleanup_large_sessions(self, max_size_kb: int = 100) -> int:
        """비정상적으로 큰 세션 정리"""
        try:
            # 모든 세션 키 조회
            session_keys = self.redis.keys(f"{self.prefix}*")
            
            deleted_count = 0
            for key in session_keys:
                try:
                    # 세션 데이터 로드
                    session_data = self.redis.get(key)
                    if not session_data:
                        continue
                    
                    # 데이터 크기 측정
                    size_kb = len(session_data) / 1024
                    
                    # 사이즈가 기준보다 크면 삭제
                    if size_kb > max_size_kb:
                        session_id = key.decode('utf-8').replace(self.prefix, "")
                        print(f"[큰 세션 발견] 세션 ID: {session_id}, 크기: {size_kb:.2f} KB")
                        
                        # 가능하면 세션을 정리하고 다시 저장 (완전 삭제 대신)
                        try:
                            session = json.loads(session_data)
                            
                            # 최소 필드만 남김
                            minimal_session = {
                                "id": session.get("id", session_id),
                                "created_at": session.get("created_at", ""),
                                "last_accessed": session.get("last_accessed", ""),
                                "cart": session.get("cart", [])[:5]  # 최대 5개 항목만 유지
                            }
                            
                            # 다시 저장
                            minimal_data = json.dumps(minimal_session)
                            self.redis.setex(key, self.timeout, minimal_data)
                            print(f"[세션 최소화] 세션 ID: {session_id}, 새 크기: {len(minimal_data) / 1024:.2f} KB")
                            deleted_count += 1
                        except:
                            # 정리 실패 시 완전 삭제
                            if self.redis.delete(key):
                                deleted_count += 1
                
                except Exception as e:
                    # 개별 세션 처리 중 오류 무시하고 계속 진행
                    print(f"[세션 정리 중 오류] 키: {key}, 오류: {e}")
                    continue
            
            print(f"[큰 세션 정리 완료] 처리된 세션 수: {deleted_count}")
            return deleted_count
        
        except Exception as e:
            print(f"[세션 정리 오류] {e}")
            return 0

    def set_session_timeout(self, session_id: str, timeout_seconds: int = None) -> bool:
        """특정 세션의 TTL 변경"""
        if not session_id:
            return False
        
        try:
            session_key = f"{self.prefix}{session_id}"
            
            # 현재 세션 데이터 가져오기
            session_data = self.redis.get(session_key)
            if not session_data:
                return False
            
            # 타임아웃 설정 (기본값: 인스턴스 기본 타임아웃)
            timeout = timeout_seconds if timeout_seconds is not None else self.timeout
            
            # 세션 데이터 유지하고 타임아웃만 갱신
            self.redis.expire(session_key, timeout)
            
            return True
        
        except Exception as e:
            print(f"[세션 타임아웃 설정 오류] 세션 ID: {session_id}, 오류: {e}")
            return False

    def add_to_order_queue(self, session_id: str, menus: List[Dict[str, Any]]) -> bool:
        """주문 대기열에 메뉴 추가"""
        session = self.get_session(session_id)
        if not session:
            return False
        
        # 대기열 초기화
        if "order_queue" not in session:
            session["order_queue"] = []
        
        # 대기열에 메뉴 추가
        session["order_queue"].extend(menus)
        
        # 세션 저장
        return self._save_session(session_id, session)

    def get_next_queued_menu(self, session_id: str) -> Optional[Dict[str, Any]]:
        """대기열에서 다음 메뉴 가져오기"""
        session = self.get_session(session_id)
        queue_exists = session and "order_queue" in session and session["order_queue"]
        
        if not queue_exists:
            print(f"[대기열 조회] 세션 ID: {session_id}, 대기열 비어있음")
            return None
        
        # 첫 번째 메뉴 가져오기 (pop하지 않고 peek만)
        first_menu = session["order_queue"][0]
        print(f"[대기열 조회] 세션 ID: {session_id}, 다음 메뉴: {first_menu.get('name_kr', '') or first_menu.get('menu_name', '') or first_menu.get('name', '')}")
        return first_menu

    def remove_from_order_queue(self, session_id: str) -> bool:
        """대기열에서 처리 완료된 메뉴 제거"""
        session = self.get_session(session_id)
        queue_exists = session and "order_queue" in session and session["order_queue"]
        
        if not queue_exists:
            print(f"[대기열 제거] 세션 ID: {session_id}, 대기열 비어있음")
            return False
        
        # 제거 전 메뉴 확인
        first_menu = session["order_queue"][0]
        menu_name = first_menu.get('name_kr', '') or first_menu.get('menu_name', '') or first_menu.get('name', '')
        print(f"[대기열 제거] 세션 ID: {session_id}, 제거할 메뉴: {menu_name}")
        
        # 첫 번째 메뉴 제거
        session["order_queue"].pop(0)
        print(f"[대기열 제거] 세션 ID: {session_id}, 제거 후 크기: {len(session['order_queue'])}")
        
        # 세션 저장 및 결과 확인
        result = self._save_session(session_id, session)
        # 저장 후 세션 다시 확인하여 변경 사항이 반영되었는지 검증
        updated_session = self.get_session(session_id)
        updated_queue_size = len(updated_session.get("order_queue", [])) if updated_session and "order_queue" in updated_session else 0
        print(f"[대기열 제거 검증] 세션 ID: {session_id}, 저장 후 대기열 크기: {updated_queue_size}")
        
        return result
    
    def update_order_queue_first(self, session_id: str, updated_menu: Dict[str, Any]) -> None:
        session = self.get_session(session_id)
        if session and "order_queue" in session and session["order_queue"]:
            session["order_queue"][0] = updated_menu
            self._save_session(session_id, session)

    def update_session_field(self, session_id: str, field: str, value: Any) -> bool:
        """세션의 특정 필드만 업데이트"""
        if not session_id:
            print(f"[오류] 세션 ID가 없음: 필드 {field} 업데이트 실패")
            return False
        
        # 기존 세션 가져오기
        session = self.get_session(session_id)
        if not session:
            print(f"[오류] 세션을 찾을 수 없음: {session_id}, 필드 {field} 업데이트 실패")
            return False
        
        # 필드 업데이트
        session[field] = value
        
        # 세션 저장 (장바구니 및 다른 데이터는 유지)
        return self._save_session(session_id, session)

    def _build_selected_option(option, force=False):
        # ① is_selected 이거나 ② force=True 인 경우에만 detail을 고른다
        if not option.get("is_selected") and not force:
            return None        # 선택 안 했으면 None 반환

        detail = _extract_selected_detail(option, force_fallback=force)
        if not detail:
            return None

        return {
            "option_id": option["option_id"],
            "option_name": option["option_name"],
            "is_selected": True,
            "option_details": [detail],
        }

    
    def _extract_selected_detail(option) -> Optional[Dict[str, Any]]:
        """
        이름(value) ➜ id ➜ (필수·force_fallback 인 경우만) 첫 detail
        """
        value = (option.get("option_value") or "").strip().lower()
        sel_id = option.get("selected_id")

        # ① value 매칭
        if value:
            for d in option.get("option_details", []):
                if value in d["value"].lower():
                    return {k: d[k] for k in ("id", "value", "additional_price")}

        # ② id 매칭
        if sel_id is not None:
            for d in option.get("option_details", []):
                if d["id"] == sel_id:
                    return {k: d[k] for k in ("id", "value", "additional_price")}

        # ③ fallback (필수 or 강제일 때만)
        if force_fallback and option.get("option_details"):
            d = option["option_details"][0]
            return {k: d[k] for k in ("id", "value", "additional_price")}

        # 선택 안 함
        return None

    # --- payment_method persistence -------------------------
    def save_pending_payment(self, session_id: str, method: str):
        self.set_session_value(session_id, "pending_payment_method", method)

    def pop_pending_payment(self, session_id: str) -> Optional[str]:
        """가져오면서 바로 삭제"""
        pm = self.get_session_value(session_id, "pending_payment_method")
        if pm:
            self.delete_session_value(session_id, "pending_payment_method")
        return pm


    def get_session_value(self, session_id: str, field: str) -> Optional[Any]:
        """세션에서 특정 필드 값을 읽어온다."""
        session = self.get_session(session_id)
        return session.get(field) if session else None

    def set_session_value(self, session_id: str, field: str, value: Any) -> bool:
        """세션의 특정 필드를 저장한다."""
        session = self.get_session(session_id)
        if not session:
            return False
        session[field] = value
        return self._save_session(session_id, session)

    def delete_session_value(self, session_id: str, field: str) -> bool:
        """세션에서 특정 필드를 삭제한다."""
        session = self.get_session(session_id)
        if not session or field not in session:
            return False
        del session[field]
        return self._save_session(session_id, session)