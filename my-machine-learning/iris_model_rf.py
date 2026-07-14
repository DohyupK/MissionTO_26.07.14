import joblib
import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score



# 1. 데이터 로드
iris = load_iris()
print(iris.feature_names)
print(iris.target_names)
X = iris.data
y = iris.target

# 2. 데이터 전처리

# 3. 학습 및 테스트 데이터 분할
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# 4. 모델 선정
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

#5 . 예측
y_pred = model.predict(X_test)


#6. 평가지표, 정확도, f1 스코어
print("정확도:", accuracy_score(y_test, y_pred))
f1_score_weighted = f1_score(y_test, y_pred,average="weighted")
print("F1 Score(weighted):", f1_score_weighted)

f1_score_macro = f1_score(y_test, y_pred,average="macro")
print("F1 Score(macro):", f1_score_macro)



#7.모델저장
joblib.dump(model, "models/iris_model_v1.0.0_ac_1.0.pkl")

#8.모델로드
loaded_model = joblib.load("models/iris_model_v1.0.0_ac_1.0.pkl")


#9.임의의 값으로 예측
new_data = np.array([[5.1,3.5,1.4,0.2]])
prediction = loaded_model.predict(new_data)
class_nmuber = prediction[0]

predicted_species = iris.target_names[class_nmuber]
print(predicted_species)
