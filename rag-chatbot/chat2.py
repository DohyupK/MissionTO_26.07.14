"""
저장된 임베딩을 불러와 RAG 챗봇 실행

[chat.py와의 차이]
  chat.py     : 실행할 때마다 PDF 읽기 → 청크 분할 → 임베딩 (느림)
  chat2.py    : embedding.py가 미리 저장한 데이터를 로드 → 바로 질문 가능 (빠름)

[실행 순서]
  1. python embedding.py  → data/ 폴더에 임베딩 저장 (PDF 변경 시에만 재실행)
  2. python chat2.py      → 저장된 데이터 로드 후 챗봇 대화

[답변 흐름]
  질문 입력 → retrieve()로 관련 청크 검색 → generate_answer()로 답변 생성
"""

import json
from pathlib import Path

import torch
import faiss
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForCausalLM

# embedding.py가 저장하는 파일 경로
SAVE_DIR = Path("data")
INDEX_PATH = SAVE_DIR / "index.faiss"   # FAISS 벡터 인덱스 (검색용)
CHUNKS_PATH = SAVE_DIR / "chunks.json"  # 원본 텍스트 청크 (인덱스 번호와 1:1 대응)
META_PATH = SAVE_DIR / "meta.json"      # 임베딩 모델명, PDF 경로 등 메타정보

GEN_MODEL_ID = "heegyu/polyglot-ko-1.3b-chat"       # 답변 생성용 LLM
EMBED_MODEL_ID = "jhgan/ko-sroberta-multitask"      # 질문 임베딩용 (검색 시 사용)


# ── load_saved_data: 저장된 임베딩 데이터 로드 ──────────────────────────
# embedding.py가 data/ 폴더에 저장해 둔 파일들을 읽어옵니다.
# FAISS 인덱스(벡터)와 chunks.json(원문)을 함께 불러야 검색 결과를 텍스트로 복원할 수 있습니다.
def load_saved_data() -> tuple[faiss.Index, list[str], str]:
    # 필수 파일 존재 여부 확인 (없으면 embedding.py 먼저 실행하라고 안내)
    if not INDEX_PATH.exists() or not CHUNKS_PATH.exists():
        raise FileNotFoundError(
            "임베딩 데이터가 없습니다. 먼저 `python embedding.py`를 실행하세요."
        )

    # index.faiss: 문서 청크들의 임베딩 벡터가 저장된 검색 인덱스
    index = faiss.read_index(str(INDEX_PATH))
    # chunks.json: FAISS는 벡터(숫자)만 저장하므로, 원본 텍스트는 별도 JSON으로 보관
    chunks = json.loads(CHUNKS_PATH.read_text(encoding="utf-8"))

    # meta.json에서 임베딩에 사용된 모델명을 읽음 (질문 임베딩 시 동일 모델을 써야 검색이 정확함)
    embed_model_id = EMBED_MODEL_ID
    if META_PATH.exists():
        meta = json.loads(META_PATH.read_text(encoding="utf-8"))
        embed_model_id = meta.get("embed_model", EMBED_MODEL_ID)
        print(f"메타정보: PDF={meta.get('pdf_path')}, 청크={meta.get('num_chunks')}개")

    return index, chunks, embed_model_id


# ── retrieve: 관련 문서 검색 (RAG Retrieval) ───────────────────────────
# 사용자 질문을 벡터로 변환한 뒤, 저장된 인덱스에서 의미가 가장 가까운 청크를 찾습니다.
# 문서 청크는 이미 임베딩되어 있으므로, 질문만 실시간으로 임베딩합니다.
def retrieve(
    query: str,
    chunks: list[str],
    index: faiss.Index,
    embed_model: SentenceTransformer,
    top_k: int = 3,
) -> list[str]:
    # 1) 질문 → 숫자 벡터 변환 (문서 임베딩과 같은 모델·같은 벡터 공간 사용)
    q_emb = embed_model.encode([query], convert_to_numpy=True)

    # 2) FAISS 검색: L2(유클리드) 거리가 가장 가까운 top_k개 벡터의 인덱스 번호 반환
    _, indices = index.search(q_emb, top_k)

    # 3) 인덱스 번호 → chunks 리스트에서 실제 텍스트로 매핑
    return [chunks[i] for i in indices[0]]


# ── generate_answer: LLM 답변 생성 (RAG Generation) ─────────────────────
# retrieve()에서 찾은 문서 청크를 프롬프트에 넣고, 로컬 LLM이 문서를 참고해 답변을 생성합니다.
# CausalLM은 이전 토큰을 보고 다음 토큰을 하나씩 예측하는 방식으로 문장을 만듭니다.
def generate_answer(
    query: str,
    contexts: list[str],
    gen_tokenizer: AutoTokenizer,
    gen_model: AutoModelForCausalLM,
) -> str:
    # 검색된 청크들을 하나의 문자열로 합쳐 프롬프트의 "문서" 섹션에 삽입
    context_text = "\n".join(contexts)
    prompt = (
        "당신은 AI 챗봇입니다. 사용자에게 도움이 되고 유익한 내용을 제공해야합니다. "
        "답변은 길고 자세하며 친절한 설명을 덧붙여서 작성하세요.\n\n"
        f"### 문서:\n{context_text}\n\n"
        f"### 사용자:\n{query}\n\n"
        "### 챗봇:\n"  # 모델이 이 줄 이후부터 답변 토큰을 생성
    )

    # 프롬프트를 토큰 ID 시퀀스로 변환 (1024 토큰 초과 시 앞부분 잘림)
    inputs = gen_tokenizer(prompt, return_tensors="pt", truncation=True, max_length=1024)
    inputs.pop("token_type_ids", None)  # CausalLM은 BERT용 token_type_ids를 사용하지 않음

    # 추론 전용 모드: 학습(역전파) 비활성화 → 메모리 절약 및 속도 향상
    with torch.no_grad():
        outputs = gen_model.generate(**inputs, max_new_tokens=200)  # 최대 200토큰까지 생성

    # 토큰 ID → 한국어 텍스트로 복원 후, 프롬프트 부분을 제거하고 답변만 추출
    decoded = gen_tokenizer.decode(outputs[0], skip_special_tokens=True)
    return decoded.split("### 챗봇:")[-1].strip()


# ── 실행 흐름 ───────────────────────────────────────────────────────────
# [시작 시 1회] 저장된 임베딩 + 모델 로드
# [질문마다]     retrieve(검색) → generate_answer(생성) 반복
if __name__ == "__main__":
    print("저장된 임베딩 로딩 중...")
    index, chunks, embed_model_id = load_saved_data()

    embed_model = SentenceTransformer(embed_model_id)               # 질문 임베딩용
    gen_tokenizer = AutoTokenizer.from_pretrained(GEN_MODEL_ID)     # 텍스트 ↔ 토큰 변환
    gen_model = AutoModelForCausalLM.from_pretrained(GEN_MODEL_ID)  # 답변 생성용 LLM

    print("준비 완료. 질문을 입력하세요. (종료: quit 또는 exit)")
    while True:
        query = input("\n질문: ").strip()
        if not query or query.lower() in {"quit", "exit", "종료"}:
            print("챗봇을 종료합니다.")
            break

        top_chunks = retrieve(query, chunks, index, embed_model)              # RAG 1단계: 관련 문서 검색
        answer = generate_answer(query, top_chunks, gen_tokenizer, gen_model)  # RAG 2단계: 문서 기반 답변 생성
        print("답변:", answer)
