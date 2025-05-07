# 1. 가벼운 파이썬 베이스
FROM python:3.11-slim

# 2. 필수 리눅스 패키지 (gcc 없으면 chromadb·tiktoken 컴파일 실패)
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

# 3. 작업 디렉터리
WORKDIR /app

RUN pip install --no-cache-dir langchain-openai

# 4. 프로젝트 파일 복사
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
# .env 는 로컬에서 마운트 or compose env_file 로 주입

# 5. FastAPI 실행
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--log-level", "info"]
