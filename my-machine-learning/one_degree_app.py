import joblib
import numpy as np


#함수정의
def predict_value(x:float)->float:
    #모델로드
    loaded_model = joblib.load('models/one_degree_model.pkl')


    #임의의 값으로 예측
    new_data = np.array([[x]])
    prediction = loaded_model.predict(new_data)

    return prediction[0][0]




value = input("값을 입력하세요: ")
value = float(value)


result = predict_value(x=value)
print(result)




