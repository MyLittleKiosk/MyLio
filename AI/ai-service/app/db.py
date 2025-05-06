# app/db.py
import os, pymysql, functools
from typing import Dict, List

# ──────────────── MySQL DSN ────────────────
DSN = dict(
    host        = os.getenv("MYSQL_HOST", "host.docker.internal"),
    port        = int(os.getenv("MYSQL_PORT", 3307)),
    user        = os.getenv("MYSQL_USER", "root"),
    password    = os.getenv("MYSQL_PASS", ""),
    db          = os.getenv("MYSQL_DB", "mylio"),
    charset     = "utf8mb4",
    cursorclass = pymysql.cursors.DictCursor,
)

def _query(sql: str, *args):
    with pymysql.connect(**DSN) as conn, conn.cursor() as cur:
        cur.execute(sql, args)
        return cur.fetchall()
    
# ──────────────── value 표준화 매핑 ────────────────
VAL_MAP = {
    # 온도
    "HOT": "HOT", "따뜻": "HOT", "뜨거운": "HOT",
    "ICE": "ICE", "ICED": "ICE", "차가워": "ICE", "차가운": "ICE",
    # 사이즈
    "S": "S", "SMALL": "S", "작은": "S",
    "M": "M", "MEDIUM": "M", "중간": "M",
    "L": "L", "LARGE": "L", "큰": "L",
}

