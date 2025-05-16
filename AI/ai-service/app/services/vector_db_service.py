# # app/services/vector_db_service.py
# import os
# import time
# import re
# from typing import List, Dict, Any, Optional
# from langchain.schema import Document
# from langchain.embeddings.openai import OpenAIEmbeddings
# from langchain.vectorstores import Chroma
# import chromadb
# from chromadb.config import Settings
# from chromadb.utils import embedding_functions

# class VectorDBService:
#     """벡터 DB 서비스"""
    
#     _instance = None
    
#     @classmethod
#     def get_instance(cls):
#         """싱글톤 인스턴스 반환"""
#         if cls._instance is None:
#             cls._instance = cls()
#         return cls._instance
    
#     # URL 대신 host와 port를 사용하는 방식
#     def __init__(self):
#         """벡터 DB 서비스 초기화"""
#         self.chroma_host = os.getenv("CHROMA_HOST", "http://localhost:8000")
#         self.collection_name = os.getenv("COLLECTION_NAME", "menu_collection")
        
#         print(f"[벡터 DB] 초기화: 호스트={self.chroma_host}, 컬렉션={self.collection_name}")
        
#         # URL에서 호스트와 포트 추출
#         import urllib.parse
#         parsed_url = urllib.parse.urlparse(self.chroma_host)
#         host = parsed_url.hostname or "localhost"
#         port = parsed_url.port or 8000
        
#         # OpenAI 임베딩 초기화
#         self.embeddings = OpenAIEmbeddings(
#             model="text-embedding-ada-002",
#             openai_api_key=os.getenv("OPENAI_API_KEY")
#         )
        
#         # ChromaDB 클라이언트 초기화 (HTTP 클라이언트)
#         try:
#             # 새로운 방식으로 먼저 시도
#             self.client = chromadb.HttpClient(host=host, port=port)
#             print(f"[벡터 DB] ChromaDB 클라이언트 초기화 성공 (host={host}, port={port})")
#         except TypeError:
#             # 구버전 호환성을 위한 시도
#             try:
#                 self.client = chromadb.HttpClient(url=self.chroma_host)
#                 print(f"[벡터 DB] ChromaDB 클라이언트 초기화 성공 (url={self.chroma_host})")
#             except Exception as e:
#                 print(f"[벡터 DB] ChromaDB 클라이언트 초기화 실패: {e}")
#                 self.client = None
        
#         # 컬렉션 초기화 (이미 존재하는지 확인)
#         self._init_collection()
    
#     def _init_collection(self):
#         """컬렉션 초기화 (확인만 수행)"""
#         try:
#             # 클라이언트가 없으면 컬렉션을 초기화할 수 없음
#             if self.client is None:
#                 print("[벡터 DB] 클라이언트가 초기화되지 않아 컬렉션을 초기화할 수 없습니다.")
#                 self.collection = None
#                 return

#             # 기존 컬렉션이 있는지 확인
#             collections = self.client.list_collections()
#             collection_exists = any(c.name == self.collection_name for c in collections)
            
#             if collection_exists:
#                 # 컬렉션이 있으면 가져오기
#                 self.collection = self.client.get_collection(name=self.collection_name)
#                 count = self.collection.count()
#                 print(f"[벡터 DB] 기존 컬렉션 로드됨: {self.collection_name}, 항목 수: {count}")
#             else:
#                 print(f"[벡터 DB] 컬렉션이 존재하지 않음: {self.collection_name}, 새로 생성합니다.")
#                 # 컬렉션 생성
#                 try:
#                     self.collection = self.client.create_collection(name=self.collection_name)
#                     print(f"[벡터 DB] 새 컬렉션 생성됨: {self.collection_name}")
#                 except Exception as create_error:
#                     print(f"[벡터 DB] 컬렉션 생성 실패: {create_error}")
#                     self.collection = None
#         except Exception as e:
#             print(f"[벡터 DB] 컬렉션 초기화 확인 중 오류: {e}")
#             import traceback
#             traceback.print_exc()
#             self.collection = None
    
#     def initialize_from_menus(self, menu_service, store_ids=[1]):
#         """메뉴 데이터로 벡터 DB 초기화"""
#         # 컬렉션이 초기화되지 않았으면 초기화 실패
#         if self.collection is None:
#             print("[벡터 DB] 컬렉션이 초기화되지 않아 메뉴 데이터를 로드할 수 없습니다.")
#             return 0

