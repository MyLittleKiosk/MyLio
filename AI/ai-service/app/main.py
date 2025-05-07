import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# 상대 경로 대신 절대 경로 사용
from app.models.schemas import (
    VoiceInputRequest, 
    VoiceInputResponse, 
    ResponseGenerationRequest, 
    ResponseGenerationResponse
)
from app.services.intent_recognition import IntentRecognitionService
from app.services.response_generation import ResponseGenerationService
from app.services.rag_service import RAGService
from app.db.vector_store import VectorStore
from app.db.mysql_connector import DSN

# 환경 변수 로드
load_dotenv()

# 앱 인스턴스 생성
app = FastAPI(
    title="Voice Kiosk RAG API",
    description="음성 키오스크를 위한 의도 인식 및 응답 생성 API",
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

# 서비스 인스턴스 초기화
@app.on_event("startup")
async def startup_event():
    # 벡터 DB 초기화 (DSN으로 MySQL 설정 전달)
    vector_store = VectorStore(
        persist_directory="chroma_db",
        mysql_dsn=DSN
    )
    app.state.vector_store = vector_store
    
    # 데이터가 없으면 벡터 DB 구축
    try:
        vector_store.client.get_collection("menu_collection")
        print("메뉴 컬렉션이 이미 존재합니다.")
    except:
        print("메뉴 컬렉션 구축 중...")
        # MySQL에서 데이터 가져와 컬렉션 구축
        count = vector_store.create_menu_collection()
        print(f"{count}개의 메뉴 데이터 추가 완료")
    
    try:
        vector_store.client.get_collection("option_collection")
        print("옵션 컬렉션이 이미 존재합니다.")
    except:
        print("옵션 컬렉션 구축 중...")
        # MySQL에서 데이터 가져와 컬렉션 구축
        count = vector_store.create_option_collection()
        print(f"{count}개의 옵션 데이터 추가 완료")
    
    # RAG 서비스 초기화
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY 환경 변수가 설정되지 않았습니다.")
    
    rag_service = RAGService(vector_store, openai_api_key)
    
    # 서비스 인스턴스 설정
    app.state.intent_recognition_service = IntentRecognitionService(rag_service)
    app.state.response_generation_service = ResponseGenerationService(rag_service)


# 의도 인식 API 엔드포인트
@app.post("/recognize_intent", response_model=VoiceInputResponse)
async def recognize_intent(request: VoiceInputRequest):
    """음성 인식 텍스트에서 의도 인식 API"""
    try:
        text = request.text
        language = request.language
        screen_state = request.screen_state
        store_id = request.store_id
        
        # correct_text 호출 제거
        # 바로 recognize_intent 메서드 호출
        result = app.state.intent_recognition_service.recognize_intent(
            text, 
            language, 
            screen_state, 
            store_id
        )
        
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"의도 인식 중 오류가 발생했습니다: {str(e)}"
        )


# 응답 생성 API 엔드포인트
@app.post("/generate_response", response_model=ResponseGenerationResponse)
async def generate_response(request: ResponseGenerationRequest):
    """검증된 정보를 바탕으로 사용자에게 응답 메시지를 생성"""
    response = app.state.response_generation_service.generate_response(
        request.status,
        request.menus,
        request.raw_text,
        request.screen_state
    )
    
    return ResponseGenerationResponse(response=response)


# 벡터 DB 재구축 API (개발용)
@app.post("/rebuild_vector_db")
async def rebuild_vector_db(store_id: int = None):
    """벡터 DB 재구축 (개발 환경에서만 사용)"""
    vector_store = app.state.vector_store
    
    # 메뉴 컬렉션 재구축
    menu_count = vector_store.create_menu_collection(store_id)
    
    # 옵션 컬렉션 재구축
    option_count = vector_store.create_option_collection(store_id)
    
    return {
        "status": "success",
        "menu_count": menu_count,
        "option_count": option_count,
        "store_id": store_id
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)