"""
PDF 임베딩 생성 및 저장

실행: python embedding.py
  → data/index.faiss  (벡터 인덱스)
  → data/chunks.json  (원본 텍스트 청크)
  → data/meta.json    (모델명, PDF 경로 등 메타정보)

chat2.py에서 이 파일들을 불러와 검색에 사용합니다.
"""

import json
from pathlib import Path

import faiss
import pdfplumber
from sentence_transformers import SentenceTransformer

EMBED_MODEL_ID = "jhgan/ko-sroberta-multitask"
SAVE_DIR = Path("data")
INDEX_PATH = SAVE_DIR / "index.faiss"
CHUNKS_PATH = SAVE_DIR / "chunks.json"
META_PATH = SAVE_DIR / "meta.json"


def extract_text_from_pdf(path: str) -> str:
    text = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks


def build_and_save(pdf_path: str, chunk_size: int = 500, overlap: int = 50) -> None:
    print(f"PDF 읽는 중: {pdf_path}")
    text = extract_text_from_pdf(pdf_path)
    chunks = chunk_text(text, chunk_size, overlap)
    print(f"청크 {len(chunks)}개 생성")

    print(f"임베딩 모델 로딩: {EMBED_MODEL_ID}")
    embed_model = SentenceTransformer(EMBED_MODEL_ID)
    embeddings = embed_model.encode(chunks, convert_to_numpy=True)

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    SAVE_DIR.mkdir(exist_ok=True)
    faiss.write_index(index, str(INDEX_PATH))
    CHUNKS_PATH.write_text(json.dumps(chunks, ensure_ascii=False), encoding="utf-8")
    META_PATH.write_text(
        json.dumps(
            {
                "embed_model": EMBED_MODEL_ID,
                "pdf_path": pdf_path,
                "chunk_size": chunk_size,
                "overlap": overlap,
                "num_chunks": len(chunks),
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print(f"저장 완료:")
    print(f"  - {INDEX_PATH}")
    print(f"  - {CHUNKS_PATH}")
    print(f"  - {META_PATH}")


if __name__ == "__main__":
    build_and_save("sample.pdf")
