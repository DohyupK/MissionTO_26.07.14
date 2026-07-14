from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score ,confusion_matrix

# 데이터셋 로드
wine = load_wine()
X = wine.data
y = wine.target

# 데이터셋 나누기 (Train/Test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

print(X_train)

# 데이터 정규화
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

print(X_train)


# 랜덤 포레스트 모델 학습
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# 모델 예측
y_pred = model.predict(X_test)

# 평가 결과 출력
print("Accuracy:", accuracy_score(y_test, y_pred))
#혼돈 행렬
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
