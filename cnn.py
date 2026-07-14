# CNN 기본 예제: MNIST 손글씨 숫자 분류

import tensorflow as tf
from tensorflow.keras.datasets import mnist
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout

# 1. 데이터 불러오기
(X_train, y_train), (X_test, y_test) = mnist.load_data()

# 2. 데이터 전처리
# 픽셀값 0~255 → 0~1로 정규화
X_train = X_train / 255.0
X_test = X_test / 255.0

# CNN 입력 형태로 변경: (데이터 수, 높이, 너비, 채널)
# MNIST는 흑백 이미지이므로 채널 수 = 1
X_train = X_train.reshape(-1, 28, 28, 1)
X_test = X_test.reshape(-1, 28, 28, 1)

# 3. CNN 모델 구성
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
    MaxPooling2D((2, 2)),

    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),

    Flatten(),

    Dense(128, activation='relu'),
    Dropout(0.3),

    Dense(10, activation='softmax')
])

# 4. 모델 컴파일
model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

# 5. 모델 구조 확인
model.summary()

# 6. 모델 학습
model.fit(
    X_train,
    y_train,
    epochs=5,
    batch_size=64,
    validation_split=0.2
)

# 7. 모델 평가
loss, accuracy = model.evaluate(X_test, y_test)

print("Test Loss:", loss)
print("Test Accuracy:", accuracy)

# 8. 모델 저장
model.save("mnist_cnn_model.keras")