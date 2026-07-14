#naver-review-model.keras 파일을 사용하여 감성 분석을 수행하는 코드

import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from konlpy.tag import Mecab
from konlpy.tag import Okt
import pickle

# 모델 로드
model = load_model('naver-review-model.keras')

# 토크나이저 로드 tokenizer.pkl 파일에서 로드
with open('tokenizer.pkl', 'rb') as f:
    tokenizer = pickle.load(f)

# 형태소 분석기 준비 (Mecab 우선, 실패 시 Okt로 폴백)
def get_tagger():
    if Mecab is not None:
        try:
            return Mecab()
        except Exception:
            pass
    return Okt()

# 최대 시퀀스 길이
max_len = 100

# 감성 예측 함수
def predict_sentiment(model, tokenizer, text, max_len=100):
    tagger = get_tagger()
    processed_text = ' '.join(tagger.morphs(text))
    sequence = tokenizer.texts_to_sequences([processed_text])
    padded_sequence = pad_sequences(sequence, maxlen=max_len)
    prediction = model.predict(padded_sequence)
    return "긍정" if prediction > 0.5 else "부정"

# 새로운 댓글 예측
while True:
    new_comment = input("분석할 댓글을 입력하세요 (종료: 'exit'): ")
    if new_comment.lower() == "exit":
        break
    result = predict_sentiment(model, tokenizer, new_comment, max_len)
    print(f"예측 결과: {result}")

