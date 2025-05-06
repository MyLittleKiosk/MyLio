# app/vectordb.py
import os, chromadb, functools
from chromadb.errors import InvalidCollectionException
from langchain_openai import OpenAIEmbeddings
from typing import List, Dict, Any

# ──────────────────────────────────────────────
CHROMA_HOST = os.getenv("CHROMA_HOST", "http://chroma:8000")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "menu_embeddings")
EMB = OpenAIEmbeddings(model="text-embedding-3-small")
client = chromadb.HttpClient(host=CHROMA_HOST)
# ──────────────────────────────────────────────

@functools.lru_cache(maxsize=1)
def _get_coll():
    """
    최신 컬렉션 핸들 반환.
    ingest 쪽에서 새로 만들면 다음 호출 때 즉시 갱신됩니다.
    """
    try:
        return client.get_collection(COLLECTION_NAME)
    except InvalidCollectionException:
        # ingest 가 아직 못 만들었을 수도 있으니 생성해 둠
        return client.create_collection(COLLECTION_NAME)

def _refresh_coll():
    """ingest.py 에서 컬렉션 재생성 직후 호출 → 캐시 무효화"""
    _get_coll.cache_clear()

# ──────────────────────────────────────────────
def menu_id(name: str, store_id: int, language: str = "kr") -> int:
    """
    메뉴 이름으로 ID 찾기
    언어에 따라 다르게 검색 가능 (kr/en)
    """
    if not name:
        return None
        
    # 언어별 검색어 변형 (다국어 지원)
    query = name
    
    # 임베딩 생성
    vec = EMB.embed_query(query)
    coll = _get_coll()
    
    # 검색 조건에 매장 ID 추가
    res = coll.query(
        query_embeddings=[vec],
        n_results=1,
        where={"store_id": store_id},
    )
    
    # 결과가 있으면 메뉴 ID 반환
    if res["ids"] and res["ids"][0]:
        return res["metadatas"][0][0]["menu_id"]
    return None

def get_menu_name(menu_id: int, store_id: int, language: str = "kr") -> str:
    """메뉴 ID로 이름 가져오기 (언어별)"""
    from .db import store_meta
    meta = store_meta(store_id)
    
    if menu_id in meta["menus"]:
        # 언어에 맞는 필드 선택
        name_field = "name_kr" if language == "kr" else "name_en"
        return meta["menus"][menu_id].get(name_field, "")
    return None

def search_menu(query: str, store_id: int, n_results: int = 3) -> List[Dict[str, Any]]:
    """메뉴 검색 - 벡터 유사도 검색"""
    if not query:
        return []
        
    vec = EMB.embed_query(query)
    coll = _get_coll()
    
    # 검색 조건에 매장 ID 추가
    res = coll.query(
        query_embeddings=[vec],
        n_results=n_results,
        where={"store_id": store_id},
    )
    
    results = []
    if res["metadatas"] and res["metadatas"][0]:
        for i, meta in enumerate(res["metadatas"][0]):
            results.append({
                "menuId": meta["menu_id"],
                "menuName": meta["name"],
                "distance": res["distances"][0][i] if "distances" in res and res["distances"][0] else None
            })
    
    return results