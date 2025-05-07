"""
vector_store.py
벡터 db 연결 관리
벡터 데이터 베이스 구축
"""

import os
from typing import List, Dict, Any
import chromadb
from chromadb.config import Settings
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from .mysql_connector import MySQLConnector, DSN

class VectorStore:
    def __init__(self, 
                 persist_directory: str = "chroma_db",
                 mysql_dsn: Dict = None):
        self.persist_directory = persist_directory
        
        # 새 버전의 OpenAIEmbeddings 사용
        self.embedding_function = OpenAIEmbeddings(
            model="text-embedding-ada-002",
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )

        # ChromaDB 클라이언트 설정
        self.client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Langchain 용 Chroma 인스턴스
        self.db = Chroma(
            persist_directory=persist_directory,
            embedding_function=self.embedding_function,
            client=self.client
        )
        
        # MySQL 연결
        self.mysql = MySQLConnector(dsn=mysql_dsn)
    
    def create_menu_collection(self, store_id: int = None):
        """MySQL에서 메뉴 데이터를 가져와 벡터 DB 컬렉션 생성"""
        # 기존 컬렉션이 있으면 삭제
        try:
            self.client.delete_collection("menu_collection")
        except:
            pass
        
        # 새 컬렉션 생성
        collection = self.client.create_collection("menu_collection")
        
        # MySQL에서 메뉴 데이터 로드
        menu_data = self.mysql.get_menus(store_id)
        
        if not menu_data:
            print("메뉴 데이터가 없습니다.")
            return 0
        
        # 각 메뉴마다 문서 생성
        documents = []
        metadatas = []
        ids = []
        
        for idx, menu in enumerate(menu_data):
            # 메뉴 이름 (한글 + 영어)
            text = f"{menu['name_kr']} {menu['name_en']}"
            
            # 메뉴 설명 추가
            if menu.get('description'):
                text += f" {menu['description']}"
            
            # 태그 추가
            tag_texts = []
            if 'tags' in menu and menu['tags']:
                for tag in menu['tags']:
                    text += f" {tag['tag_kr']} {tag['tag_en']}"
                    tag_texts.append(f"{tag['tag_kr']} {tag['tag_en']}")
            
            # 원재료 추가
            ingredient_texts = []
            if 'ingredients' in menu and menu['ingredients']:
                for ingredient in menu['ingredients']:
                    text += f" {ingredient['name_kr']} {ingredient['name_en']}"
                    ingredient_texts.append(f"{ingredient['name_kr']} {ingredient['name_en']}")
            
            # ChromaDB 메타데이터 적합화: 복잡한 구조(list, dict) 제거
            metadata = {
                "id": menu.get('id'),
                "store_id": menu.get('store_id'),
                "category_id": menu.get('category_id'),
                "name_kr": menu.get('name_kr'),
                "name_en": menu.get('name_en'),
                "description": menu.get('description', ""),
                "price": menu.get('price'),
                "image_url": menu.get('image_url', ""),
                "status": menu.get('status', ""),
                "tags_text": ", ".join(tag_texts) if tag_texts else "",
                "ingredients_text": ", ".join(ingredient_texts) if ingredient_texts else ""
            }
            
            documents.append(text)
            metadatas.append(metadata)
            ids.append(f"menu_{menu['id']}")
        
        # 컬렉션에 추가
        collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        
        print(f"{len(documents)}개의 메뉴 데이터가 벡터 DB에 추가되었습니다.")
        return len(documents)
    
    def create_option_collection(self, store_id: int = None):
        """MySQL에서 옵션 데이터를 가져와 벡터 DB 컬렉션 생성"""
        # 기존 컬렉션이 있으면 삭제
        try:
            self.client.delete_collection("option_collection")
        except:
            pass
        
        # 새 컬렉션 생성
        collection = self.client.create_collection("option_collection")
        
        # MySQL에서 옵션 데이터 로드
        option_data = self.mysql.get_options(store_id)
        
        if not option_data:
            print("옵션 데이터가 없습니다.")
            return 0
        
        # 각 옵션마다 문서 생성
        documents = []
        metadatas = []
        ids = []
        
        for idx, option in enumerate(option_data):
            # 옵션 이름 (한글 + 영어)
            text = f"{option['option_name_kr']} {option['option_name_en']}"
            
            # 옵션 상세 추가
            option_detail_texts = []
            if 'option_details' in option and option['option_details']:
                for detail in option['option_details']:
                    text += f" {detail['value']}"
                    option_detail_texts.append(detail['value'])
            
            # 메뉴 IDs 문자열로 변환
            menu_ids_str = ','.join(map(str, option.get('menu_ids', [])))
            
            # ChromaDB 메타데이터 적합화
            metadata = {
                "id": option.get('id'),
                "store_id": option.get('store_id'),
                "option_name_kr": option.get('option_name_kr'),
                "option_name_en": option.get('option_name_en'),
                "status": option.get('status', ""),
                "option_details_text": ", ".join(option_detail_texts),
                "menu_ids": menu_ids_str
            }
            
            documents.append(text)
            metadatas.append(metadata)
            ids.append(f"option_{option['id']}")
        
        # 컬렉션에 추가
        collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        
        print(f"{len(documents)}개의 옵션 데이터가 벡터 DB에 추가되었습니다.")
        return len(documents)
    
    def search_menu(self, query: str, store_id: int = None, top_k: int = 5):
        """메뉴 검색"""
        print(f"검색 쿼리: {query}, 매장 ID: {store_id}")
        
        # 1. 메뉴 데이터에서 정확한 이름 매칭 시도
        menu_data = self.mysql.get_menus(store_id)
        
        # 정확한 이름 매칭 검색
        exact_matches = []
        query_lower = query.lower().strip()
        query_no_space = query_lower.replace(" ", "")
        
        for menu in menu_data:
            menu_name_kr = menu.get('name_kr', '').lower()
            menu_name_kr_no_space = menu_name_kr.replace(" ", "")
            
            # 정확한 일치 또는 공백 제거 후 일치 확인
            if (query_lower == menu_name_kr or 
                query_no_space == menu_name_kr_no_space or
                query_lower in menu_name_kr or 
                menu_name_kr in query_lower):
                
                tags = []
                if 'tags' in menu and menu['tags']:
                    tags = menu['tags']
                
                exact_matches.append({
                    "id": menu.get('id'),
                    "store_id": menu.get('store_id'),
                    "name_kr": menu.get('name_kr'),
                    "name_en": menu.get('name_en'),
                    "price": menu.get('price'),
                    "description": menu.get('description', ""),
                    "tags": tags,
                    "score": 0.0  # 정확한 매칭은 최고 점수(0.0)로 설정
                })
        
        # 정확한 매칭 결과가 있으면 바로 반환
        if exact_matches:
            print(f"정확한 매칭 결과: {exact_matches}")
            return exact_matches
        
        # 2. 정확한 매칭이 없는 경우 벡터 검색 수행
        try:
            collection = self.client.get_collection("menu_collection")
            results = collection.query(
                query_texts=[query],
                n_results=top_k * 2  # 필터링 가능성을 고려해 더 많은 결과 요청
            )
        except Exception as e:
            print(f"벡터 검색 오류: {e}")
            return []
        
        # 벡터 검색 결과 처리
        vector_results = []
        
        if results.get("metadatas") and results["metadatas"][0]:
            for idx, metadata in enumerate(results["metadatas"][0]):
                # 메타데이터에서 store_id 가져오기 및 타입 변환
                meta_store_id = metadata.get("store_id")
                
                # 타입 변환
                if meta_store_id is not None:
                    try:
                        meta_store_id = int(meta_store_id)
                    except (ValueError, TypeError):
                        print(f"store_id 변환 오류: {meta_store_id}")
                
                # store_id가 None이거나 메타데이터의 store_id와 일치하는 경우만 필터링
                if store_id is None or meta_store_id == store_id:
                    # 태그 및 원재료 정보 추가
                    menu_id = metadata.get("id")
                    tags = []
                    
                    if metadata.get("tags_text"):
                        tag_pairs = metadata.get("tags_text").split(", ")
                        for pair in tag_pairs:
                            if " " in pair:
                                kr, en = pair.split(" ", 1)
                                tags.append({"tag_kr": kr, "tag_en": en})
                    
                    # 거리(유사도) 점수 가져오기
                    score = results["distances"][0][idx] if "distances" in results and len(results["distances"]) > 0 else 1.0
                    
                    vector_results.append({
                        "id": metadata.get("id"),
                        "store_id": meta_store_id,
                        "name_kr": metadata.get("name_kr"),
                        "name_en": metadata.get("name_en"),
                        "price": metadata.get("price"),
                        "description": metadata.get("description"),
                        "tags": tags,
                        "score": score
                    })
        
        # 점수로 정렬 (낮은 점수가 더 유사함)
        vector_results.sort(key=lambda x: x.get('score', 1.0))
        
        # 결과가 없거나 유사도가 너무 낮은 경우 빈 리스트 반환
        if not vector_results or vector_results[0].get('score', 1.0) > 0.5:
            return []
        
        return vector_results[:top_k]
    
    def get_menu_required_options(self, menu_id: int) -> List[Dict[str, Any]]:
        """메뉴의 필수 옵션 조회"""
        return self.mysql.get_required_options(menu_id)