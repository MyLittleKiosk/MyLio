"""
response_generation.py
응답 생성 서비스
"""

from typing import Dict, Any, List
from .rag_service import RAGService


class ResponseGenerationService:
    def __init__(self, rag_service: RAGService):
        self.rag_service = rag_service
    
    def generate_response(self, status: str, menus: List[Dict[str, Any]], raw_text: str, screen_state: str) -> str:
        """응답 생성"""
        return self.rag_service.generate_response(status, menus, raw_text, screen_state)