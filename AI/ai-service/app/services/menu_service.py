# app/services/menu_service.py
import copy
from typing import Dict, List, Any, Optional
from app.db.mysql_connector import MySQLConnector
from app.models.schemas import ResponseStatus

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
    
        # 5. 메뉴 영양 성분 정보 조회
        self._load_menu_nutrition(menus, store_id)
        
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
    
    def _load_menu_nutrition(self, menus: Dict[int, Dict[str, Any]], store_id: int) -> None:
        """메뉴 영양 성분 정보 조회"""
        if not menus:
            return
        
        menu_ids = list(menus.keys())
        if not menu_ids:
            return
        
        placeholders = ", ".join(["%s"] * len(menu_ids))
        
        # 테이블 구조에 맞게 쿼리 수정
        query = f"""
        SELECT menu_id, nutrition_id, value, status 
        FROM nutrition_value 
        WHERE menu_id IN ({placeholders})
        """
        
        params = menu_ids
        nutrition_rows = self.db.execute_query(query, params)
        
        if not nutrition_rows:
            return
        
        # 영양 성분 템플릿 정보 가져오기 (이름과 단위)
        nutrition_template_query = """
        SELECT id, name_kr, name_en, unit_type 
        FROM nutrition_template
        """
        
        nutrition_templates = self.db.execute_query(nutrition_template_query)
        if not nutrition_templates:
            return
        
        # 영양 성분 템플릿을 ID 기준으로 매핑
        nutrition_template_map = {template["id"]: template for template in nutrition_templates}
        
        # 각 메뉴별로 영양 성분 정보 리스트 생성 및 초기화
        for menu_id in menus:
            # 이미 dict으로 초기화되어 있어도 리스트로 덮어쓰기
            menus[menu_id]["nutrition"] = []
        
        # 각 메뉴별로 영양 성분 정보 구성
        for row in nutrition_rows:
            menu_id = row["menu_id"]
            if menu_id in menus:
                # 영양 성분 ID를 이용해 템플릿 정보 가져오기
                nutrition_id = row["nutrition_id"]
                template = nutrition_template_map.get(nutrition_id)
                
                if template:
                    name = template["name_kr"]
                    name_en = template.get("name_en", "")
                    unit = template["unit_type"]
                    value = row["value"]
                    
                    # 영양 성분 정보를 객체로 구성하여 리스트에 추가
                    nutrition_item = {
                        "id": nutrition_id,
                        "name": name,
                        "name_en": name_en,
                        "value": value,
                        "unit": unit,
                        "formatted": f"{value}{unit}"  # 포맷팅된 값
                    }
                    
                    menus[menu_id]["nutrition"].append(nutrition_item)

    def find_menu_by_id(self, menu_id: int, store_id: int) -> Optional[Dict[str, Any]]:
        """메뉴 ID로 메뉴 검색"""
        if not menu_id:
            return None
        
        # 1. 스토어 메뉴 데이터 가져오기
        menus = self.get_store_menus(store_id)
        
        # 2. ID로 메뉴 찾기
        if menu_id in menus:
            return copy.deepcopy(menus[menu_id])
        
        return None

    def find_similar_menu(self, menu_name: str, store_id: int) -> Optional[Dict[str, Any]]:
        """유사한 이름의 메뉴 찾기"""
        # 메뉴 목록 가져오기
        store_menus = self.get_store_menus(store_id)
        
        # 별칭 사전 가져오기
        aliases = self._get_menu_aliases()
        
        # 별칭으로 먼저 검색
        for alias, real_name in aliases.items():
            if menu_name.lower() in alias.lower() or alias.lower() in menu_name.lower():
                # 실제 메뉴 이름으로 검색
                for menu_id, menu in store_menus.items():
                    if real_name.lower() == menu.get("name_kr", "").lower():
                        return menu
        
        # 유사도 기반 검색 (간단한 방식)
        best_match = None
        highest_similarity = 0
        
        for menu_id, menu in store_menus.items():
            # 메뉴 이름 유사도 계산 (포함 관계 확인)
            menu_kr = menu.get("name_kr", "").lower()
            if menu_kr in menu_name.lower() or menu_name.lower() in menu_kr:
                similarity = len(set(menu_kr) & set(menu_name.lower())) / max(len(menu_kr), len(menu_name.lower()))
                if similarity > highest_similarity:
                    highest_similarity = similarity
                    best_match = menu
        
        # 유사도가 일정 수준(30%) 이상인 경우에만 반환
        if highest_similarity >= 0.3:
            return best_match
        
        return None


    def get_option_detail(
            self, option_name: str, option_value: str, store_id: int
    ) -> tuple[int | None, int]:
        """
        옵션명·값으로 option_detail.id와 additional_price를 반환.
        못 찾으면 (None, 0) 리턴
        """
        menus = self.get_store_menus(store_id)
        for menu in menus.values():
            for opt in menu["options"]:
                if opt["option_name"].lower() == option_name.lower():
                    for detail in opt["option_details"]:
                        if detail["value"].upper() == option_value.upper():
                            return detail["id"], detail["additional_price"]
        return None, 0

    def get_menu_price(self, menu_id: int, store_id: int) -> int:
        """
        메뉴 ID로 기본 가격을 조회합니다.
        """
        menu = self.find_menu_by_id(menu_id, store_id)
        # 메뉴가 없거나 price 필드가 없으면 0 리턴
        return menu.get("price", 0) if menu else 0