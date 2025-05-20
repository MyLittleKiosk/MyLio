# utils/sanitize.py
"""
LLM이 내놓은 menu_id / option_id / option_detail_id 가
컨텍스트(=DB)와 엇갈리는 문제를 100 % 교정하는 모듈.

● 사용 방법
    from utils.sanitize import sanitize_menus
    ...
    result["menus"] = sanitize_menus(result["menus"], store_menus)

● store_menus 형태
    {
      101: {
        "name_kr": "아메리카노",
        "options": [
          {
            "option_id": 102,
            "option_name": "온도",
            "option_details": [
              {"id": 1004, "value": "Hot"},
              {"id": 1005, "value": "Ice"}
            ]
          },
          ...
        ]
      },
      ...
    }
"""
from __future__ import annotations
from typing import List, Dict, Any
import unicodedata, re, logging

# ─────────────────────────────────────────────────────────────
# 1. 문자열 정규화 헬퍼
# ─────────────────────────────────────────────────────────────
def _n(txt: str) -> str:
    """대소문자·공백·한글자모 분해를 모두 없애고 비교용 key 반환"""
    if txt is None:
        return ""
    nkfd = unicodedata.normalize("NFKD", txt)
    return re.sub(r"\s+", "", nkfd).lower()

# ─────────────────────────────────────────────────────────────
# 2. 옵션 value 동의어 매핑 (필요하면 계속 확장)
# ─────────────────────────────────────────────────────────────
ALIAS = {
    # ─── Temperature ───
    "ice": "Ice", "iced": "Ice", "cold": "Ice",
    "아이스": "Ice", "차가운": "Ice",
    "hot": "Hot", "핫": "Hot", "따뜻": "Hot", "하뜨": "Hot",

    # ─── Size ───
    "s": "S", "small": "S", "스몰": "S", "작은": "S",
    "m": "M", "medium": "M", "미디엄": "M", "중간": "M",
    "l": "L", "large": "L", "라지": "L", "큰": "L",

    # ─── Ice Amount ───
    "noice": "얼음 없음", "얼음없음": "얼음 없음",
    "lessice": "얼음 적게", "얼음적게": "얼음 적게",
    "normalice": "얼음 보통", "얼음보통": "얼음 보통",
    "moreice": "얼음 많이", "얼음많이": "얼음 많이",

    # ─── Sweetness ───
    "0%": "당도 0%", "0퍼": "당도 0%", "무설탕": "당도 0%",
    "30%": "당도 30%", "30퍼": "당도 30%",
    "50%": "당도 50%", "50퍼": "당도 50%",
    "70%": "당도 70%", "70퍼": "당도 70%",
    "100%": "당도 100%", "100퍼": "당도 100%",

    # ─── Shot Option ───
    "shot없음": "샷 추가 없음", "샷추가없음": "샷 추가 없음",
    "light": "연하게", "연하게": "연하게",
    "shot1": "샷 1개 추가", "샷1": "샷 1개 추가", "샷한개": "샷 1개 추가",
    "shot2": "샷 2개 추가", "샷2": "샷 2개 추가", "샷두개": "샷 2개 추가",

    # ─── Syrup ───
    "no syrup": "시럽 추가 없음", "시럽없음": "시럽 추가 없음",
    "바닐라": "바닐라 시럽 추가", "바닐라시럽": "바닐라 시럽 추가",
    "카라멜": "카라멜 시럽 추가", "카라멜시럽": "카라멜 시럽 추가",
    "헤이즐넛": "헤이즐넛 시럽 추가", "헤이즐넛시럽": "헤이즐넛 시럽 추가",

    # ─── Whipped Cream ───
    "휘핑없음": "휘핑크림 없음", "no whip": "휘핑크림 없음",
    "휘핑": "휘핑크림 추가", "휘핑추가": "휘핑크림 추가",

    # ─── Milk Change ───
    "normalmilk": "일반 우유", "우유": "일반 우유",
    "lowfat": "저지방 우유", "저지방": "저지방 우유",
    "soy": "두유", "soymilk": "두유",
    "oat": "오트 우유", "oatmilk": "오트 우유",
}

def canonical(val: str) -> str:
    """동의어 → 공식 value 로 치환 (없으면 원본)"""
    return ALIAS.get(_n(val), val)

# ─────────────────────────────────────────────────────────────
# 3. 메인 진입점
# ─────────────────────────────────────────────────────────────
def sanitize_menus(
    menus_from_llm: List[Dict[str, Any]],
    store_menus: Dict[int, Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    LLM 응답의 menus 배열을 매장 DB에 맞춰 정합성 교정.
      • menu_id 없거나 잘못됨  → menu_name 으로 다시 매핑
      • option_id / detail_id  → option_name + value 로 다시 매핑
    반환값: 교정 완료된 새 menus (불일치로 매핑 실패한 항목은 자동 제거)
    """
    # ── 인덱스 빌드 ───────────────────────────────────────────
    name2id = { _n(v["name_kr"]): mid for mid, v in store_menus.items() }

    # (menu_id, option_name_key)      → option_dict
    opt_idx: Dict[tuple, Dict] = {}
    # (option_id, canonical_value)    → detail_dict
    det_idx: Dict[tuple, Dict] = {}

    for mid, m in store_menus.items():
        for opt in m.get("options", []):
            opt_key = (mid, _n(opt["option_name"]))
            opt_idx[opt_key] = opt
            for d in opt.get("option_details", []):
                det_idx[(opt["option_id"], canonical(d["value"]))] = d

    # ── 교정 시작 ─────────────────────────────────────────────
    cleaned: list[Dict[str, Any]] = []
    for m in menus_from_llm:
        # 1) menu_id 교정
        mid = m.get("menu_id")
        if mid not in store_menus:
            mid = name2id.get(_n(m.get("menu_name", "")))
        if not mid:                           # 매핑 실패 → skip
            logging.warning("sanitize: menu match fail %s", m)
            continue
        m["menu_id"] = mid

        # 2) 옵션 교정
        fixed_opts: list[Dict[str, Any]] = []
        for o in m.get("options", []):
            opt = opt_idx.get((mid, _n(o.get("option_name", ""))))
            if not opt:
                logging.warning("sanitize: option name fail %s", o)
                continue

            det = det_idx.get((opt["option_id"], canonical(o.get("option_value", ""))))
            if not det:
                logging.warning("sanitize: option value fail %s", o)
                continue

            fixed_opts.append({
                "option_id":        opt["option_id"],
                "option_name":      opt["option_name"],
                "option_detail_id": det["id"],
                "option_value":     det["value"]
            })

        m["options"] = fixed_opts
        cleaned.append(m)

    return cleaned