#         start_time = time.time()
#         print("[벡터 DB] 메뉴 데이터로 벡터 DB 초기화 시작")
#         """메뉴 데이터로 벡터 DB 초기화"""
#         start_time = time.time()
#         print("[벡터 DB] 메뉴 데이터로 벡터 DB 초기화 시작")
        
#         # 기존 데이터 삭제
#         try:
#             count = self.collection.count()
#             if count > 0:
#                 print(f"[벡터 DB] 기존 {count}개 문서 삭제")
#                 self.collection.delete()
#                 # 컬렉션 재생성
#                 self.collection = self.client.create_collection(
#                     name=self.collection_name,
#                     embedding_function=self.openai_ef
#                 )
#         except Exception as e:
#             print(f"[벡터 DB] 기존 데이터 삭제 오류: {e}")
        
#         # 문서, 메타데이터, ID 리스트
#         documents = []
#         metadatas = []
#         ids = []
        
#         # 매장별 메뉴 로드 및 문서 생성
#         for store_id in store_ids:
#             store_menus = menu_service.get_store_menus(store_id)
#             print(f"[벡터 DB] 매장 ID {store_id}: {len(store_menus)} 메뉴 로드됨")
            
#             # ChromaDB 문서 생성
#             for menu_id, menu in store_menus.items():
#                 # 메뉴 정보를 텍스트로 변환
#                 menu_text = self._format_menu_as_text(menu, store_id)
                
#                 # 메타데이터 생성 (문자열 값만 포함)
#                 metadata = {
#                     "menu_id": str(menu_id),
#                     "store_id": str(store_id),
#                     "name_kr": menu.get("name_kr", ""),
#                     "name_en": menu.get("name_en", ""),
#                     "price": str(menu.get("price", 0)),
#                     "category_id": str(menu.get("category_id", "")),
#                 }
#                 # 태그 정보 추가 (텍스트로 변환)
#                 if menu.get("tags"):
#                     tags_text = ", ".join([
#                         f"{tag.get('tag_kr', '')} {tag.get('tag_en', '')}" 
#                         for tag in menu.get("tags", [])
#                     ])
#                     metadata["tags_text"] = tags_text

#                 # 원재료 정보 추가 (텍스트로 변환)
#                 if menu.get("ingredients"):
#                     ingredients_text = ", ".join([
#                         f"{ing.get('name_kr', '')} {ing.get('name_en', '')}"
#                         for ing in menu.get("ingredients", [])
#                     ])
#                     metadata["ingredients_text"] = ingredients_text
                
#                 documents.append(menu_text)
#                 metadatas.append(metadata)
#                 ids.append(f"menu_{menu_id}")
                
#                 # 최적화: 100개씩 일괄 처리
#                 if len(documents) >= 100:
#                     self.collection.add(
#                         documents=documents,
#                         metadatas=metadatas,
#                         ids=ids
#                     )
#                     documents, metadatas, ids = [], [], []
        
#         # 남은 문서 처리
#         if documents:
#             self.collection.add(
#                 documents=documents,
#                 metadatas=metadatas,
#                 ids=ids
#             )
        
#         end_time = time.time()
#         total_count = self.collection.count()
#         print(f"[벡터 DB] 초기화 완료: {total_count}개 문서, 소요 시간: {end_time - start_time:.2f}초")
        
#         return total_count
    
#     def _format_menu_as_text(self, menu: Dict[str, Any], store_id: int) -> str:
#         """메뉴 정보를 검색 가능한 텍스트로 포맷팅"""
#         # 메뉴 타입/카테고리를 우선적으로 강조
#         category_name = menu.get("category_name", "")
        
#         # 1. 카테고리 강조
#         category_emphasis = ""
#         if menu.get("category_id") == 107:  # 디저트 카테고리
#             category_emphasis = "디저트 카테고리 디저트 카테고리 디저트 " * 3
#         elif "에이드" in menu.get("name_kr", ""):
#             category_emphasis = "에이드 음료 에이드 음료 에이드 " * 3
#         # ... 다른 카테고리
        
#         # 2. 특수 속성 강조
#         special_emphasis = ""
#         if "디카페인" in menu.get("name_kr", ""):
#             special_emphasis = "디카페인 카페인없음 디카페인 카페인없음 " * 3
        
