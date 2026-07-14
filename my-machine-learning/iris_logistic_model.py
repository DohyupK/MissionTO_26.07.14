import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# 1. 데이터 로드 및 전처리
iris = load_iris()
print(iris.feature_names)
print(iris.target_names)
X = iris.data
y = iris.target

# 이진 분류 문제를 위해 클래스 0과 1만 선택
binary_mask = y < 2  # 클래스 0과 1만 선택
X_binary = X[binary_mask]
y_binary = y[binary_mask]


# 2. 데이터 분할 (학습 데이터와 테스트 데이터)
X_train, X_test, y_train, y_test = train_test_split(X_binary, y_binary, test_size=0.2, random_state=42)

#모델 학습
model = LogisticRegression()
model.fit(X_train, y_train)

#예측
y_pred = model.predict(X_test)

#평가
accuracy = accuracy_score(y_test, y_pred)
print("정확도: ", accuracy)


