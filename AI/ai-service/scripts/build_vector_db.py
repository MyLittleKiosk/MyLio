# scripts/build_vector_db.py
import os
import time
import sys
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# 경로 추가 (app 모듈 import 위해)
sys.path.append('.')

# 모듈 import
from app.services.menu_service import MenuService
from app.services.vector_db_service import VectorDBService

def main():
    """메뉴 데이터로 벡터 DB 구축"""
    print("벡터 DB 구축 시작")
    start_time = time.time()
    
    # 메뉴 서비스 초기화
    mysql_host = os.getenv("MYSQL_HOST", "localhost")
    mysql_port = int(os.getenv("MYSQL_PORT", "3307"))
    mysql_user = os.getenv("MYSQL_USER", "root")
    mysql_pass = os.getenv("MYSQL_PASS", "root")
    mysql_db = os.getenv("MYSQL_DB", "mylio")
    
    menu_service = MenuService(
        host=mysql_host, 
        port=mysql_port,
        user=mysql_user,
        password=mysql_pass,
        database=mysql_db
    )
    
    # 벡터 DB 서비스 초기화
    vector_db_service = VectorDBService.get_instance()
    
    # 매장 ID 목록 (필요에 따라 수정)
    store_ids = [1]  # 예: 여러 매장 [1, 2, 3]
    
    # 벡터 DB 구축
    menu_count = vector_db_service.initialize_from_menus(menu_service, store_ids)
    
    end_time = time.time()
    print(f"벡터 DB 구축 완료: {menu_count}개 메뉴, 소요 시간: {end_time - start_time:.2f}초")

if __name__ == "__main__":
    main()