import pandas as pd
try:
    from konlpy.tag import Mecab  # optional: may fail at runtime without MeCab installed
except Exception:  # fallback import path when Mecab is unavailable
    Mecab = None
from konlpy.tag import Okt
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout
import pickle


# 1. 데이터 로드
def load_data():
    train_data = pd.read_csv("data/review_train_data/ratings_train.txt", sep='\t').dropna()
    test_data = pd.read_csv("data/review_train_data/ratings_test.txt", sep='\t').dropna()
    return train_data, test_data

# 2. 형태소 분석기 준비 (Mecab 우선, 실패 시 Okt로 폴백)
def get_tagger():
    if Mecab is not None:
        try:
            return Mecab()
        except Exception:
            pass
    return Okt()

# 2-1. 데이터 전처리 헬퍼
def preprocess_text(text):
    tagger = get_tagger()
    tokens = tagger.morphs(text)
    return ' '.join(tokens)

def preprocess_data(train_data, test_data):
    tagger = get_tagger()
    train_data['document'] = train_data['document'].apply(lambda x: ' '.join(tagger.morphs(x)))
    test_data['document'] = test_data['document'].apply(lambda x: ' '.join(tagger.morphs(x)))
    return train_data, test_data

# 3. 시퀀스 변환 및 패딩
def prepare_sequences(train_data, test_data, max_words=20000, max_len=100):
    tokenizer = Tokenizer(num_words=max_words)
    tokenizer.fit_on_texts(train_data['document'])

    X_train_seq = tokenizer.texts_to_sequences(train_data['document'])
    X_test_seq = tokenizer.texts_to_sequences(test_data['document'])

    X_train_pad = pad_sequences(X_train_seq, maxlen=max_len)
    X_test_pad = pad_sequences(X_test_seq, maxlen=max_len)

    return X_train_pad, train_data['label'], X_test_pad, test_data['label'], tokenizer

# 4. 모델 정의
def build_model(input_dim, output_dim=128, input_length=100):
    model = Sequential([
        Embedding(input_dim=input_dim, output_dim=output_dim, input_length=input_length),
        LSTM(128, return_sequences=False),
        Dropout(0.5),
        Dense(1, activation='sigmoid')  # 긍정/부정 분류
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model



# 5. 감성 예측 함수
def predict_sentiment(model, tokenizer, text, max_len=100):
    tagger = get_tagger()
    processed_text = ' '.join(tagger.morphs(text))
    sequence = tokenizer.texts_to_sequences([processed_text])
    padded_sequence = pad_sequences(sequence, maxlen=max_len)
    prediction = model.predict(padded_sequence)
    return "긍정" if prediction > 0.5 else "부정"




# 6. 메인 실행 코드
if __name__ == "__main__":
    # 데이터 로드
    train_data, test_data = load_data()

    # 데이터 전처리
    train_data, test_data = preprocess_data(train_data, test_data)

    # 시퀀스 준비
    max_words = 20000
    max_len = 100
    X_train, y_train, X_test, y_test, tokenizer = prepare_sequences(train_data, test_data, max_words, max_len)

    # 모델 생성
    model = build_model(input_dim=max_words, input_length=max_len)
    model.summary()

    # 모델 학습
    model.fit(X_train, y_train, validation_split=0.2, epochs=5, batch_size=64)

    # 모델 평가
    loss, accuracy = model.evaluate(X_test, y_test)
    print(f"Test Accuracy: {accuracy}")


    # 모델 저장
    model.save('naver-review-model.keras')

    #토크나이저 저장
    with open('tokenizer.pkl', 'wb') as f:
        pickle.dump(tokenizer, f)

    # 새로운 댓글 예측
    while True:
        new_comment = input("분석할 댓글을 입력하세요 (종료: 'exit'): ")
        if new_comment.lower() == "exit":
            break
        result = predict_sentiment(model, tokenizer, new_comment, max_len)
        print(f"예측 결과: {result}")