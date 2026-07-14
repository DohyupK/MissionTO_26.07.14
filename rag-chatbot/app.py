"""
Flask 기본 구조

실행:
  pip install flask openai faiss-cpu sentence-transformers
  python embedding.py   # 최초 1회
  python app.py

접속:
  http://127.0.0.1:5000
"""

import importlib.util
import os
from pathlib import Path

from flask import Flask, jsonify, render_template, request
from openai import OpenAI
from sentence_transformers import SentenceTransformer

# 파일명에 하이픈이 있어 importlib로 chat_gpt.py 로드
_MODULE_PATH = Path(__file__).parent / "chat_gpt.py"
_spec = importlib.util.spec_from_file_location("chat_gpt", _MODULE_PATH)
chat_gpt = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(chat_gpt)

app = Flask(__name__)

_chatbot: dict | None = None


def get_chatbot() -> dict:
    """임베딩·GPT 클라이언트를 한 번만 로드합니다."""
    global _chatbot
    if _chatbot is not None:
        return _chatbot

    api_key = os.environ.get("OPENAI_API_KEY") or chat_gpt.OPENAI_API_KEY
    if not api_key:
        raise EnvironmentError(
            "OPENAI_API_KEY가 설정되지 않았습니다.\n"
            "예: $env:OPENAI_API_KEY='sk-...'"
        )

    index, chunks, embed_model_id = chat_gpt.load_saved_data()
    embed_model = SentenceTransformer(embed_model_id)
    client = OpenAI(api_key=api_key)

    _chatbot = {
        "index": index,
        "chunks": chunks,
        "embed_model": embed_model,
        "client": client,
    }
    return _chatbot


@app.route("/")
def index():
    """메인 페이지"""
    return render_template("index.html")


@app.route("/health")
def health():
    """서버 상태 확인"""
    return jsonify({"status": "ok"})


@app.route("/api/chat", methods=["POST"])
def chat():
    """RAG + GPT Tool Calling 챗봇 API"""
    data = request.get_json(silent=True) or {}
    query = (data.get("query") or "").strip()

    if not query:
        return jsonify({"error": "query가 필요합니다."}), 400

    try:
        bot = get_chatbot()
        top_chunks = chat_gpt.retrieve(
            query, bot["chunks"], bot["index"], bot["embed_model"]
        )
        answer = chat_gpt.generate_answer(query, top_chunks, bot["client"])
        return jsonify({"query": query, "answer": answer})
    except FileNotFoundError as e:
        return jsonify({"error": str(e)}), 503
    except EnvironmentError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": f"답변 생성 중 오류: {e}"}), 500


@app.errorhandler(404)
def not_found(_error):
    return jsonify({"error": "페이지를 찾을 수 없습니다."}), 404


@app.errorhandler(500)
def internal_error(_error):
    return jsonify({"error": "서버 오류가 발생했습니다."}), 500


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
