from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import requests
import os
import io
from dotenv import load_dotenv
from typing import Dict, Any
import urllib.parse
from google.cloud import texttospeech

# Load environment variables
load_dotenv()

app = FastAPI()

# CORS 설정
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173")
origins = [origin.strip() for origin in ALLOWED_ORIGINS.split(",")]

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

GOOGLE_TTS_API_URL = os.getenv("GOOGLE_TTS_API_URL")
GOOGLE_TTS_API_SECRET = os.getenv("GOOGLE_TTS_API_SECRET")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

SUPPORTED_FORMATS = { "audio/mp3", "audio/wav" }

@app.post("/voice/clova/stt")
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


@app.post("/voice/google/tts")
async def google_tts(text: str = Form(...)):
    try:
        # Google TTS 클라이언트 초기화
        client = texttospeech.TextToSpeechClient()

        # 사용할 음성 선택
        voice_name = "ko-KR-Chirp3-HD-Gacrux"

        # 텍스트 입력 생성
        synthesis_input = texttospeech.SynthesisInput(text=text)

        # 음성 선택
        voice = texttospeech.VoiceSelectionParams(
            language_code=voice_name.split("-")[0] + "-" + voice_name.split("-")[1],
            name=voice_name,
            ssml_gender=texttospeech.SsmlVoiceGender.SSML_VOICE_GENDER_UNSPECIFIED,
        )

        # 출력 형식 설정
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

        # 음성 생성
        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

        # 음성 출력
        return StreamingResponse(io.BytesIO(response.audio_content), media_type="audio/mp3")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Google API 요청 실패: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        ssl_keyfile="localhost-key.pem",
        ssl_certfile="localhost.pem"
    ) 