#         # 3. 우유 포함 여부 강조
#         milk_emphasis = ""
#         has_milk = False
#         # 이름에 우유 관련 키워드가 있는지 확인
#         if any(keyword in menu.get("name_kr", "").lower() for keyword in ["우유", "밀크", "라떼"]):
#             has_milk = True
#         # 원재료에 우유가 있는지 확인
#         for ing in menu.get("ingredients", []):
#             if "우유" in ing.get("name_kr", "").lower():
#                 has_milk = True
        
#         if has_milk:
#             milk_emphasis = "우유 포함 유제품 포함 우유 " * 3
#         else:
#             milk_emphasis = "우유 없음 유제품 없음 우유 미포함 " * 3
        
#         # 기본 메뉴 정보 + 강조 텍스트
#         lines = [
#             category_emphasis,
#             special_emphasis,
#             milk_emphasis,
#             f"메뉴: {menu.get('name_kr', '')}",
#             f"영문명: {menu.get('name_en', '')}",
#             f"가격: {menu.get('price', 0)}원",
#             f"설명: {menu.get('description', '')}"
#         ]
        
#         # 카테고리 정보
#         category_id = menu.get("category_id")
#         category_name = menu.get("category_name", f"카테고리 {category_id}")
#         lines.append(f"카테고리: {category_name}")

#         # 태그 정보
#         if menu.get("tags"):
#             tag_names = [tag.get("tag_kr", "") for tag in menu.get("tags", [])]
#             tag_names_en = [tag.get("tag_en", "") for tag in menu.get("tags", [])]
#             if tag_names:
#                 lines.append(f"태그: {', '.join(filter(None, tag_names))}")
#             if tag_names_en:
#                 lines.append(f"태그(영문): {', '.join(filter(None, tag_names_en))}")
        
#         # 원재료 정보
#         if menu.get("ingredients"):
#             ingredient_names = [ing.get("name_kr", "") for ing in menu.get("ingredients", [])]
#             ingredient_names_en = [ing.get("name_en", "") for ing in menu.get("ingredients", [])]
#             if ingredient_names:
#                 lines.append(f"원재료: {', '.join(filter(None, ingredient_names))}")
#             if ingredient_names_en:
#                 lines.append(f"원재료(영문): {', '.join(filter(None, ingredient_names_en))}")
        
#         # 영양성분 정보 - 리스트 형태 대응
#         if menu.get("nutrition"):
#             nutrition_data = menu.get("nutrition")
#             nutrition_lines = ["영양성분:"]
            
#             # nutrition이 리스트인 경우
#             if isinstance(nutrition_data, list):
#                 for item in nutrition_data:
#                     name = item.get("name", "")
#                     formatted_value = item.get("formatted", "")
#                     nutrition_lines.append(f"- {name}: {formatted_value}")
#             # nutrition이 딕셔너리인 경우 (기존 코드 유지)
#             elif isinstance(nutrition_data, dict):
#                 for key, value in nutrition_data.items():
#                     nutrition_lines.append(f"- {key}: {value}")
            
#             lines.append("\n".join(nutrition_lines))
        
#         # 옵션 정보
#         if menu.get("options"):
#             option_lines = ["옵션:"]
#             for opt in menu.get("options", []):
#                 opt_name = opt.get("option_name", "")
#                 required = "필수" if opt.get("required", False) else "선택"
#                 option_lines.append(f"- {opt_name} ({required})")
                
#                 # 옵션 상세 정보
#                 for detail in opt.get("option_details", []):
#                     value = detail.get("value", "")
#                     price = detail.get("additional_price", 0)
#                     price_text = f"+{price}원" if price > 0 else ""
#                     option_lines.append(f"  * {value} {price_text}")
            
#             lines.append("\n".join(option_lines))
        
#         # 특별 키워드 추가 (검색 최적화)
#         special_keywords = []
        
#         # 디카페인 관련 키워드
#         if any("디카페인" in tag.get("tag_kr", "").lower() for tag in menu.get("tags", [])) or \
#         "디카페인" in menu.get("name_kr", "").lower() or \
#         "decaf" in menu.get("name_en", "").lower():
#             special_keywords.extend(["디카페인", "카페인 없는", "카페인 제거"])
        
#        # 우유 변경 옵션 파악 및 키워드 삽입
#         for opt in menu.get("options", []):
#             if "우유" in opt.get("option_name", "") or "milk" in opt.get("option_name", ""):
#                 for detail in opt.get("option_details", []):
#                     val = detail.get("value", "").lower()
#                     if "두유" in val or "soy" in val:
#                         special_keywords.extend(["두유", "비유제품", "유제품 없음", "plant milk", "soy milk"])
#                     if "오트" in val or "oat" in val:
#                         special_keywords.extend(["오트", "오트 밀크", "유제품 없음", "oat milk"])
#                     if "일반" in val or "우유" in val:
#                         special_keywords.append("유제품")

