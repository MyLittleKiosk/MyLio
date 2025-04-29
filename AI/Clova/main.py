from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import requests
import os
from dotenv import load_dotenv
from typing import Dict, Any

# 환경 변수 로드
load_dotenv()

app = FastAPI()

# CORS 설정
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Clova Speech API 설정
CLOVA_API_URL = os.getenv("CLOVA_API_INVOKE_URL")
API_KEY_ID = os.getenv("CLOVA_API_KEY_ID")
API_SECRET = os.getenv("CLOVA_API_SECRET")

# 지원하는 파일 형식
SUPPORTED_FORMATS = {
    "audio/wav",
    "audio/mp3",
    "audio/mp4",
    "audio/ogg",
    "audio/flac"
}

def validate_file(file: UploadFile) -> None:
    """파일 유효성 검사"""
    if file.content_type not in SUPPORTED_FORMATS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file format. Supported formats: {', '.join(SUPPORTED_FORMATS)}"
        )

@app.post("/clova/stt")
async def clova_stt(file: UploadFile = File(...)) -> Dict[str, Any]:
    """
    음성 파일을 텍스트로 변환하는 엔드포인트
    
    Args:
        file (UploadFile): 변환할 음성 파일
        
    Returns:
        Dict[str, Any]: 변환된 텍스트와 상태 정보
    """
    try:
        # 파일 유효성 검사
        validate_file(file)
        
        # 파일 읽기
        file_bytes = await file.read()
        
        # API 요청 준비
        files = {
            "media": (file.filename, file_bytes, file.content_type),
            "language": (None, "ko-KR"),
        }
        headers = {
            "X-NCP-APIGW-API-KEY-ID": API_KEY_ID,
            "X-NCP-APIGW-API-KEY": API_SECRET,
        }

        # Clova API 호출
        response = requests.post(CLOVA_API_URL, files=files, headers=headers)
        
        # API 응답 처리
        if response.status_code == 200:
            result = response.json()
            return {
                "status": "success",
                "data": result,
                "message": "음성 변환이 성공적으로 완료되었습니다."
            }
        else:
            error_detail = response.json().get("error", {}).get("message", "Unknown error")
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Clova API Error: {error_detail}"
            )
            
    except HTTPException as he:
        raise he
    except requests.RequestException as e:
        raise HTTPException(
            status_code=500,
            detail=f"Clova API 요청 중 오류가 발생했습니다: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"서버 오류가 발생했습니다: {str(e)}"
        )