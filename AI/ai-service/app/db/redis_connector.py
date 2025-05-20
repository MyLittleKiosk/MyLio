# app/db/redis_connector.py
import redis
import os
from typing import Optional

class RedisConnector:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RedisConnector, cls).__new__(cls)
            cls._instance.client = redis.Redis(
                host=os.getenv("REDIS_HOST", "localhost"),
                port=int(os.getenv("REDIS_PORT", 6379)),
                db=0,
                password=os.getenv("REDIS_PASSWORD", ""),
                decode_responses=True  # 문자열 자동 디코딩
            )
        return cls._instance
    
    def get_client(self) -> redis.Redis:
        """Redis 클라이언트 인스턴스 반환"""
        return self.client
    
    def ping(self) -> bool:
        """Redis 연결 확인"""
        try:
            return self.client.ping()
        except Exception as e:
            print(f"Redis 연결 오류: {e}")
            return False