# app/services/menu_service.py
import copy
from typing import Dict, List, Any, Optional
from app.db.mysql_connector import MySQLConnector

class MenuService:
    def __init__(self, db: MySQLConnector):
        self.db = db
        self.menu_cache = {}  # 메뉴 캐시 (store_id -> menus)

    def get_all_store_ids(self) -> List[int]:
        query = "SELECT DISTINCT id FROM store"
        rows = self.db.execute_query(query)
        return [row["id"] for row in rows]

    
    def get_store_menus(self, store_id: int) -> Dict[int, Dict[str, Any]]:
        """스토어 ID에 해당하는 메뉴 정보 조회 (캐싱 적용)"""
        # 캐시된 결과가 있으면 반환
        if store_id in self.menu_cache:
            return self.menu_cache[store_id]
        
        # 1. 메뉴 기본 정보 조회
        menus = self._load_menus(store_id)
        
        # 2. 메뉴 옵션 정보 조회
        self._load_menu_options(menus, store_id)
        
        # 3. 메뉴 태그 정보 조회
        self._load_menu_tags(menus, store_id)
        
        # 4. 메뉴 원재료 정보 조회
        self._load_menu_ingredients(menus, store_id)
        
        # 결과 캐싱
        self.menu_cache[store_id] = menus
        
        return menus
    
    def _load_menus(self, store_id: int) -> Dict[int, Dict[str, Any]]:
        """메뉴 기본 정보 조회"""
        query = """
        SELECT id, name_kr, name_en, description, price, image_url, status, category_id
        FROM menu 
        WHERE store_id = %s AND status = 'SELLING'
        """
        
        menu_rows = self.db.execute_query(query, (store_id,))
        
        if not menu_rows:
            return {}
        
        menus = {}
        for menu in menu_rows:
            menu_id = menu["id"]
            menus[menu_id] = {
                "id": menu_id,
                "name_kr": menu["name_kr"],
                "name_en": menu.get("name_en", ""),
                "description": menu.get("description", ""),
                "price": menu["price"],
                "image_url": menu.get("image_url", ""),
                "status": menu["status"],
                "category_id": menu["category_id"],
                "options": [],
                "tags": [],
                "ingredients": []
            }
        
        return menus
    
    def _load_menu_options(self, menus: Dict[int, Dict[str, Any]], store_id: int) -> None:
        """메뉴 옵션 정보 조회"""
        if not menus:
            return
        
        print(f"메뉴 옵션 로드 시작: store_id={store_id}")
        
        # 메뉴와 옵션 매핑 정보 조회 - DISTINCT 추가
        query = """
        SELECT DISTINCT mom.menu_id, mom.option_id, mom.is_required,
            o.option_name_kr, o.option_name_en
        FROM menu_option_map mom
        JOIN options o ON mom.option_id = o.id
        WHERE o.store_id = %s
        """
        
        option_maps = self.db.execute_query(query, (store_id,))
        
        if not option_maps:
            return
        
        print(f"조회된 옵션 매핑 수: {len(option_maps)}")
        
        # 각 메뉴별로 추가된 옵션 ID 추적
        added_options = {menu_id: set() for menu_id in menus.keys()}
        
        # 옵션별로 옵션 상세 정보 추가
        for option_map in option_maps:
            menu_id = option_map["menu_id"]
            option_id = option_map["option_id"]
            
            if menu_id not in menus:
                continue
            
            # 이미 추가된 옵션인지 확인
            if menu_id in added_options and option_id in added_options[menu_id]:
                print(f"중복 옵션 스킵: menu_id={menu_id}, option_id={option_id}")
                continue
            
            # 옵션 추가 기록
            added_options[menu_id].add(option_id)
            
            # 옵션 상세 정보 조회
            detail_query = """
            SELECT id, value, additional_price
            FROM option_detail
            WHERE option_id = %s AND status = 'REGISTERED'
            """
            
            option_details = self.db.execute_query(detail_query, (option_id,))
            
            # 옵션 정보 구조화
            option_info = {
                "option_id": option_id,
                "option_name": option_map["option_name_kr"],
                "option_name_en": option_map["option_name_en"],
                "required": option_map["is_required"] == b'\x01',  # MySQL BIT -> Python Boolean
                "is_selected": False,
                "selected_id": None,
                "option_details": option_details or []
            }
            
            # 메뉴에 옵션 추가
            menus[menu_id]["options"].append(option_info)
    
    def _load_menu_tags(self, menus: Dict[int, Dict[str, Any]], store_id: int) -> None:
        """메뉴 태그 정보 조회"""
        if not menus:
            return
        
        query = """
        SELECT menu_id, tag_kr, tag_en
        FROM menu_tag_map
        WHERE store_id = %s
        """
        
        tag_rows = self.db.execute_query(query, (store_id,))
        
        if not tag_rows:
            return
        
        for row in tag_rows:
            menu_id = row["menu_id"]
            if menu_id in menus:
                menus[menu_id]["tags"].append({
                    "tag_kr": row["tag_kr"],
                    "tag_en": row["tag_en"]
                })
    
    def _load_menu_ingredients(self, menus: Dict[int, Dict[str, Any]], store_id: int) -> None:
        """메뉴 원재료 정보 조회"""
        if not menus:
            return
        
        # 메뉴 ID 목록
        menu_ids = list(menus.keys())
        if not menu_ids:
            return
        
        placeholders = ", ".join(["%s"] * len(menu_ids))
        
        query = f"""
        SELECT mi.menu_id, it.name_kr, it.name_en
        FROM menu_ingredient mi
        JOIN ingredient_template it ON mi.ingredient_id = it.id
        JOIN menu m ON mi.menu_id = m.id
        WHERE mi.menu_id IN ({placeholders}) AND m.store_id = %s
        """
        
        params = menu_ids + [store_id]
        ingredient_rows = self.db.execute_query(query, params)
        
        if not ingredient_rows:
            return
        
        for row in ingredient_rows:
            menu_id = row["menu_id"]
            if menu_id in menus:
                menus[menu_id]["ingredients"].append({
                    "name_kr": row["name_kr"],
                    "name_en": row["name_en"]
                })
    
    def find_menu_by_name(self, menu_name: str, store_id: int) -> Optional[Dict[str, Any]]:
        if not menu_name:
            return None
        
        """메뉴 이름으로 메뉴 검색"""
        # 1. 스토어 메뉴 데이터 가져오기
        menus = self.get_store_menus(store_id)
        
        # 2. 정규화된 메뉴명
        normalized_name = menu_name.lower().strip()
        
        # 3. 정확한 이름 매칭
        for _, menu in menus.items():
            if menu["name_kr"].lower() == normalized_name or (menu["name_en"] and menu["name_en"].lower() == normalized_name):
                return copy.deepcopy(menu)
        
        # 4. 부분 매칭
        for _, menu in menus.items():
            if normalized_name in menu["name_kr"].lower() or (menu["name_en"] and normalized_name in menu["name_en"].lower()):
                return copy.deepcopy(menu)
        
        # 5. 특수 별칭 매핑
        aliases = self._get_menu_aliases()
        if normalized_name in aliases:
            alias_pattern = aliases[normalized_name]
            for _, menu in menus.items():
                if alias_pattern.lower() in menu["name_kr"].lower():
                    return copy.deepcopy(menu)
        
        return None
    
    def _get_menu_aliases(self) -> Dict[str, str]:
        """자주 사용되는 메뉴 별칭 사전"""
        return {
            "아아": "아메리카노",
            "아이스아메리카노": "아메리카노",
            "따아": "아메리카노",
            "바라": "바닐라 라떼",
            "바닐라라떼": "바닐라 라떼",
            "바닐라라테": "바닐라 라떼",
            "카라": "카페 라떼",
            "카페라테": "카페 라떼",
            "라떼": "카페 라떼",
            "라테": "카페 라떼"
        }
    
    def get_category_by_id(self, category_id: int) -> Optional[Dict[str, Any]]:
        """카테고리 ID로 카테고리 정보 조회"""
        # 캐시에서 먼저 확인
        if hasattr(self, '_categories_cache') and self._categories_cache.get(category_id):
            return self._categories_cache.get(category_id)
        
        # 캐시가 없으면 카테고리 로드
        if not hasattr(self, '_categories_cache'):
            self.load_all_categories()
            # 로드 후 다시 확인
            if category_id in self._categories_cache:
                return self._categories_cache[category_id]
        
        # 캐시에 없으면 직접 DB에서 조회
        query = """
            SELECT id, name_kr, name_en 
            FROM category 
            WHERE id = %s
        """
        
        result = self.db.execute_query(query, (category_id,))
        
        if not result or len(result) == 0:
            return None
        
        # 결과 캐싱
        if not hasattr(self, '_categories_cache'):
            self._categories_cache = {}
        
        self._categories_cache[category_id] = result[0]
        
        return result[0]

    def load_all_categories(self) -> Dict[int, Dict[str, Any]]:
        """모든 카테고리 정보를 로드하고 캐싱"""
        # 이미 캐시가 있으면 반환
        if hasattr(self, '_categories_cache'):
            return self._categories_cache
        
        # DB에서 모든 카테고리 조회
        query = """
            SELECT id, name_kr, name_en 
            FROM category
        """
        
        result = self.db.execute_query(query)
        
        # 캐시 초기화
        self._categories_cache = {}
        
        if result:
            for category in result:
                self._categories_cache[category['id']] = category
        
        return self._categories_cache

    def get_store_categories(self, store_id: int) -> List[Dict[str, Any]]:
        """매장에서 사용하는 카테고리 목록 조회"""
        # 메뉴에서 사용되는 카테고리 ID 조회
        query = """
            SELECT DISTINCT category_id 
            FROM menu 
            WHERE store_id = %s AND status = 'SELLING'
        """
        
        result = self.db.execute_query(query, (store_id,))
        
        if not result:
            return []
        
        # 카테고리 정보 로드
        categories = []
        for item in result:
            category_id = item['category_id']
            category = self.get_category_by_id(category_id)
            if category:
                categories.append(category)
        
        return categories
    