#         # 디카페인 확인 - 이름, 설명, 옵션명에 기반
#         if "디카페인" in menu.get("name_kr", "").lower() or \
#         "decaf" in menu.get("name_en", "").lower() or \
#         "디카페인" in menu.get("description", "").lower():
#             special_keywords.extend(["디카페인", "카페인 없음", "카페인 제거", "decaf"])

        
#         # 비건 관련 키워드
#         if any("비건" in tag.get("tag_kr", "").lower() for tag in menu.get("tags", [])) or \
#         any("vegan" in tag.get("tag_en", "").lower() for tag in menu.get("tags", [])):
#             special_keywords.extend(["비건", "베지테리안", "채식", "식물성"])
        
#         # 특별 다이어트 관련 키워드
#         if any("저칼로리" in tag.get("tag_kr", "").lower() for tag in menu.get("tags", [])) or \
#         any("low calorie" in tag.get("tag_en", "").lower() for tag in menu.get("tags", [])):
#             special_keywords.extend(["저칼로리", "다이어트", "라이트"])
        
#         # 계절 한정 키워드
#         if any("시즌" in tag.get("tag_kr", "").lower() for tag in menu.get("tags", [])) or \
#         any("season" in tag.get("tag_en", "").lower() for tag in menu.get("tags", [])):
#             special_keywords.extend(["시즌 한정", "계절 메뉴", "한정판"])
        
#         # 키워드가 있으면 추가
#         if special_keywords:
#             lines.append(f"관련 키워드: {', '.join(special_keywords)}")
#         return "\n".join(lines)
    
#     def search(self, query: str, store_id: Optional[int] = None, category_filter: Optional[str] = None, k: int = 5) -> List[Dict[str, Any]]:
#         """벡터 검색 실행"""
#         try:
#             start_time = time.time()
            
#             # 검색 필터 설정
#             where_filter = None
#             if store_id is not None:
#                 where_filter = {"store_id": str(store_id)}
        
#             # 카테고리 필터 추가 (예: '에이드' 검색 시 에이드 카테고리만)
#             if category_filter:
#                 where_filter["category_name"] = category_filter
            
#             # ChromaDB 검색 수행
#             results = self.collection.query(
#                 query_texts=[query],
#                 n_results=k,
#                 where=where_filter
#             )
            
#             end_time = time.time()
#             query_time = end_time - start_time
            
#             # 결과 포맷팅
#             formatted_results = []
            
#             if results["metadatas"] and results["metadatas"][0]:
#                 for idx, metadata in enumerate(results["metadatas"][0]):
#                     distance = results["distances"][0][idx] if "distances" in results and results["distances"][0] else 1.0
#                     similarity = 1.0 - distance  # 거리를 유사도로 변환
                    
#                     # menu_id를 정수로 변환
#                     menu_id = int(metadata.get("menu_id")) if metadata.get("menu_id") else None
                    
#                     formatted_results.append({
#                         "menu_id": menu_id,
#                         "store_id": int(metadata.get("store_id")) if metadata.get("store_id") else None,
#                         "name_kr": metadata.get("name_kr", ""),
#                         "name_en": metadata.get("name_en", ""),
#                         "price": int(metadata.get("price", 0)),
#                         "category_id": int(metadata.get("category_id")) if metadata.get("category_id") else None,
#                         "similarity": similarity,
#                         "text": results["documents"][0][idx] if "documents" in results else ""
#                     })
            
#             print(f"[벡터 DB] 검색 완료: 쿼리='{query}', 결과={len(formatted_results)}개, 소요 시간={query_time:.3f}초")
#             return formatted_results
            
#         except Exception as e:
#             print(f"[벡터 DB] 검색 오류: {e}")
#             import traceback
#             traceback.print_exc()
#             return []
    
#     def get_stats(self):
#         """벡터 DB 통계 정보"""
#         try:
#             count = self.collection.count()
#             return {
#                 "collection_name": self.collection_name,
#                 "document_count": count,
#                 "chroma_host": self.chroma_host
#             }
#         except Exception as e:
#             print(f"[벡터 DB] 통계 조회 오류: {e}")
#             return {
#                 "collection_name": self.collection_name,
#                 "error": str(e),
#                 "chroma_host": self.chroma_host
#             }