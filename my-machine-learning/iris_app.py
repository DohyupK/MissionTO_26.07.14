import joblib
import numpy as np


def predict_iris(sepal_length:float, petal_length:float, sepal_width:float, petal_width:float)->str:
    #8.모델로드
    loaded_model = joblib.load("models/iris_model_v1.0.0_ac_1.0.pkl")


    #9.임의의 값으로 예측
    new_data = np.array([[float(sepal_length), float(petal_length),float(sepal_width),float(petal_width)]])
    prediction = loaded_model.predict(new_data)
    class_number = prediction[0]

    predicted_species = ['setosa','versicolor','virginica'][class_number]
    

    return predicted_species




sepal_length = input('꽃받침 길이 입력 : ')
petal_length = input('꽃잎 길이 입력 : ')
sepal_width = input('꽃받침 너비 입력 : ')
petal_width = input('꽃잎 너비 입력 : ')

result = predict_iris(
        sepal_length=float(sepal_length), 
        petal_length=float(petal_length), 
        sepal_width=float(sepal_width), 
        petal_width=float(petal_width)
    )
print(result)




