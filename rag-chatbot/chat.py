"""
PDF 기반 RAG 챗봇 예제

[RAG(Retrieval-Augmented Generation) 답변 원리]
  일반 LLM은 학습 데이터에 없는 내용은 모릅니다.
  RAG는 "먼저 관련 문서를 찾고(Retrieval), 그 내용을 프롬프트에 넣어 답을 생성(Generation)"합니다.

  질문 입력
    → (1) PDF에서 추출한 텍스트 중 질문과 가장 관련 있는 부분을 벡터 검색으로 찾음
    → (2) 찾은 문서 조각(context) + 질문을 하나의 프롬프트로 합침
    → (3) 로컬 LLM이 프롬프트를 읽고, 다음 토큰을 하나씩 예측하며 답변 문장을 생성

  ※ 외부 API(GPT 등)가 아니라, Hugging Face에서 받은 모델을 내 PC에서 직접 실행합니다.

필요 패키지:
pip install pdfplumber faiss-cpu sentence-transformers transformers torch --break-system-packages
"""

import torch
import faiss
import pdfplumber
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForCausalLM


# ── 1단계: PDF → 텍스트 ──────────────────────────────────────────────
# PDF는 바이너리 파일이므로, pdfplumber로 각 페이지의 글자를 순서대로 추출합니다.
def extract_text_from_pdf(path: str) -> str:
    text = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text


# ── 2단계: 텍스트 → 청크(chunk) ────────────────────────────────────────
# LLM은 한 번에 읽을 수 있는 길이(컨텍스트 윈도우)에 제한이 있습니다.
# 긴 문서를 500자 단위로 잘라 검색·참조 단위로 만듭니다.
# overlap(겹침)을 두면 문장이 청크 경계에서 잘리더라도 문맥이 이어집니다.
def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks


# ── 3단계: 임베딩 모델 (검색용) ─────────────────────────────────────────
# SentenceTransformer는 문장을 고정 길이 숫자 벡터(임베딩)로 변환합니다.
# 의미가 비슷한 문장 → 벡터 공간에서 가까운 위치에 놓입니다.
# (내부적으로 Transformer encoder + self-attention 사용)
embed_model = SentenceTransformer("jhgan/ko-sroberta-multitask")


# 모든 청크를 벡터로 변환한 뒤 FAISS 인덱스에 저장합니다.
# FAISS는 수많은 벡터 중 "가장 가까운(유사한) 벡터"를 빠르게 찾는 검색 엔진입니다.
def build_index(chunks: list[str]):
    embeddings = embed_model.encode(chunks, convert_to_numpy=True)
    index = faiss.IndexFlatL2(embeddings.shape[1])  # L2 거리(유클리드 거리) 기준 검색
    index.add(embeddings)
    return index


# ── 4단계: Retrieval (관련 문서 검색) ──────────────────────────────────
# 질문도 같은 방식으로 벡터화한 뒤, 인덱스에서 가장 가까운 top_k개 청크를 가져옵니다.
# 거리가 가까울수록 질문과 의미적으로 관련이 높다고 판단합니다.
def retrieve(query: str, chunks: list[str], index, top_k: int = 3) -> list[str]:
    q_emb = embed_model.encode([query], convert_to_numpy=True)
    _, indices = index.search(q_emb, top_k)
    return [chunks[i] for i in indices[0]]


# ── 5단계: Generation (답변 생성) ──────────────────────────────────────
# CausalLM(인과 언어 모델): 이전 토큰들을 보고 "다음에 올 단어"를 확률적으로 예측합니다.
# 이 과정을 max_new_tokens번 반복하면 문장 전체가 만들어집니다.
# attention 메커니즘으로 프롬프트 안의 문서·질문 토큰을 참조하며 답변을 생성합니다.
GEN_MODEL_ID = "heegyu/polyglot-ko-1.3b-chat"
gen_tokenizer = AutoTokenizer.from_pretrained(GEN_MODEL_ID)   # 텍스트 ↔ 숫자 토큰 변환
gen_model = AutoModelForCausalLM.from_pretrained(GEN_MODEL_ID)  # 토큰 예측 모델


def generate_answer(query: str, contexts: list[str]) -> str:
    # 검색된 청크들을 프롬프트의 "문서" 섹션에 삽입 → LLM이 이 내용을 근거로 답변
    context_text = "\n".join(contexts)
    prompt = (
        "당신은 AI 챗봇입니다. 사용자에게 도움이 되고 유익한 내용을 제공해야합니다. "
        "답변은 길고 자세하며 친절한 설명을 덧붙여서 작성하세요.\n\n"
        f"### 문서:\n{context_text}\n\n"
        f"### 사용자:\n{query}\n\n"
        "### 챗봇:\n"  # 모델이 이 지점 이후부터 답변 토큰을 생성
    )

    # 프롬프트를 토큰 ID 시퀀스로 변환 (max_length 초과 시 잘림)
    inputs = gen_tokenizer(prompt, return_tensors="pt", truncation=True, max_length=1024)
    inputs.pop("token_type_ids", None)  # CausalLM은 token_type_ids를 사용하지 않음

    # torch.no_grad(): 추론만 하므로 역전파(학습) 비활성화 → 메모리·속도 절약
    with torch.no_grad():
        outputs = gen_model.generate(**inputs, max_new_tokens=200)

    # 생성된 토큰 ID를 다시 한국어 텍스트로 디코딩
    decoded = gen_tokenizer.decode(outputs[0], skip_special_tokens=True)
    # 프롬프트 부분을 제거하고 "### 챗봇:" 이후 생성된 답변만 추출
    return decoded.split("### 챗봇:")[-1].strip()


# ── 실행 흐름 ───────────────────────────────────────────────────────────
# 시작 시: PDF 로딩 → 청크 분할 → 인덱스 구축 (1회)
# 질문마다: retrieve(검색) → generate_answer(생성) 반복
if __name__ == "__main__":
    pdf_path = "sample.pdf"
    text = extract_text_from_pdf(pdf_path)
    chunks = chunk_text(text)
    index = build_index(chunks)

    print("PDF 로딩 완료. 질문을 입력하세요. (종료: quit 또는 exit)")
    while True:
        query = input("\n질문: ").strip()
        if not query or query.lower() in {"quit", "exit", "종료"}:
            print("챗봇을 종료합니다.")
            break

        top_chunks = retrieve(query, chunks, index)   # RAG 1단계: 관련 문서 찾기
        answer = generate_answer(query, top_chunks)   # RAG 2단계: 문서 기반 답변 생성
        print("답변:", answer)
 
 
# ── 부록: attention 핵심 연산 (embed_model, gen_model 내부에서 수천 번 반복) ──
# Q(질의), K(키), V(값) 벡터 간 유사도를 계산해 "어떤 토큰에 집중할지" 가중치를 구합니다.
# embed_model: 문장 전체 문맥을 반영한 벡터 생성 시 사용 (encoder attention)
# gen_model  : 답변 생성 시 프롬프트의 문서·질문 토큰을 참조할 때 사용 (decoder attention)
def scaled_dot_product_attention(Q, K, V):
    d_k = Q.size(-1)
    scores = torch.matmul(Q, K.transpose(-2, -1)) / (d_k ** 0.5)  # 유사도 점수
    weights = torch.softmax(scores, dim=-1)                        # 확률 분포로 변환
    return torch.matmul(weights, V), weights                       # 가중 합산 → 출력