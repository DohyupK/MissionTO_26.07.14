import numpy as np
import pandas as pd
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error


#ssl
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# 데이터셋 로드
data = fetch_california_housing(as_frame=True)
df = data.frame

print(df.info())

X = df.drop(columns=['MedHouseVal'])
y = df['MedHouseVal']

#학습, 테스트 데이터 분리
X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.2, random_state=42)

#모델 학습
model = LinearRegression()
model.fit(X_train, y_train)

#예측
y_pred = model.predict(X_test)

#평가지표
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

print("MAE:", mae)
print("MSE:", mse)
print("RMSE:", rmse)
print("R2:", r2)


#모델 저장
import joblib
joblib.dump(model, 'linear_model.pkl')
print("모델이 성공적으로 저장되었습니다.")  



