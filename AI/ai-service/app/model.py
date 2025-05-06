# model.py
import json
import logging
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from typing import Dict, Any, List

log = logging.getLogger(__name__)
_llm = ChatOpenAI(model="gpt-4.1", temperature=0)

# 다국어 지원 개선 🌍
LANGUAGE_MAP = {
    'kr': 'Korean',
    'en': 'English',
    'cn': 'Chinese',
    'ja': 'Japanese',
    'es': 'Spanish',
    'fr': 'French'
}

def llm_parse(utter: str, options_mappings: Dict[str, Any], language: str = "kr") -> dict:
    """매장별 옵션 매핑을 고려한 LLM 파싱"""
    
    # 다국어 지원 프롬프트 🌍
    lang_name = LANGUAGE_MAP.get(language, 'English')
    
    system_prompt = f"""You are a cafe kiosk voice order parser.
    Convert user speech to exact JSON format.
    
    This store's option mappings:
    {generate_options_prompt(options_mappings)}
    
    JSON format rules:
    - menuName: Menu name (required)
    - quantity: Number of items (default: 1)
    - temperature: Temperature (HOT/ICE)
    - size: Size (depends on store options)
    - decaf: Decaffeinated (boolean)
    - Other options stored in respective keys
    
    Respond in {lang_name}."""
    
    messages = [SystemMessage(content=system_prompt)]
    
    # Few-shot 예시 (매장별 맞춤)
    examples = get_store_examples(options_mappings, language)
    for user_msg, expected_json in examples:
        messages.append(HumanMessage(content=user_msg))
        messages.append(AIMessage(content=json.dumps(expected_json, ensure_ascii=False)))
    
    messages.append(HumanMessage(content=utter))
    
    try:
        response = _llm.invoke(messages)
        # AIMessage에서 content 추출
        content = response.content if hasattr(response, 'content') else str(response)
        parsed = json.loads(content)
        
        # 매장 옵션에 맞게 정규화
        return normalize_with_mappings(parsed, options_mappings)
        
    except Exception as e:
        log.warning("LLM parse 실패: %s", e)
        return {"menuName": utter}

def generate_options_prompt(mappings: Dict[str, Any]) -> str:
    """매장별 옵션 매핑 프롬프트 생성"""
    prompt_parts = []
    for option_name, mapping_list in mappings.items():
        values = []
        for m in mapping_list:
            if m.get("original") and m.get("mapped"):
                values.append(f"{m['mapped']} -> {m['original']}")
        if values:
            prompt_parts.append(f"{option_name}: {', '.join(values)}")
    return "\n".join(prompt_parts)

def normalize_with_mappings(parsed: Dict[str, Any], mappings: Dict[str, Any]) -> Dict[str, Any]:
    """매핑을 통해 값 정규화"""
    for option_name, mapping_list in mappings.items():
        # 옵션키 매핑
        key_map = {
            "온도": "temperature",
            "사이즈": "size",
            "얼음량": "ice_amount",
            "당도": "sweetness",
            "휘핑크림": "whipped_cream",
            "샷 추가": "extra_shot",
            "시럽 추가": "extra_syrup",
            "우유 변경": "milk_change"
        }
        
        field_key = key_map.get(option_name, option_name.lower().replace(" ", "_"))
        
        if field_key in parsed:
            user_value = parsed[field_key]
            for m in mapping_list:
                if str(m.get("mapped", "")).lower() == str(user_value).lower():
                    parsed[field_key] = m["original"]
                    # 옵션 상세 ID와 추가 가격 저장
                    parsed[f"{field_key}_detail_id"] = m.get("id")
                    parsed[f"{field_key}_price"] = m.get("additional_price", 0)
                    break
    
    return parsed

def get_store_examples(options_mappings: Dict[str, Any], language: str) -> List[tuple]:
    """매장별 맞춤 few-shot 예시 생성"""
    examples = []
    
    # 기본 예시들
    if language == "kr":
        examples.extend([
            ("아메리카노 하나", {
                "menuName": "아메리카노",
                "quantity": 1
            }),
            ("카페라떼 두 개", {
                "menuName": "카페라떼",
                "quantity": 2
            }),
            ("아아 하나, 뜨아 하나, 카페라떼 하나", {
                "orders": [
                    {"menuName": "아메리카노", "temperature": "ICE", "quantity": 1},
                    {"menuName": "아메리카노", "temperature": "HOT", "quantity": 1},
                    {"menuName": "카페라떼", "quantity": 1}
                ]
            })
        ])
    else:  # 한국어가 아닌 경우 모두 영어 예시로
        examples.extend([
            ("One Americano", {
                "menuName": "Americano",
                "quantity": 1
            }),
            ("Two Cafe Latte", {
                "menuName": "Cafe Latte",
                "quantity": 2
            }),
            ("One iced americano, one hot americano, and one latte", {
                "orders": [
                    {"menuName": "Americano", "temperature": "ICE", "quantity": 1},
                    {"menuName": "Americano", "temperature": "HOT", "quantity": 1},
                    {"menuName": "Cafe Latte", "quantity": 1}
                ]
            })
        ])
    
    # 매장의 사이즈 옵션에 따른 예시
    if "사이즈" in options_mappings:
        size_values = [m["original"] for m in options_mappings["사이즈"]]
        
        if language == "kr":
            if "S" in size_values:
                examples.append(("아아 작은거", {
                    "menuName": "아메리카노",
                    "temperature": "ICE",
                    "size": "S"
                }))
            if "Tall" in size_values:
                examples.append(("아메리카노 톨 사이즈로", {
                    "menuName": "아메리카노",
                    "size": "Tall"
                }))
        else:
            if "S" in size_values:
                examples.append(("Iced Americano Small", {
                    "menuName": "Americano",
                    "temperature": "ICE",
                    "size": "S"
                }))
            if "Tall" in size_values:
                examples.append(("Americano Tall", {
                    "menuName": "Americano",
                    "size": "Tall"
                }))
    
    # 디카페인 예시
    if language == "kr":
        examples.append(("디카페인 카페라떼 하나", {
            "menuName": "카페라떼",
            "decaf": True,
            "quantity": 1
        }))
    else:
        examples.append(("Decaf Cafe Latte", {
            "menuName": "Cafe Latte",
            "decaf": True,
            "quantity": 1
        }))
    
    return examples
