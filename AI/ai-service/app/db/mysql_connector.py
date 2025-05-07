"""
mysql_commector.py
mysql 역결 설정 추가
"""

import pymysql
from pymysql import Error  # Error 클래스 임포트 수정
import os
from typing import List, Dict, Any, Optional

# MySQL 연결 DSN 설정
DSN = dict(
    host        = os.getenv("MYSQL_HOST", "host.docker.internal"),
    port        = int(os.getenv("MYSQL_PORT", 3307)),
    user        = os.getenv("MYSQL_USER", "root"),
    password    = os.getenv("MYSQL_PASS", ""),
    db          = os.getenv("MYSQL_DB", "mylio"),
    charset     = "utf8mb4",
    cursorclass = pymysql.cursors.DictCursor,
)

class MySQLConnector:
    def __init__(self, dsn=None):
        self.dsn = dsn or DSN
        self.connection = None
    
    def connect(self):
        """MySQL 데이터베이스에 연결"""
        try:
            self.connection = pymysql.connect(**self.dsn)
            print("MySQL 데이터베이스에 성공적으로 연결되었습니다.")
            return True
        except Error as e:
            print(f"MySQL 연결 오류: {e}")
            return False
    
    def disconnect(self):
        """MySQL 데이터베이스 연결 종료"""
        if self.connection:
            self.connection.close()
            print("MySQL 데이터베이스 연결이 종료되었습니다.")
    
    def execute_query(self, query: str, params: tuple = None) -> Optional[List[Dict[str, Any]]]:
        """쿼리 실행 및 결과 반환"""
        try:
            if not self.connection:
                self.connect()
            
            with self.connection.cursor() as cursor:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                
                result = cursor.fetchall()
                return result
        except Exception as e:
            print(f"쿼리 실행 오류: {e}")
            return None
    
    def get_menus(self, store_id: int = None) -> List[Dict[str, Any]]:
        """메뉴 데이터 조회"""
        query = """
        SELECT m.id, m.store_id, m.category_id, 
               m.name_kr, m.name_en, m.description, 
               m.price, m.image_url, m.status
        FROM menu m
        WHERE m.status = 'SELLING'
        """
        
        params = None
        if store_id is not None:
            query += " AND m.store_id = %s"
            params = (store_id,)
        
        menus = self.execute_query(query, params)
        if not menus:
            return []
        
        # 각 메뉴마다 태그 정보 추가
        for menu in menus:
            menu_id = menu['id']
            menu['tags'] = self.get_menu_tags(menu_id)
            menu['ingredients'] = self.get_menu_ingredients(menu_id)
        
        return menus
    
    def get_menu_tags(self, menu_id: int) -> List[Dict[str, str]]:
        """메뉴 태그 조회"""
        query = """
        SELECT tag_kr, tag_en
        FROM menu_tag_map
        WHERE menu_id = %s
        """
        
        tags = self.execute_query(query, (menu_id,))
        return tags if tags else []
    
    def get_menu_ingredients(self, menu_id: int) -> List[Dict[str, Any]]:
        """메뉴 원재료 조회"""
        query = """
        SELECT it.name_kr, it.name_en
        FROM menu_ingredient mi
        JOIN ingredient_template it ON mi.ingredient_id = it.id
        WHERE mi.menu_id = %s
        """
        
        ingredients = self.execute_query(query, (menu_id,))
        return ingredients if ingredients else []
    
    def get_options(self, store_id: int = None) -> List[Dict[str, Any]]:
        """옵션 데이터 조회"""
        query = """
        SELECT o.id, o.store_id, o.option_name_kr, o.option_name_en, o.status
        FROM options o
        WHERE o.status = 'REGISTERED'
        """
        
        params = None
        if store_id is not None:
            query += " AND o.store_id = %s"
            params = (store_id,)
        
        options = self.execute_query(query, params)
        if not options:
            return []
        
        # 각 옵션마다 옵션 상세 정보 추가
        for option in options:
            option_id = option['id']
            option['option_details'] = self.get_option_details(option_id)
            option['menu_ids'] = self.get_option_menus(option_id)
        
        return options
    
    def get_option_details(self, option_id: int) -> List[Dict[str, Any]]:
        """옵션 상세 정보 조회"""
        query = """
        SELECT id, value, additional_price
        FROM option_detail
        WHERE option_id = %s AND status = 'REGISTERED'
        """
        
        option_details = self.execute_query(query, (option_id,))
        return option_details if option_details else []
    
    def get_option_menus(self, option_id: int) -> List[int]:
        """해당 옵션을 사용하는 메뉴 ID 목록 조회"""
        query = """
        SELECT DISTINCT menu_id
        FROM menu_option_map
        WHERE option_id = %s
        """
        
        menu_ids_dicts = self.execute_query(query, (option_id,))
        if not menu_ids_dicts:
            return []
        
        return [item['menu_id'] for item in menu_ids_dicts]
    
    def get_required_options(self, menu_id: int) -> List[Dict[str, Any]]:
        """메뉴의 필수 옵션 조회"""
        query = """
        SELECT mom.option_id, o.option_name_kr, o.option_name_en
        FROM menu_option_map mom
        JOIN options o ON mom.option_id = o.id
        WHERE mom.menu_id = %s AND mom.is_required = b'1'
        GROUP BY mom.option_id
        """
        
        required_options = self.execute_query(query, (menu_id,))
        if not required_options:
            return []
        
        # 각 필수 옵션마다 옵션 상세 정보 추가
        for option in required_options:
            option_id = option['option_id']
            option['option_details'] = self.get_option_details(option_id)
        
        return required_options
    
    # def get_menu_options(self, menu_id: int, store_id: int) -> List[Dict[str, Any]]:
    #     """메뉴의 모든 옵션 조회"""
    #     # 메뉴-옵션 매핑 조회
    #     query = """
    #     SELECT mom.option_id, mom.is_required, o.option_name_kr, o.option_name_en
    #     FROM menu_option_map mom
    #     JOIN options o ON mom.option_id = o.id
    #     WHERE mom.menu_id = %s AND o.store_id = %s
    #     """
        
    #     option_maps = self.execute_query(query, (menu_id, store_id))
    #     if not option_maps:
    #         return []
        
    #     # 각 옵션의 상세 정보 조회
    #     result = []
    #     for option_map in option_maps:
    #         option_id = option_map["option_id"]
            
    #         # 옵션 상세 정보 조회
    #         option_details = self.get_option_details(option_id)
            
    #         result.append({
    #             "option_id": option_id,
    #             "option_name": option_map["option_name_kr"],
    #             "option_name_en": option_map["option_name_en"],
    #             "required": option_map["is_required"] == b'\x01',  # MySQL BIT -> Python Boolean
    #             "is_selected": False,
    #             "option_details": option_details
    #         })
        
    #     return result
    
    def get_menu_options(self, menu_id: int, store_id: int) -> List[Dict[str, Any]]:
        """메뉴의 모든 옵션 조회"""
        # 메뉴-옵션 매핑 조회 (메뉴별 옵션 필터링 추가)
        query = """
        SELECT mom.option_id, mom.is_required, o.option_name_kr, o.option_name_en
        FROM menu_option_map mom
        JOIN options o ON mom.option_id = o.id
        WHERE mom.menu_id = %s AND o.store_id = %s
        GROUP BY mom.option_id, mom.is_required, o.option_name_kr, o.option_name_en
        """
        
        option_maps = self.execute_query(query, (menu_id, store_id))
        if not option_maps:
            # 옵션이 없으면 기본 옵션 추가
            return self._get_default_options(store_id)
        
        # 각 옵션의 상세 정보 조회
        result = []
        for option_map in option_maps:
            option_id = option_map["option_id"]
            
            # 옵션 상세 정보 조회 (option_detail)
            option_details = self.get_option_details(option_id)
            
            result.append({
                "option_id": option_id,
                "option_name": option_map["option_name_kr"],
                "option_name_en": option_map["option_name_en"],
                "required": option_map["is_required"] == b'\x01',  # MySQL BIT -> Python Boolean
                "is_selected": False,
                "selected_id" : None,
                "option_details": option_details
            })
        
        return result

    def _get_default_options(self, store_id: int) -> List[Dict[str, Any]]:
        """기본 옵션 생성 (옵션이 없는 경우 사용)"""
        # 여기서는 사이즈와 온도 옵션만 기본으로 제공
        return [
            {
                "option_id": 100,  # 임의의 ID
                "option_name": "사이즈",
                "option_name_en": "Size",
                "required": True,
                "is_selected": False,
                "option_details": [
                    {"id": 998, "value": "S", "additional_price": 0},
                    {"id": 999, "value": "M", "additional_price": 500},
                    {"id": 1000, "value": "L", "additional_price": 1000}
                ]
            },
            {
                "option_id": 101,  # 임의의 ID
                "option_name": "온도",
                "option_name_en": "Temperature",
                "required": True,
                "is_selected": False,
                "option_details": [
                    {"id": 1001, "value": "HOT", "additional_price": 0},
                    {"id": 1002, "value": "ICE", "additional_price": 0}
                ]
            }
        ]