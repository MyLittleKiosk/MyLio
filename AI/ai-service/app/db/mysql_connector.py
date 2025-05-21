# app/db/mysql_connector.py
import pymysql
from pymysql.cursors import DictCursor
from typing import List, Dict, Any, Optional, Tuple, Union

class MySQLConnector:
    def __init__(self, host: str, port: int, user: str, password: str, database: str):
        """MySQL 연결 클래스 초기화"""
        self.config = {
            "host": host,
            "port": port,
            "user": user,
            "password": password,
            "database": database,
            "charset": "utf8mb4",
            "cursorclass": DictCursor
        }
        self.connection = None
        self.connect()
    
    def connect(self) -> bool:
        """데이터베이스 연결"""
        try:
            self.connection = pymysql.connect(**self.config)
            return True
        except Exception as e:
            # print(f"MySQL 연결 오류: {e}")
            return False
    
    def disconnect(self) -> None:
        """데이터베이스 연결 종료"""
        if self.connection:
            self.connection.close()
            self.connection = None
    
    def execute_query(self, query: str, params: Union[Tuple, List, Dict] = None) -> Optional[List[Dict[str, Any]]]:
        """쿼리 실행 및 결과 반환"""
        try:
            if not self.connection or not self.connection.open:
                self.connect()
            
            with self.connection.cursor() as cursor:
                cursor.execute(query, params)
                result = cursor.fetchall()
                return result
        except Exception as e:
            # print(f"쿼리 실행 오류: {e}")
            # print(f"실행 쿼리: {query}")
            # print(f"파라미터: {params}")
            # 연결이 끊어진 경우 재연결 시도
            if "MySQL server has gone away" in str(e):
                self.connect()
            return None
    
    def execute_update(self, query: str, params: Union[Tuple, List, Dict] = None) -> Optional[int]:
        """데이터 수정 쿼리 실행 및 영향받은 행 수 반환"""
        try:
            if not self.connection or not self.connection.open:
                self.connect()
            
            with self.connection.cursor() as cursor:
                affected_rows = cursor.execute(query, params)
                self.connection.commit()
                return affected_rows
        except Exception as e:
            # print(f"업데이트 쿼리 실행 오류: {e}")
            # print(f"실행 쿼리: {query}")
            # print(f"파라미터: {params}")
            # 연결이 끊어진 경우 재연결 시도
            if "MySQL server has gone away" in str(e):
                self.connect()
            return None