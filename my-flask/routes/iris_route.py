from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score
from flask.globals import request
from flask import Blueprint, jsonify
import db # 루트 경로의 db.py를 임포트
import joblib
import numpy as np

# Blueprint 객체 생성
iris_bp = Blueprint('iris_route', __name__, url_prefix='/api/ai')

#8.모델로드
loaded_model = joblib.load("models/iris_model_v1.0.0_ac_1.0.pkl")

@iris_bp.route('/iris', methods=['POST'])
def iris():
    try:
        conn = db.get_db_IRIS()
        with conn.cursor() as cursor:
            data = request.get_json()
            sepal_length = data.get('sepal_length')
            sepal_width = data.get('sepal_width')
            petal_length = data.get('petal_length')
            petal_width = data.get('petal_width')

            new_data = np.array([[float(sepal_length), float(sepal_width), float(petal_length), float(petal_width)]])
            prediction = loaded_model.predict(new_data)
            class_nmuber = prediction[0]
            target_name = ['setosa','versicolor','virginica']
            predicted_species = target_name[class_nmuber]
            confidence_score = loaded_model.predict_proba(new_data)[0][class_nmuber]

            cursor.execute("""INSERT INTO iris
            (sepal_length, sepal_width, petal_length, petal_width, class_name, confidence_score)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,(sepal_length, sepal_width, petal_length, petal_width, predicted_species, confidence_score ))  
            conn.commit()
            return jsonify({
                "success":True,
                "message":"아이리스, data는 예측 결과",
                "class_name":predicted_species,
                "confidence_score":confidence_score*100,
                })
    except Exception as e:
        return jsonify({
            'data':None,
            'success':False,
            'message':"데이터베이스 연결 실패",
            'error':str(e)
        })
    finally:
        db.close_db_IRIS()