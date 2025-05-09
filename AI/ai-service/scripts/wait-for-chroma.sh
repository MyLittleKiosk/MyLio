#!/bin/bash
set -e

# 최대 대기 시간 (초)
TIMEOUT=60
QUIET=0

HOST=chroma
PORT=8000

start_time=$(date +%s)

# 최대 대기 시간 동안 반복
while [ $(( $(date +%s) - start_time )) -lt $TIMEOUT ]; do
  # chroma 서비스의 상태 확인
  curl -s "http://$HOST:$PORT/api/v1/heartbeat" > /dev/null && {
    echo "Chroma is up and running!"
    exec "$@"  # 나머지 명령 실행
    exit 0
  }
  
  echo "Waiting for Chroma to be ready... ($(( TIMEOUT - $(( $(date +%s) - start_time )) )) seconds left)"
  sleep 2
done

echo "Timed out waiting for Chroma to be ready after $TIMEOUT seconds"
echo "Starting application anyway..."
exec "$@"  # 나머지 명령 실행