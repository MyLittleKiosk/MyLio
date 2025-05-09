FROM python:3.11-slim

# 필수 리눅스 패키지
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential curl && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 의존성 레이어 분리 (캐싱 최적화)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY ./app /app/app
COPY ./scripts/wait-for-chroma.sh /app/wait-for-chroma.sh

# 실행 권한 부여
RUN chmod +x /app/wait-for-chroma.sh

# 포트 노출
EXPOSE 8000

# 애플리케이션 실행
CMD ["/app/wait-for-chroma.sh", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--log-level", "info"]