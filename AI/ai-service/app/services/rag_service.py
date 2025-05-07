"""
rag_service.py
RAG 서비스 구현
"""

from typing import List, Dict, Any
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI 
import json
import os

# 절대 경로 사용
from app.db.vector_store import VectorStore

class RAGService:
    def __init__(self, vector_store: VectorStore, api_key: str):
        self.vector_store = vector_store
        self.llm = ChatOpenAI(
            model_kwargs={"api_key": api_key},  # api_key를 model_kwargs로 전달
            model_name="gpt-4.1", # 또는 "gpt-3.5-turbo" 등 현재 지원되는 모델
            temperature=0.7
        )
        
        # Few-shot 예제 로드
        self.few_shot_examples = self._load_few_shot_examples()
    
    def _load_few_shot_examples(self):
        """Few-shot 예제 로드"""
        # 예제 데이터는 실제 구현시 파일에서 로드
        return {
            "intent_examples": [
                {
                    "input": "아메리카노 하나 주세요",
                    "intent": "ORDER",
                    "menus": [{"menu_name": "아메리카노", "quantity": 1, "options": []}]
                },
                {
                    "input": "아이스 아메리카노 주세요",
                    "intent": "ORDER",
                    "menus": [{"menu_name": "아메리카노", "quantity": 1, "options": [{"option_name": "온도", "option_value": "ICE"}]}]
                },
                {
                    "input": "따뜻한 커피 알려줘",
                    "intent": "SEARCH",
                    "search_query": "따뜻한 커피"
                },
                {
                    "input": "결제할게요",
                    "intent": "PAYMENT",
                    "payment_method": None
                }
            ],
            "response_examples": [
                {
                    "status": "MISSING_REQUIRED_OPTIONS",
                    "menus": [{"menuName": "아메리카노", "missingRequiredOptions": [{"optionName": "온도"}]}],
                    "input": "아메리카노 주세요",
                    "response": "아메리카노를 선택하셨네요. 따뜻한 것으로 드릴까요, 차가운 것으로 드릴까요?"
                },
                {
                    "status": "READY_TO_ADD_CART",
                    "menus": [{"menuName": "아이스 아메리카노"}],
                    "input": "아이스 아메리카노 주세요",
                    "response": "아이스 아메리카노를 장바구니에 담았습니다. 더 주문하실 건가요?"
                }
            ]
        }
    
    def recognize_intent(self, text: str, language: str, screen_state: str, store_id: int = None) -> Dict[str, Any]:
        """사용자 의도 인식"""
        # Few-shot 예제 생성
        few_shot_examples_text = []
        for example in self.few_shot_examples["intent_examples"]:
            menus_json = json.dumps(example.get('menus', []), ensure_ascii=False)
            example_text = (
                f"입력: \"{example['input']}\"\n"
                f"의도: {example['intent']}\n"
                f"메뉴: {menus_json}\n"
                f"검색어: {example.get('search_query', 'null')}\n"
                f"결제방법: {example.get('payment_method', 'null')}"
            )
            few_shot_examples_text.append(example_text)

        few_shot_prompt = "\n\n".join(few_shot_examples_text)
        
        # 프롬프트 템플릿 생성
        prompt_template_str = """
        당신은 음성 키오스크 시스템의 일부로, 사용자가 말한 내용을 분석하여 의도와 메뉴, 옵션을 인식하는 역할을 합니다.
        현재 화면 상태는 '{screen_state}'입니다.
        사용자 입력: "{text}"

        1. 메뉴명 교정 규칙을 최우선으로 적용하세요:
        - "버닐라라떼/버닐라 라떼/버닐라라테/버닐라 라테" → "바닐라 라떼"
        - "아아/아이스아메리카노/아아메리카노" → "아메리카노"
        - "따아/따듯한 아메리카노/핫아메리카노" → "아메리카노"
        - "카페라떼/카페라테/라떼/라테" → "카페 라떼"
        - "헤이즐넛 라떼/헤이즐넛라떼/헤이즐 라떼" → "헤이즐넛 라떼"
        - "딸기스무디/딸기 스무디" → "딸기 스무디"
        - "블루베리 요거트/블루베리요거트스무디" → "블루베리 요거트 스무디"
        - "초콜릿라떼떼 어이스 한개 줘" → "초코라떼"
        - "어메리카노 어이스 한개 줘" → "아메리카노"

        2. 다음과 같은 옵션 매핑 규칙을 적용하세요:
        - "아이스/아이스아메리카노/차가운" → 온도 옵션의 "ICE" 값
        - "따뜻한/뜨거운/따아" → 온도 옵션의 "HOT" 값
        - "작은/스몰/S" → 사이즈 옵션의 "S" 값
        - "중간/미디엄/M" → 사이즈 옵션의 "M" 값
        - "큰/라지/L" → 사이즈 옵션의 "L" 값
        
        아래의 예시를 참고하여, 사용자의 의도와 메뉴, 옵션을 JSON 형식으로 분석해주세요:
        
        {few_shot_prompt}
        
        위 예시를 참고하여, 입력된 텍스트에 대한 분석 결과를 JSON 형식으로 제공해주세요.
        만약 "아메리카노"와 같은 커피 메뉴가 언급되었다면, 그것은 주문(ORDER) 의도입니다.
        결과는 다음 형식으로 반환해주세요:
        {{
        "intent": "ORDER 또는 SEARCH 또는 PAYMENT 중 하나",
        "menus": [
            {{
            "menu_name": "메뉴 이름 (정확한 메뉴명으로 교정해주세요)",
            "quantity": 수량,
            "options": [
                {{
                "option_id" : db에서 조회한 옵션 id
                "option_name": "옵션 이름(예: 온도, 사이즈)",
                "option_value": "옵션 값(예: HOT, ICE, S, M, L)"
                }}
            ]
            }}
        ],
        "search_query": "검색어(SEARCH 의도인 경우에만)",
        "payment_method": "결제 방법(PAYMENT 의도인 경우에만)"
        }}
        
        분석 결과:
        """
        
        # LLM을 사용하여 의도 인식
        prompt = PromptTemplate(
            template=prompt_template_str,
            input_variables=["screen_state", "text", "few_shot_prompt"]
        )
        
        chain = LLMChain(
            llm=self.llm,
            prompt=prompt
        )
        
        # 디버깅을 위해 결과 출력
        print(f"사용자 입력: {text}")
        
        result_text = chain.run(
            screen_state=screen_state,
            text=text,
            few_shot_prompt=few_shot_prompt
        )
        
        print(f"LLM 응답: {result_text}")
        
        # 결과를 파싱하여 정형화된 응답으로 변환
        try:
            # JSON 문자열을 파싱할 때 줄바꿈 및 공백 처리
            cleaned_result = result_text.strip()
            
            # JSON 형식이 아닌 머리말이나 꼬리말 제거
            if "```json" in cleaned_result:
                cleaned_result = cleaned_result.split("```json")[1].split("```")[0].strip()
            elif "```" in cleaned_result:
                cleaned_result = cleaned_result.split("```")[1].split("```")[0].strip()
            
            # 시작 위치의 { 찾기
            start_idx = cleaned_result.find('{')
            # 끝 위치의 } 찾기
            end_idx = cleaned_result.rfind('}')
            
            if start_idx != -1 and end_idx != -1:
                cleaned_result = cleaned_result[start_idx:end_idx+1]
            
            print(f"정제된 결과: {cleaned_result}")
            
            parsed_result = json.loads(cleaned_result)
            
            # 인식된 메뉴에 대한 추가 정보 조회
            if parsed_result.get("intent") == "ORDER" and parsed_result.get("menus"):
                enriched_menus = []
                for menu in parsed_result["menus"]:
                    menu_name = menu.get("menu_name")
                    original_menu_name = menu.get("original_menu_name", menu_name)  

                    if menu_name:
                        # 디버깅을 위해 검색 전 출력
                        print(f"검색할 메뉴 이름: {menu_name}, 매장 ID: {store_id}")
                        
                        # 메뉴 검색
                        search_results = self.vector_store.search_menu(menu_name, store_id, top_k=1)
                        
                        # 디버깅을 위해 검색 결과 출력
                        print(f"검색 결과: {search_results}")
                        
                        if search_results:
                            # 검색된 메뉴 정보 추가
                            menu["menu_id"] = search_results[0].get("id")
                            menu["menu_name_kr"] = search_results[0].get("name_kr")
                            menu["menu_name_en"] = search_results[0].get("name_en")
                            menu["price"] = search_results[0].get("price")
                    
                        # 교정 여부 확인 및 추가
                        if original_menu_name and original_menu_name.lower() != menu_name.lower():
                            menu["is_corrected"] = True
                            menu["original_menu_name"] = original_menu_name
                    
                    enriched_menus.append(menu)
                
                parsed_result["menus"] = enriched_menus
            
            # 결과 반환 시 raw_text와 post_text 포함
            post_text = text  # 기본값은 원본 텍스트

            # 메뉴명 교정이 있는 경우 post_text 업데이트
            for menu in parsed_result.get("menus", []):
                if menu.get("is_corrected") and menu.get("original_menu_name") and menu.get("menu_name"):
                    post_text = post_text.replace(menu.get("original_menu_name"), menu.get("menu_name"))
            
            
            return {
                "intent_type": parsed_result.get("intent", "UNKNOWN"),
                "confidence": parsed_result.get("confidence", 0.8),
                "recognized_menus": parsed_result.get("menus", []),
                "search_query": parsed_result.get("search_query"),
                "payment_method": parsed_result.get("payment_method"),
                "raw_text": text,
                "screen_state": screen_state
            }
            
        except json.JSONDecodeError as e:
            # 디버깅을 위해 오류 정보 출력
            print(f"JSON 파싱 오류: {e}")
            print(f"파싱 시도한 문자열: {result_text}")
            
            # 파싱 실패 시 기본 응답
            return {
                "intent_type": "UNKNOWN",
                "confidence": 0.5,
                "recognized_menus": [],
                "raw_text": text,
                "screen_state": screen_state
            }
    
    def generate_response(self, status: str, menus: List[Dict[str, Any]], raw_text: str, screen_state: str) -> str:
        """응답 생성"""
        # Few-shot 프롬프트 구성
        few_shot_examples_text = []
        for example in self.few_shot_examples["response_examples"]:
            menus_json = json.dumps(example.get('menus', []), ensure_ascii=False)
            example_text = (
                f"상태: {example['status']}\n"
                f"메뉴: {menus_json}\n"
                f"사용자 입력: \"{example['input']}\"\n"
                f"응답: \"{example['response']}\""
            )
            few_shot_examples_text.append(example_text)

        few_shot_prompt = "\n\n".join(few_shot_examples_text)
        
        menus_str = json.dumps(menus, ensure_ascii=False)
        
         # 프롬프트 템플릿 생성
        prompt_template_str = """
        당신은 음성 키오스크 시스템의 응답 생성 모델입니다. 검증된 정보를 바탕으로 사용자에게 적절한 응답을 생성해야 합니다.
        
        현재 화면 상태: {screen_state}
        현재 상태: {status}
        메뉴 정보: {menus_str}
        사용자 입력: "{raw_text}"
        
        아래 예시를 참고하여 사용자에게 자연스럽고 친절한 응답을 생성해주세요:
        
        {few_shot_prompt}
        
        응답:
        """
        
        # LLM을 사용하여 응답 생성
        prompt = PromptTemplate(
            template=prompt_template_str,
            input_variables=["screen_state", "status", "menus_str", "raw_text", "few_shot_prompt"]
        )
        
        chain = LLMChain(
            llm=self.llm,
            prompt=prompt
        )
        
        response = chain.run(
            screen_state=screen_state,
            status=status,
            menus_str=menus_str,
            raw_text=raw_text,
            few_shot_prompt=few_shot_prompt
        )
        
        return response.strip()