"""
저장된 임베딩 + OpenAI GPT로 RAG 챗봇 실행 (외부 API Tool Calling 지원)

[chat-gpt.py와의 차이]
  chat-gpt.py  : PDF 검색 + GPT 답변
  chat-gpt2.py : PDF 검색 + GPT 답변 + GPT가 필요 시 외부 API 호출 (Function Calling)

[제품 정보 조회 예시]
  질문: "1번 제품에 대한 정보를 알려줘"
  → GPT가 fetch_product_info(1) 도구를 호출
  → https://jsonplaceholder.typicode.com/todos/1 에서 JSON 조회
  → 조회 결과를 바탕으로 답변 생성

[사전 준비]
  1. pip install openai
  2. OPENAI_API_KEY 설정
  3. python embedding.py
  4. python chat-gpt2.py
"""

import json
import os
import urllib.error
import urllib.request
from pathlib import Path

import faiss
from openai import OpenAI
from sentence_transformers import SentenceTransformer

# API 키: 환경변수 우선, 없으면 아래 상수 사용 (실제 키는 코드에 직접 넣지 마세요)
OPENAI_API_KEY = "[ENCRYPTION_KEY]"

PRODUCT_API_BASE = "https://jsonplaceholder.typicode.com/todos"

SAVE_DIR = Path("data")
INDEX_PATH = SAVE_DIR / "index.faiss"
CHUNKS_PATH = SAVE_DIR / "chunks.json"
META_PATH = SAVE_DIR / "meta.json"

EMBED_MODEL_ID = "jhgan/ko-sroberta-multitask"
GPT_MODEL = "gpt-4o-mini"

# GPT에게 제공할 도구 목록 (Function Calling)
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "fetch_product_info",
            "description": (
                "제품 번호(id)로 외부 API에서 제품 정보를 조회합니다. "
                "사용자가 'N번 제품', '제품 N' 등 제품 정보를 물을 때 사용하세요."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "product_id": {
                        "type": "integer",
                        "description": "조회할 제품 번호 (예: 1, 2, 3)",
                    }
                },
                "required": ["product_id"],
            },
        },
    }
]


def load_saved_data() -> tuple[faiss.Index, list[str], str]:
    if not INDEX_PATH.exists() or not CHUNKS_PATH.exists():
        raise FileNotFoundError(
            "임베딩 데이터가 없습니다. 먼저 `python embedding.py`를 실행하세요."
        )

    index = faiss.read_index(str(INDEX_PATH))
    chunks = json.loads(CHUNKS_PATH.read_text(encoding="utf-8"))

    embed_model_id = EMBED_MODEL_ID
    if META_PATH.exists():
        meta = json.loads(META_PATH.read_text(encoding="utf-8"))
        embed_model_id = meta.get("embed_model", EMBED_MODEL_ID)
        print(f"메타정보: PDF={meta.get('pdf_path')}, 청크={meta.get('num_chunks')}개")

    return index, chunks, embed_model_id


def retrieve(
    query: str,
    chunks: list[str],
    index: faiss.Index,
    embed_model: SentenceTransformer,
    top_k: int = 3,
) -> list[str]:
    q_emb = embed_model.encode([query], convert_to_numpy=True)
    _, indices = index.search(q_emb, top_k)
    return [chunks[i] for i in indices[0]]


# ── fetch_product_info: GPT가 호출하는 외부 API 조회 함수 ────────────────
def fetch_product_info(product_id: int) -> dict:
    """
    제품 번호로 JSON API에서 정보를 가져옵니다.
    GPT가 tool call을 요청하면 이 함수가 실제 HTTP 요청을 수행합니다.
    """
    url = f"{PRODUCT_API_BASE}/{product_id}"
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return {"error": f"HTTP {e.code}", "product_id": product_id, "url": url}
    except urllib.error.URLError as e:
        return {"error": str(e.reason), "product_id": product_id, "url": url}


def run_tool_call(tool_name: str, arguments: str) -> str:
    """GPT가 요청한 도구 이름에 맞는 함수를 실행하고 JSON 문자열로 반환합니다."""
    args = json.loads(arguments)
    if tool_name == "fetch_product_info":
        result = fetch_product_info(args["product_id"])
        return json.dumps(result, ensure_ascii=False)
    return json.dumps({"error": f"알 수 없는 도구: {tool_name}"}, ensure_ascii=False)


# ── generate_answer: GPT + Tool Calling ─────────────────────────────────
def generate_answer(
    query: str,
    contexts: list[str],
    client: OpenAI,
    model: str = GPT_MODEL,
) -> str:
    context_text = "\n".join(contexts)
    messages = [
        {
            "role": "system",
            "content": (
                "당신은 PDF 문서 기반 Q&A 어시스턴트입니다. "
                "PDF 문서 내용과 외부 API(제품 정보)를 함께 활용해 답변하세요. "
                "제품 번호에 대한 질문이면 fetch_product_info 도구로 API에서 정보를 조회하세요. "
                "문서와 API 모두에 없는 내용은 모른다고 답하세요."
            ),
        },
        {
            "role": "user",
            "content": f"문서:\n{context_text}\n\n질문: {query}",
        },
    ]

    # GPT가 tool call을 요청하면 실행 후 결과를 다시 GPT에 전달 (루프)
    while True:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
        )
        message = response.choices[0].message

        # tool call 없으면 최종 답변
        if not message.tool_calls:
            return (message.content or "").strip()

        messages.append(message)
        for tool_call in message.tool_calls:
            tool_result = run_tool_call(
                tool_call.function.name,
                tool_call.function.arguments,
            )
            print(f"  [API 호출] {tool_call.function.name}({tool_call.function.arguments})")
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": tool_result,
                }
            )


if __name__ == "__main__":
    api_key = OPENAI_API_KEY
    if not api_key:
        raise EnvironmentError(
            "OPENAI_API_KEY가 설정되지 않았습니다.\n"
            "예: $env:OPENAI_API_KEY='sk-...'"
        )

    print("저장된 임베딩 로딩 중...")
    index, chunks, embed_model_id = load_saved_data()
    embed_model = SentenceTransformer(embed_model_id)
    client = OpenAI(api_key=api_key)

    print(f"준비 완료 (GPT: {GPT_MODEL}, Tool Calling 활성화)")
    print("질문 예시: '1번 제품에 대한 정보를 알려줘' (종료: quit)")
    while True:
        query = input("\n질문: ").strip()
        if not query or query.lower() in {"quit", "exit", "종료"}:
            print("챗봇을 종료합니다.")
            break

        top_chunks = retrieve(query, chunks, index, embed_model)
        answer = generate_answer(query, top_chunks, client)
        print("답변:", answer)