# ──────────────── 캐시 + 메타 취합 ────────────────
@functools.lru_cache(maxsize=32)
def store_meta(store_id: int) -> Dict:
    """
    매장별 메뉴·옵션·재료·영양·태그 전부 일괄 로드해서 메모리에 캐싱
    """
    # 1. 메뉴 정보
    menu_rows = _query(
        """SELECT id, name_kr, name_en, price
           FROM menu
           WHERE store_id = %s AND status = 'SELLING'""",
        store_id,
    )
    menus = {r["id"]: r for r in menu_rows}
    
    # 2. 옵션과 옵션 상세 정보 함께 조회
    opt_rows = _query(
        """SELECT o.id AS option_id,
                  o.option_name_kr,
                  o.option_name_en,
                  d.id AS option_detail_id,
                  d.value AS option_value,
                  d.additional_price
           FROM options o
           JOIN option_detail d ON d.option_id = o.id
           WHERE o.store_id = %s
           AND o.status = 'REGISTERED'
           AND d.status = 'REGISTERED'""",
        store_id,
    )
    
    options = {}
    option_mappings = {}
    option_details = {}
    
    # 옵션 기본 정보 설정 및 옵션 상세 정보 수집
    for r in opt_rows:
        opt_id = r["option_id"]
        option_detail_id = r["option_detail_id"]
        option_value = r["option_value"]
        
        # 옵션 정보 설정
        if opt_id not in options:
            options[opt_id] = {
                "name_kr": r["option_name_kr"],
                "name_en": r["option_name_en"],
                "values": [],
                "details": []  # 상세 정보 추가
            }
        
        if option_value not in options[opt_id]["values"]:
            options[opt_id]["values"].append(option_value)
        
        # 옵션 상세 정보 추가
        option_detail = {
            "id": option_detail_id,
            "value": option_value,
            "additional_price": r["additional_price"],
            "display_kr": option_value,  # 기본값
            "display_en": option_value   # 기본값
        }
        options[opt_id]["details"].append(option_detail)
        
        # 매핑 정보 저장 (LLM이 이해하는 값으로 변환)
        if r["option_name_kr"] not in option_mappings:
            option_mappings[r["option_name_kr"]] = []
        
        # 다양한 표현 매핑
        if option_value in ["S", "SMALL", "작은"]:
            mappings = ["작은", "작은거", "스몰", "S", "SMALL"]
        elif option_value in ["M", "MEDIUM", "중간"]:
            mappings = ["중간", "미디움", "M", "MEDIUM"]
        elif option_value in ["L", "LARGE", "큰"]:
            mappings = ["큰", "큰거", "라지", "L", "LARGE"]
        elif option_value in ["Tall", "Grande", "Venti"]:
            mappings = [option_value, option_value.lower()]
        elif option_value == "HOT":
            mappings = ["HOT", "핫", "따뜻한", "뜨거운"]
        elif option_value == "ICE":
            mappings = ["ICE", "아이스", "차가운", "아이스", "ICED"]
        else:
            mappings = [option_value]
        
        for mapping in mappings:
            option_mappings[r["option_name_kr"]].append({
                "original": option_value,
                "mapped": mapping,
                "id": option_detail_id,
                "additional_price": r["additional_price"]
            })
    
    # 3. 필수 옵션 매핑
    required_opt_rows = _query(
        """SELECT m.id AS menu_id,
                  o.id AS option_id,
                  o.option_name_kr,
                  o.option_name_en
           FROM menu_option_map mop
           JOIN menu m ON m.id = mop.menu_id  
           JOIN options o ON o.id = mop.option_id
           WHERE m.store_id = %s
           AND mop.is_required = TRUE""",
        store_id,
    )
    
    required_options = {}
    seen_options = set()  # 중복 체크용 집합
    for r in required_opt_rows:
        menu_id = r["menu_id"]
        option_id = r["option_id"]

        # 중복 확인 - (메뉴ID, 옵션ID) 조합이 이미 처리되었는지 확인
        option_key = (menu_id, option_id)
        if option_key in seen_options:
            continue
        
        seen_options.add(option_key)

        if menu_id not in required_options:
            required_options[menu_id] = []
        required_options[menu_id].append({
            "id": r["option_id"],
            "name_kr": r["option_name_kr"],
            "name_en": r["option_name_en"]
        })

    # 4) 영양소 ---------------------------------------------------------------
    nut_rows = _query(
        """
        SELECT  nv.menu_id,
                nt.name_kr   AS nut_name,
                nt.name_en   AS nut_name_en,
                nv.value
          FROM  nutrition_value     nv
          JOIN  nutrition_template  nt ON nt.id = nv.nutrition_id
         WHERE  nv.store_id = %s
           AND  nv.status   != 'DELETED'
        """,
        store_id,
    )
    nutrition = {}
    nutrition_en = {} 
    for r in nut_rows:
        menu_id = r["menu_id"]
        nutrition.setdefault(menu_id, {})[r["nut_name"]] = float(r["value"])
        nutrition_en.setdefault(menu_id, {})[r["nut_name_en"]] = float(r["value"])

    # 5) 재료 ------------------------------------------------------------------
    ing_rows = _query(
        """
        SELECT  mi.menu_id,
                it.name_kr   AS ing_kr,
                it.name_en   AS ing_en
          FROM  menu_ingredient     mi
          JOIN  ingredient_template it ON it.id = mi.ingredient_id
         WHERE  mi.store_id = %s
        """,
        store_id,
    )
    ingredients_kr = {}
    ingredients_en = {}
    for r in ing_rows:
        menu_id = r["menu_id"]
        ingredients_kr.setdefault(menu_id, []).append(r["ing_kr"])
        ingredients_en.setdefault(menu_id, []).append(r["ing_en"])

    # 6) 태그 ------------------------------------------------------------------
    tag_rows = _query(
        """
        SELECT  menu_id,
                tag_kr,
                tag_en
          FROM  menu_tag_map
         WHERE  store_id = %s
        """,
        store_id,
    )
    tags_kr = {}
    tags_en = {}
    for r in tag_rows:
        tags_kr.setdefault(r["menu_id"], []).append(r["tag_kr"])
        tags_en.setdefault(r["menu_id"], []).append(r["tag_en"])

    # 정렬‧반환 ---------------------------------------------------------------
    return {
        "menus": menus,
        "options": options,  
        "option_mappings": option_mappings,  
        "required_options": required_options,  
        "nutrition": nutrition,
        "nutrition_en": nutrition_en,
        "ingredients": ingredients_kr,
        "ingredients_en": ingredients_en,
        "tags": tags_kr,
        "tags_en": tags_en,
        "size_type": detect_size_type(options)  
    }

def detect_size_type(options: Dict) -> str:
    """매장의 사이즈 표현 방식 감지"""
    for option in options.values():
        if "사이즈" in option["name_kr"] or "Size" in option["name_en"]:
            values = option["values"]
            if "Tall" in values or "Grande" in values or "Venti" in values:
                return "STARBUCKS"
            elif "S" in values and "M" in values and "L" in values:
                return "SML"
            else:
                return "CUSTOM"
    return "NONE"