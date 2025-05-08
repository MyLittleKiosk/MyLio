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
from app.services.session_manager import SessionManager
from app.services.intent_service import IntentService

# 환경 변수 로드
load_dotenv()

# FastAPI 앱 생성
app = FastAPI(
    title="Voice Kiosk API",
    description="음성 키오스크용 API 서비스",
    version="0.1.0"
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
        print("[경고] 세션 매니저가 존재하지 않아서 생성합니다.")
        app.state.session_manager = SessionManager()
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
    print("음성 키오스크 API 서비스가 시작되었습니다.")
    
    # 세션 관리자 초기화
    app.state.session_manager = SessionManager()
    
    # 세션 정리 작업 예약 (실제 프로덕션에서는 백그라운드 작업으로 구현)
    # import asyncio
    # asyncio.create_task(cleanup_expired_sessions())

# 종료 이벤트
@app.on_event("shutdown")
async def shutdown_event():
    print("음성 키오스크 API 서비스가 종료되었습니다.")

# 화면 상태 목록 조회 엔드포인트
@app.get("/screen-states")
async def get_screen_states():
    """화면 상태 목록 조회"""
    return {"screen_states": [state.value for state in ScreenState]}

# 지원 언어 목록 조회 엔드포인트
@app.get("/languages")
async def get_languages():
    """지원 언어 목록 조회"""
    return {"languages": [lang.value for lang in Language]}

# 메뉴 조회 엔드포인트
@app.get("/menus/{store_id}")
async def get_store_menus(store_id: int, menu_service: MenuService = Depends(get_menu_service)):
    """스토어 ID에 해당하는 메뉴 정보 조회"""
    try:
        menus = menu_service.get_store_menus(store_id)
        return {"menus": list(menus.values())}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"메뉴 조회 중 오류 발생: {str(e)}")

# 음성 입력 처리 엔드포인트
@app.post("/recognize-intent", response_model=VoiceInputResponse)
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

# 세션 관리 엔드포인트 (옵션)
@app.get("/sessions/{session_id}")
async def get_session(session_id: str, session_manager = Depends(get_session_manager)):
    """세션 정보 조회"""
    session = session_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="세션을 찾을 수 없습니다.")
    
    return {
        "session_id": session_id,
        "cart": session.get("cart", []),
        "last_accessed": session.get("last_accessed", "")
    }

@app.delete("/sessions/{session_id}/cart")
async def clear_cart(session_id: str, session_manager = Depends(get_session_manager)):
    """장바구니 비우기"""
    result = session_manager.clear_cart(session_id)
    if not result:
        raise HTTPException(status_code=404, detail="세션을 찾을 수 없습니다.")
    
    return {"success": True, "message": "장바구니가 비워졌습니다."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)


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
            "language": "ko",
            "session_id": "",
            "cart": [],
            "contents": [],
            "store_id": 1
        }

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
        "search_results": None,
        "data": response_data.get("data")
    }

    # 주문 의도인 경우 메뉴 정보 포맷팅
    if intent_type == IntentType.ORDER:
        contents = response_data.get("data", {}).get("contents", [])
        if contents:
            formatted_response["recognized_menus"] = contents
    
    # 검색 의도인 경우 검색 결과 포맷팅
    elif intent_type == IntentType.SEARCH:
        formatted_response["search_results"] = response_data.get("data", {}).get("contents", [])
    
    return formatted_response


@app.post("/test/recognize-intent")
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