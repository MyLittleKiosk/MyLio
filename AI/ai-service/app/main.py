# app/main.py
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from typing import Dict, List, Any, Optional
import uuid

from app.models.schemas import VoiceInputRequest, VoiceInputResponse, ScreenState, Language, ResponseStatus, IntentType
from app.db.mysql_connector import MySQLConnector
from app.services.menu_service import MenuService
from app.services.response_service import ResponseService
from app.services.redis_session_manager import RedisSessionManager
from app.services.intent_service import IntentService
# from app.services.vector_db_service import VectorDBService
from app.models.schemas import ResponseStatus

# 환경 변수 로드
load_dotenv()

# FastAPI 앱 생성
app = FastAPI(
    title="Voice Kiosk API",
    description="음성 키오스크용 API 서비스",
    version="0.2.0"  # 버전 업데이트
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 의존성 주입을 위한 함수
def get_db():
    db = MySQLConnector(
        host=os.getenv("MYSQL_HOST", "localhost"),
        port=int(os.getenv("MYSQL_PORT", 3306)),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASS", ""),
        database=os.getenv("MYSQL_DB", "mylio")
    )
    try:
        yield db
    finally:
        db.disconnect()

def get_menu_service(db: MySQLConnector = Depends(get_db)):
    return MenuService(db)

def get_response_service():
    return ResponseService()

def get_session_manager():
    if not hasattr(app.state, "session_manager") or app.state.session_manager is None:
        print("[경고] Redis 세션 매니저가 존재하지 않아서 생성합니다.")
        app.state.session_manager = RedisSessionManager()
    return app.state.session_manager

def get_intent_service(
    menu_service: MenuService = Depends(get_menu_service),
    response_service: ResponseService = Depends(get_response_service),
    session_manager = Depends(get_session_manager)
):
    return IntentService(
        api_key=os.getenv("OPENAI_API_KEY"),
        menu_service=menu_service,
        response_service=response_service,
        session_manager=session_manager
    )

# 초기화 이벤트
@app.on_event("startup")
async def startup_event():
    print("음성 키오스크 API 서비스가 시작되었습니다. (Redis 세션 관리 활성화)")

    # 벡터 DB 초기화 (메뉴 서비스 필요)
    try:
        # 메뉴 서비스 생성
        mysql_host = os.getenv("MYSQL_HOST", "localhost")
        mysql_port = int(os.getenv("MYSQL_PORT", "3306"))
        mysql_user = os.getenv("MYSQL_USER", "root")
        mysql_pass = os.getenv("MYSQL_PASS", "password")
        mysql_db = os.getenv("MYSQL_DB", "kiosk")

        # DB 객체 생성
        db = MySQLConnector(
            host=mysql_host,
            port=mysql_port,
            user=mysql_user,
            password=mysql_pass,
            database=mysql_db
        )
        
        # MenuService 초기화 - db 객체 전달
        menu_service = MenuService(db)
        
        # 벡터 DB 서비스 초기화
        # vector_db_service = VectorDBService.get_instance()
        
        # 매장 ID 목록 
        store_ids = menu_service.get_all_store_ids()
        
        # 메뉴 데이터로 벡터 DB 초기화
        # document_count = vector_db_service.initialize_from_menus(menu_service, store_ids)
        print(f"[앱 시작] 벡터 DB 초기화 완료: {document_count}개 메뉴 데이터")
        
    except Exception as e:
        print(f"[앱 시작] 벡터 DB 초기화 오류: {e}")
        import traceback
        traceback.print_exc()
    
    # Redis 세션 관리자 초기화
    app.state.session_manager = RedisSessionManager()
    
    # Redis 연결 상태 확인
    if app.state.session_manager.redis.ping():
        print("Redis 서버에 성공적으로 연결되었습니다.")
        
        # Redis 세션 정리 스케줄러 초기화 및 시작
        try:
            import threading
            import time
            import schedule
            
            # 세션 정리 스케줄러 생성
            app.state.cleanup_thread = None
            app.state.cleanup_running = False
            
            # 세션 정리 함수
            def cleanup_expired_sessions():
                try:
                    if not hasattr(app.state, "session_manager") or app.state.session_manager is None:
                        return
                    
                    # 현재 세션 수 조회
                    all_keys = app.state.session_manager.redis.keys(f"{app.state.session_manager.prefix}*")
                    total_sessions = len(all_keys)
                    
                    # 1시간 이상 미사용 세션 정리
                    import datetime
                    from datetime import timedelta
                    
                    cutoff_time = datetime.datetime.now() - timedelta(minutes=60)
                    cutoff_str = cutoff_time.isoformat()
                    
                    cleaned_count = 0
                    for key in all_keys:
                        try:
                            # 세션 데이터 추출
                            session_data = app.state.session_manager.redis.get(key)
                            if not session_data:
                                continue
                            
                            # JSON 파싱
                            import json
                            session = json.loads(session_data)
                            
                            # 마지막 접근 시간 확인
                            last_accessed = session.get("last_accessed", "")
                            if last_accessed and last_accessed < cutoff_str:
                                # 세션 삭제
                                app.state.session_manager.redis.delete(key)
                                cleaned_count += 1
                        except:
                            continue
                    
                    if cleaned_count > 0:
                        print(f"[세션 정리] {cleaned_count}개 만료된 세션 정리 완료 (전체 {total_sessions}개 중)")
                    
                    # 큰 세션 정리 (100KB 이상)
                    large_cleaned = 0
                    for key in app.state.session_manager.redis.keys(f"{app.state.session_manager.prefix}*"):
                        try:
                            # 세션 데이터 크기 확인
                            size = len(app.state.session_manager.redis.get(key) or "")
                            if size > 100 * 1024:  # 100KB 초과
                                # 기본 필드만 유지하고 최소화
                                session_data = app.state.session_manager.redis.get(key)
                                if not session_data:
                                    continue
                                
                                session = json.loads(session_data)
                                session_id = key.decode('utf-8').replace(app.state.session_manager.prefix, "")
                                
                                # 최소 필드만 유지
                                minimal_session = {
                                    "id": session.get("id", session_id),
                                    "created_at": session.get("created_at", ""),
                                    "last_accessed": session.get("last_accessed", ""),
                                    "cart": session.get("cart", [])[:5]  # 장바구니 최대 5개 항목만 유지
                                }
                                
                                # 다시 저장
                                minimal_data = json.dumps(minimal_session)
                                app.state.session_manager.redis.setex(
                                    key, 
                                    app.state.session_manager.timeout, 
                                    minimal_data
                                )
                                large_cleaned += 1
                        except:
                            continue
                    
                    if large_cleaned > 0:
                        print(f"[세션 정리] {large_cleaned}개 큰 세션 최적화 완료")
                
                except Exception as e:
                    print(f"[세션 정리] 오류 발생: {e}")
            
            # 스케줄러 스레드
            def run_scheduler():
                while app.state.cleanup_running:
                    schedule.run_pending()
                    time.sleep(1)
            
            # 스케줄 설정
            # 매시간 실행
            schedule.every().hour.do(cleanup_expired_sessions)
            
            # 매일 자정에 대규모 정리
            schedule.every().day.at("00:00").do(cleanup_expired_sessions)
            
            # 스케줄러 시작
            app.state.cleanup_running = True
            app.state.cleanup_thread = threading.Thread(target=run_scheduler, daemon=True)
            app.state.cleanup_thread.start()
            
            print("[앱 시작] Redis 세션 정리 스케줄러가 시작되었습니다.")
            
            # 시작 시 한 번 실행
            cleanup_expired_sessions()
            
        except Exception as e:
            print(f"[앱 시작] 세션 정리 스케줄러 초기화 오류: {e}")
    else:
        print("[경고] Redis 서버에 연결할 수 없습니다.")

# 종료 이벤트
@app.on_event("shutdown")
async def shutdown_event():
    # 세션 정리 스케줄러 중지
    if hasattr(app.state, "cleanup_running"):
        app.state.cleanup_running = False
        
        if hasattr(app.state, "cleanup_thread") and app.state.cleanup_thread:
            app.state.cleanup_thread.join(timeout=1.0)
    
    print("음성 키오스크 API 서비스가 종료되었습니다.")

# # 화면 상태 목록 조회 엔드포인트
# @app.get("/ai/screen-states")
# async def get_screen_states():
#     """화면 상태 목록 조회"""
#     return {"screen_states": [state.value for state in ScreenState]}

# # 지원 언어 목록 조회 엔드포인트
# @app.get("/ai/languages")
# async def get_languages():
#     """지원 언어 목록 조회"""
#     return {"languages": [lang.value for lang in Language]}

# # 메뉴 조회 엔드포인트
# @app.get("/ai/menus/{store_id}")
# async def get_store_menus(store_id: int, menu_service: MenuService = Depends(get_menu_service)):
#     """스토어 ID에 해당하는 메뉴 정보 조회"""
#     try:
#         menus = menu_service.get_store_menus(store_id)
#         return {"menus": list(menus.values())}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"메뉴 조회 중 오류 발생: {str(e)}")

# 음성 입력 처리 엔드포인트
@app.post("/ai/recognize-intent", response_model=VoiceInputResponse)
async def recognize_intent(
    request: VoiceInputRequest,
    intent_service: IntentService = Depends(get_intent_service)
):
    """음성 입력 인식 API"""
    try:
        # 입력 데이터 추출
        text = request.text
        language = request.language
        screen_state = request.screen_state
        store_id = request.store_id
        session_id = request.session_id
        
        # 의도 인식 및 처리
        response = intent_service.process_request(
            text=text,
            language=language,
            screen_state=screen_state,
            store_id=store_id,
            session_id=session_id
        )
        # 응답 형식 포맷팅
        formatted_response = format_intent_response(response)
        
        return formatted_response
    
    except Exception as e:
        import traceback
        print(f"음성 입력 처리 중 오류 발생: {str(e)}")
        print(traceback.format_exc())
        
        raise HTTPException(
            status_code=500,
            detail=f"음성 입력 처리 중 오류 발생: {str(e)}"
        )

# # 세션 관리 엔드포인트 (옵션)
# @app.get("/ai/sessions/{session_id}")
# async def get_session(session_id: str, session_manager = Depends(get_session_manager)):
#     """세션 정보 조회"""
#     session = session_manager.get_session(session_id)
#     if not session:
#         raise HTTPException(status_code=404, detail="세션을 찾을 수 없습니다.")
    
#     return {
#         "session_id": session_id,
#         "cart": session.get("cart", []),
#         "last_accessed": session.get("last_accessed", "")
#     }

# @app.delete("/ai/sessions/{session_id}/cart")
# async def clear_cart(session_id: str, session_manager = Depends(get_session_manager)):
#     """장바구니 비우기"""
#     result = session_manager.clear_cart(session_id)
#     if not result:
#         raise HTTPException(status_code=404, detail="세션을 찾을 수 없습니다.")
    
#     return {"success": True, "message": "장바구니가 비워졌습니다."}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)


# 응답 포맷팅을 위한 새로운 함수
def format_intent_response(response_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    의도 인식 결과를 클라이언트용 응답 형식으로 변환
    """
    intent_type = response_data.get("intent_type", IntentType.UNKNOWN)
    
    # 원본 응답에 data 필드가 없는 경우 기본값 설정
    if "data" not in response_data:
        response_data["data"] = {
            "pre_text": response_data.get("raw_text", ""),
            "post_text": response_data.get("raw_text", ""),
            "reply": "죄송합니다. 요청을 처리할 수 없습니다.",
            "status": ResponseStatus.UNKNOWN,
            "language": "KR",
            "session_id": "",
            "cart": [],
            "contents": [],
            "store_id": 1
        }
    
    # 템플릿 문자열 처리 추가 - {menu_name}, {options_summary} 등 치환
    if "data" in response_data and "reply" in response_data["data"]:
        reply = response_data["data"]["reply"]
        
        # 템플릿 패턴 확인 (예: {menu_name})
        if "{" in reply and "}" in reply:
            # contents에서 메뉴 정보 추출
            contents = response_data.get("data", {}).get("contents", [])
            if contents and len(contents) > 0:
                menu = contents[0]
                
                # {menu_name} 치환
                if "{menu_name}" in reply:
                    menu_name = menu.get("name", "")
                    reply = reply.replace("{menu_name}", menu_name)
                
                # {options_summary} 치환
                if "{options_summary}" in reply:
                    selected_options = menu.get("selected_options", [])
                    option_strs = []
                    for opt in selected_options:
                        if opt.get("option_details"):
                            option_name = opt.get("option_name", "")
                            option_value = opt["option_details"][0].get("value", "")
                            option_strs.append(f"{option_name}: {option_value}")
                    
                    options_summary = f" ({', '.join(option_strs)})" if option_strs else ""
                    reply = reply.replace("{options_summary}", options_summary)
            
            # 여전히 템플릿 변수가 남아있으면 빈 문자열로 대체
            import re
            reply = re.sub(r'\{[^}]+\}', '', reply)
            
            # 수정된 응답 저장
            response_data["data"]["reply"] = reply

    # 장바구니 항목 최적화
    if "data" in response_data and "cart" in response_data["data"]:
        optimized_cart = []
        for item in response_data["data"]["cart"]:
            # options 필드 제거하고 selected_options만 포함
            optimized_item = {
                "cart_id": item.get("cart_id", str(uuid.uuid4())),
                "menu_id": item.get("menu_id"),
                "quantity": item.get("quantity", 1),
                "name": item.get("name"),
                "name_en": item.get("name_en"),
                "description": item.get("description", ""),
                "base_price": item.get("base_price", 0),
                "total_price": item.get("total_price", 0),
                "image_url": item.get("image_url"),
                "selected_options": item.get("selected_options", [])
                # options 필드 제외
            }
            optimized_cart.append(optimized_item)
        
        response_data["data"]["cart"] = optimized_cart

    formatted_response = {
        "intent_type": intent_type,
        "confidence": response_data.get("confidence", 0.0),
        "recognized_menus": [],
        "pre_text": response_data.get("raw_text", ""),
        "post_text": response_data.get("raw_text", ""),
        "reply": response_data.get("data", {}).get("reply", ""),
        "search_query": response_data.get("search_query"),
        "payment_method": response_data.get("payment_method"),
        "raw_text": response_data.get("raw_text", ""),
        "screen_state": response_data.get("screen_state", ScreenState.MAIN),
        #"search_results": None,
        "data": response_data.get("data")
    }

    # 주문 의도인 경우 메뉴 정보 포맷팅
    if intent_type == IntentType.ORDER:
        contents = response_data.get("data", {}).get("contents", [])
        if contents:
            formatted_response["recognized_menus"] = contents
    
    # 검색 의도인 경우 검색 결과 포맷팅
    # elif intent_type == IntentType.SEARCH:
    #     formatted_response["search_results"] = response_data.get("data", {}).get("contents", [])
    
    return formatted_response


@app.post("/ai/test/recognize-intent")
async def test_recognize_intent(
    request: VoiceInputRequest,
    intent_service: IntentService = Depends(get_intent_service)
):
    """음성 입력 인식 테스트 API (디버깅용)"""
    try:
        # 의도 인식 및 처리
        raw_response = intent_service.process_request(
            text=request.text,
            language=request.language,
            screen_state=request.screen_state,
            store_id=request.store_id,
            session_id=request.session_id
        )
        
        # 원본 응답과 포맷팅된 응답 모두 반환
        formatted_response = format_intent_response(raw_response)
        
        return {
            "raw_response": raw_response,
            "formatted_response": formatted_response
        }
    
    except Exception as e:
        import traceback
        print(f"테스트 요청 처리 중 오류 발생: {str(e)}")
        print(traceback.format_exc())
        
        raise HTTPException(
            status_code=500,
            detail=f"테스트 요청 처리 중 오류 발생: {str(e)}"
        )
    

# main.py에 추가할 코드 (기존 startup_event 함수 수정)

@app.on_event("startup")
async def startup_event():
    print("음성 키오스크 API 서비스가 시작되었습니다. (Redis 세션 관리 활성화)")

    # 벡터 DB 초기화 (메뉴 서비스 필요)
    try:
        # 메뉴 서비스 생성
        mysql_host = os.getenv("MYSQL_HOST", "localhost")
        mysql_port = int(os.getenv("MYSQL_PORT", "3306"))
        mysql_user = os.getenv("MYSQL_USER", "root")
        mysql_pass = os.getenv("MYSQL_PASS", "password")
        mysql_db = os.getenv("MYSQL_DB", "kiosk")

        # DB 객체 생성
        db = MySQLConnector(
            host=mysql_host,
            port=mysql_port,
            user=mysql_user,
            password=mysql_pass,
            database=mysql_db
        )
        
        # MenuService 초기화 - db 객체 전달
        menu_service = MenuService(db)
        
        # 벡터 DB 서비스 초기화
        # vector_db_service = VectorDBService.get_instance()
        
        # 매장 ID 목록 
        store_ids = menu_service.get_all_store_ids()
        
        # 메뉴 데이터로 벡터 DB 초기화
        # document_count = vector_db_service.initialize_from_menus(menu_service, store_ids)
        # print(f"[앱 시작] 벡터 DB 초기화 완료: {document_count}개 메뉴 데이터")
        
    except Exception as e:
        print(f"[앱 시작] 벡터 DB 초기화 오류: {e}")
        import traceback
        traceback.print_exc()
    
    # Redis 세션 관리자 초기화
    app.state.session_manager = RedisSessionManager()
    
    # Redis 연결 상태 확인
    if app.state.session_manager.redis.ping():
        print("Redis 서버에 성공적으로 연결되었습니다.")
        
        # Redis 세션 정리 스케줄러 초기화 및 시작
        try:
            import threading
            import time
            import schedule
            
            # 세션 정리 스케줄러 생성
            app.state.cleanup_thread = None
            app.state.cleanup_running = False
            
            # 세션 정리 함수
            def cleanup_expired_sessions():
                try:
                    if not hasattr(app.state, "session_manager") or app.state.session_manager is None:
                        return
                    
                    # 현재 세션 수 조회
                    all_keys = app.state.session_manager.redis.keys(f"{app.state.session_manager.prefix}*")
                    total_sessions = len(all_keys)
                    
                    # 1시간 이상 미사용 세션 정리
                    import datetime
                    from datetime import timedelta
                    
                    cutoff_time = datetime.datetime.now() - timedelta(minutes=60)
                    cutoff_str = cutoff_time.isoformat()
                    
                    cleaned_count = 0
                    for key in all_keys:
                        try:
                            # 세션 데이터 추출
                            session_data = app.state.session_manager.redis.get(key)
                            if not session_data:
                                continue
                            
                            # JSON 파싱
                            import json
                            session = json.loads(session_data)
                            
                            # 마지막 접근 시간 확인
                            last_accessed = session.get("last_accessed", "")
                            if last_accessed and last_accessed < cutoff_str:
                                # 세션 삭제
                                app.state.session_manager.redis.delete(key)
                                cleaned_count += 1
                        except:
                            continue
                    
                    if cleaned_count > 0:
                        print(f"[세션 정리] {cleaned_count}개 만료된 세션 정리 완료 (전체 {total_sessions}개 중)")
                    
                    # 큰 세션 정리 (100KB 이상)
                    large_cleaned = 0
                    for key in app.state.session_manager.redis.keys(f"{app.state.session_manager.prefix}*"):
                        try:
                            # 세션 데이터 크기 확인
                            size = len(app.state.session_manager.redis.get(key) or "")
                            if size > 100 * 1024:  # 100KB 초과
                                # 기본 필드만 유지하고 최소화
                                session_data = app.state.session_manager.redis.get(key)
                                if not session_data:
                                    continue
                                
                                session = json.loads(session_data)
                                session_id = key.decode('utf-8').replace(app.state.session_manager.prefix, "")
                                
                                # 최소 필드만 유지
                                minimal_session = {
                                    "id": session.get("id", session_id),
                                    "created_at": session.get("created_at", ""),
                                    "last_accessed": session.get("last_accessed", ""),
                                    "cart": session.get("cart", [])[:5]  # 장바구니 최대 5개 항목만 유지
                                }
                                
                                # 다시 저장
                                minimal_data = json.dumps(minimal_session)
                                app.state.session_manager.redis.setex(
                                    key, 
                                    app.state.session_manager.timeout, 
                                    minimal_data
                                )
                                large_cleaned += 1
                        except:
                            continue
                    
                    if large_cleaned > 0:
                        print(f"[세션 정리] {large_cleaned}개 큰 세션 최적화 완료")
                
                except Exception as e:
                    print(f"[세션 정리] 오류 발생: {e}")
            
            # 스케줄러 스레드
            def run_scheduler():
                while app.state.cleanup_running:
                    schedule.run_pending()
                    time.sleep(1)
            
            # 스케줄 설정
            # 매시간 실행
            schedule.every().hour.do(cleanup_expired_sessions)
            
            # 매일 자정에 대규모 정리
            schedule.every().day.at("00:00").do(cleanup_expired_sessions)
            
            # 스케줄러 시작
            app.state.cleanup_running = True
            app.state.cleanup_thread = threading.Thread(target=run_scheduler, daemon=True)
            app.state.cleanup_thread.start()
            
            print("[앱 시작] Redis 세션 정리 스케줄러가 시작되었습니다.")
            
            # 시작 시 한 번 실행
            cleanup_expired_sessions()
            
        except Exception as e:
            print(f"[앱 시작] 세션 정리 스케줄러 초기화 오류: {e}")
    else:
        print("[경고] Redis 서버에 연결할 수 없습니다.")

# 종료 이벤트 수정
@app.on_event("shutdown")
async def shutdown_event():
    # 세션 정리 스케줄러 중지
    if hasattr(app.state, "cleanup_running"):
        app.state.cleanup_running = False
        
        if hasattr(app.state, "cleanup_thread") and app.state.cleanup_thread:
            app.state.cleanup_thread.join(timeout=1.0)
    
    print("음성 키오스크 API 서비스가 종료되었습니다.")

# 세션 정리 관련 API 추가
@app.post("/admin/sessions/cleanup")
async def cleanup_sessions(
    max_idle_minutes: int = 30,
    session_manager = Depends(get_session_manager)
):
    """세션 수동 정리"""
    try:
        # 현재 세션 수 조회
        all_keys = session_manager.redis.keys(f"{session_manager.prefix}*")
        total_sessions = len(all_keys)
        
        # 지정된 시간 이상 미사용 세션 정리
        import datetime
        from datetime import timedelta
        import json
        
        cutoff_time = datetime.datetime.now() - timedelta(minutes=max_idle_minutes)
        cutoff_str = cutoff_time.isoformat()
        
        cleaned_count = 0
        for key in all_keys:
            try:
                # 세션 데이터 추출
                session_data = session_manager.redis.get(key)
                if not session_data:
                    continue
                
                # JSON 파싱
                session = json.loads(session_data)
                
                # 마지막 접근 시간 확인
                last_accessed = session.get("last_accessed", "")
                if last_accessed and last_accessed < cutoff_str:
                    # 세션 삭제
                    session_manager.redis.delete(key)
                    cleaned_count += 1
            except:
                continue
        
        return {
            "total_sessions": total_sessions,
            "cleaned_count": cleaned_count,
            "max_idle_minutes": max_idle_minutes
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"세션 정리 중 오류 발생: {str(e)}")

@app.get("/admin/sessions/stats")
async def get_session_stats(
    session_manager = Depends(get_session_manager)
):
    """세션 통계 조회"""
    try:
        # 세션 키 조회
        all_keys = session_manager.redis.keys(f"{session_manager.prefix}*")
        total_count = len(all_keys)
        
        # 통계 데이터 초기화
        stats = {
            "total_sessions": total_count,
            "active_sessions": 0,  # 30분 내 활성
            "idle_sessions": 0,    # 30분 ~ 2시간
            "stale_sessions": 0,   # 2시간 이상
            "large_sessions": 0,   # 50KB 이상
            "avg_size_bytes": 0,
            "total_size_mb": 0,
            "recent_sessions": []  # 최근 10개 세션 샘플
        }
        
        # 시간 기준 설정
        import datetime
        from datetime import timedelta
        
        now = datetime.datetime.now()
        active_cutoff = (now - timedelta(minutes=30)).isoformat()
        idle_cutoff = (now - timedelta(hours=2)).isoformat()
        
        # 전체 크기 및 통계
        total_size = 0
        session_sizes = []
        import json
        
        # 세션 통계 수집 (최대 500개 샘플링)
        sampled_keys = all_keys[:500] if len(all_keys) > 500 else all_keys
        recent_sessions = []
        
        for key in sampled_keys:
            try:
                # 세션 데이터 추출
                session_data = session_manager.redis.get(key)
                if not session_data:
                    continue
                
                # 크기 계산
                size = len(session_data)
                total_size += size
                session_sizes.append(size)
                
                # JSON 파싱
                session = json.loads(session_data)
                session_id = key.decode('utf-8').replace(session_manager.prefix, "")
                
                # 마지막 접근 시간 확인
                last_accessed = session.get("last_accessed", "")
                
                # 활성 상태 분류
                if last_accessed > active_cutoff:
                    stats["active_sessions"] += 1
                elif last_accessed > idle_cutoff:
                    stats["idle_sessions"] += 1
                else:
                    stats["stale_sessions"] += 1
                
                # 큰 세션 카운트
                if size > 50 * 1024:  # 50KB
                    stats["large_sessions"] += 1
                
                # 최근 세션 정보 수집 (최대 10개)
                if len(recent_sessions) < 10:
                    cart_count = len(session.get("cart", []))
                    recent_sessions.append({
                        "id": session_id,
                        "last_accessed": last_accessed,
                        "cart_items": cart_count,
                        "size_kb": round(size / 1024, 2)
                    })
            
            except:
                continue
        
        # 평균 세션 크기 계산
        if session_sizes:
            stats["avg_size_bytes"] = round(sum(session_sizes) / len(session_sizes), 2)
            stats["total_size_mb"] = round(total_size / (1024 * 1024), 2)
        
        stats["recent_sessions"] = recent_sessions
        
        return stats
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"세션 통계 조회 중 오류 발생: {str(e)}")

@app.delete("/admin/sessions/{session_id}")
async def delete_session(
    session_id: str,
    session_manager = Depends(get_session_manager)
):
    """세션 명시적 삭제"""
    try:
        # 세션 키 구성
        session_key = f"{session_manager.prefix}{session_id}"
        
        # 세션 존재 여부 확인
        if not session_manager.redis.exists(session_key):
            raise HTTPException(status_code=404, detail="세션을 찾을 수 없습니다.")
        
        # 세션 삭제
        deleted = session_manager.redis.delete(session_key)
        
        return {
            "success": deleted > 0,
            "session_id": session_id
        }
    
    except HTTPException:
        raise
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"세션 삭제 중 오류 발생: {str(e)}")