from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib

# 1. 데이터 생성
np.random.seed(42)
X = 2 * np.random.rand(100, 1)  # 100개의 랜덤 X값 생성
y = 4 + 3 * X + np.random.randn(100, 1)  # 선형 방정식 y = 4 + 3x + noise

#테스트, 학습 데이터 분리
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#모델 선정
model = LinearRegression()
model.fit(X_train, y_train)

#평가지표 MAE,MSE,RMSE,R2
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

print("MAE:", mae)
print("MSE:", mse)
print("RMSE:", rmse)
print("R2:", r2)


#모델 저장
joblib.dump(model, 'models/one_degree_model.pkl')


#모델로드
loaded_model = joblib.load('models/one_degree_model.pkl')


#임의의 값으로 예측
new_data = np.array([[1.5]])
prediction = loaded_model.predict(new_data)
print(prediction[0][0])





