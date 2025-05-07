"""
custom_embeddings.py
OpenAI API를 직접 사용하는 임베딩 클래스
"""

import openai
import os
from typing import List, Any

class CustomEmbeddings:
    """LangChain 호환 커스텀 임베딩 클래스"""
    
    def __init__(self, api_key=None, model=None):
        openai.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model or "text-embedding-ada-002"
    
    def embed_documents(self, texts):
        """문서 임베딩"""
        if not texts:
            return []
        
        embeddings = []
        # 배치 처리
        batch_size = 20
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i+batch_size]
            response = openai.Embedding.create(
                input=batch,
                model=self.model
            )
            batch_embeddings = [data["embedding"] for data in response["data"]]
            embeddings.extend(batch_embeddings)
        
        return embeddings
    
    def embed_query(self, text):
        """쿼리 임베딩"""
        response = openai.Embedding.create(
            input=[text],
            model=self.model
        )
        
        return response["data"][0]["embedding"]