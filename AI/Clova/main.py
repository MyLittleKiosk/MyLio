from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
from dotenv import load_dotenv
from typing import Dict, Any
import urllib.parse

# Load environment variables
load_dotenv()

app = FastAPI()

# CORS 설정
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "https://localhost:3000")
origins = [origin.strip() for origin in ALLOWED_ORIGINS.split(",")]
print(origins)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Clova Speech API 설정
CLOVA_API_URL = os.getenv("CLOVA_API_INVOKE_URL")
CLOVA_API_SECRET = os.getenv("CLOVA_API_SECRET")

SUPPORTED_FORMATS = { "audio/mp3", "audio/wav" }

@app.post("/clova/stt")
async def clova_stt(file: UploadFile = File(...)) -> Dict[str, Any]:
    if file.content_type not in SUPPORTED_FORMATS:
        raise HTTPException(status_code=400, detail="지원되지 않는 오디오 형식입니다. (mp3, wav만 지원)")

    try:
        file_bytes = await file.read()
        
        # 변환 없이 바로 사용
        converted_bytes = file_bytes

        # 쿼리 파라미터
        base_url = os.getenv("CLOVA_API_INVOKE_URL")
        params = {
            "lang": "Kor",
        }
        url = f"{base_url}?{urllib.parse.urlencode(params)}"

        headers = {
            "Content-Type": "application/octet-stream",
            "X-CLOVASPEECH-API-KEY": CLOVA_API_SECRET
        }

        response = requests.post(
            url,
            headers=headers,
            data=converted_bytes,
        )

        print(f"[Clova Speech AI] Status: {response.status_code}")
        print(f"[Clova Speech AI] Body: {response.text}")

        if response.status_code == 200:
            result = response.json()
            return {
                "status": "success",
                "text": result.get("text", ""),
                "quota": result.get("quota"), # 음성 길이
            }
        else:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.text
            )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Clova API 요청 실패: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="localhost",
        port=8000,
        reload=True,
        ssl_keyfile="localhost-key.pem",
        ssl_certfile="localhost.pem"
    ) 