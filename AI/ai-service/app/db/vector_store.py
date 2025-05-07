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
        
        # 먼저 정확한 메뉴명 매칭 시도 (대소문자 무시)
        # MySQL에서 메뉴 데이터 로드
        menu_data = self.mysql.get_menus(store_id)
        
        # 정확한 이름 매칭 검색
        exact_matches = []
        query_lower = query.lower()
        
        print(f"정확한 매칭 검색 시작 - 쿼리: {query_lower}")
        
        for menu in menu_data:
            menu_name_kr = menu.get('name_kr', '').lower()
            menu_name_en = menu.get('name_en', '').lower()
            
            # 디버깅을 위한 출력
            print(f"메뉴 비교: '{menu_name_kr}'/'{menu_name_en}' vs '{query_lower}'")
            
            if query_lower in menu_name_kr or query_lower in menu_name_en:
                tags = []
                if 'tags' in menu and menu['tags']:
                    tags = menu['tags']
                
                print(f"매칭된 메뉴 발견: {menu['name_kr']}")
                
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
            print(f"정확한 매칭 결과 수: {len(exact_matches)}")
            # store_id 필터링 (이미 MySQL 쿼리에서 필터링되었을 수 있음)
            if store_id is not None:
                filtered_matches = []
                for menu in exact_matches:
                    # 메뉴에 store_id가 있고 일치하는 경우만 포함
                    menu_store_id = menu.get('store_id')
                    print(f"메뉴 {menu.get('name_kr')}의 store_id: {menu_store_id}, 비교할 store_id: {store_id}")
            
                    if menu_store_id is not None:
                        if isinstance(menu_store_id, str):
                            menu_store_id = int(menu_store_id)
                        
                        if menu_store_id == store_id:
                            filtered_matches.append(menu)
                
                if filtered_matches:
                    print(f"store_id 필터링 후 결과 수: {len(filtered_matches)}")
                    return filtered_matches[:top_k]
                else:
                    print(f"store_id({store_id})와 일치하는 메뉴가 없습니다. 벡터 검색으로 전환")
                
            else:
                # store_id가 None이면 모든 결과 반환
                return exact_matches[:top_k]
            
        print("정확한 매칭 결과 없음, 벡터 검색 시작")
        
        # 정확한 매칭 결과가 없거나 store_id 필터링 후 결과가 없으면 벡터 검색 수행
        try:
            collection = self.client.get_collection("menu_collection")
            results = collection.query(
                query_texts=[query],
                n_results=top_k
            )
        except Exception as e:
            print(f"벡터 검색 오류: {e}")
            return []
        
        # 결과가 비어있는 경우 빈 배열 반환
        if not results.get("metadatas") or not results["metadatas"][0]:
            print("벡터 검색 결과가 비어있습니다.")
            return []
        
        print(f"벡터 검색 결과 수: {len(results['metadatas'][0])}")
        
        # 결과 필터링 (store_id가 지정된 경우)
        filtered_results = []
        for idx, metadata in enumerate(results["metadatas"][0]):
            # 메타데이터에서 store_id 가져오기 및 타입 변환
            meta_store_id = metadata.get("store_id")
            print(f"메타데이터: {metadata}")
            
            # 타입 변환 (문자열/정수 상관없이 비교 가능하도록)
            if meta_store_id is not None:
                try:
                    meta_store_id = int(meta_store_id)
                except (ValueError, TypeError):
                    print(f"store_id 변환 오류: {meta_store_id}")
            
            # store_id가 None이거나 메타데이터의 store_id와 일치하는 경우만 필터링
            if store_id is None or meta_store_id == store_id:
                # 태그 및 원재료 정보가 필요하면 원본 메뉴 데이터 조회
                menu_id = metadata.get("id")
                tags = []
                
                if metadata.get("tags_text"):
                    tag_pairs = metadata.get("tags_text").split(", ")
                    for pair in tag_pairs:
                        if " " in pair:
                            kr, en = pair.split(" ", 1)
                            tags.append({"tag_kr": kr, "tag_en": en})
                
                filtered_result = {
                    "id": metadata.get("id"),
                    "name_kr": metadata.get("name_kr"),
                    "name_en": metadata.get("name_en"),
                    "price": metadata.get("price"),
                    "description": metadata.get("description"),
                    "tags": tags
                }
                
                if "distances" in results and len(results["distances"]) > 0:
                    filtered_result["score"] = results["distances"][0][idx]
                
                filtered_results.append(filtered_result)
        
        print(f"필터링된 결과 수: {len(filtered_results)}")
        return filtered_results
    
    def get_menu_required_options(self, menu_id: int) -> List[Dict[str, Any]]:
        """메뉴의 필수 옵션 조회"""
        return self.mysql.get_required_options(menu_id)