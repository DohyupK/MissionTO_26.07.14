import io
import numpy as np
import tensorflow as tf
from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image

app = Flask(__name__)
CORS(app)  # 프론트와 포트가 다를 때 필요

# 모델 로드 (서버 시작 시 1번만)
model = tf.keras.models.load_model('cats_and_dogs_classifier.h5')
CLASS_NAMES = ['cat', 'dog']


def preprocess_image(file):
    """FormData로 받은 파일을 모델 입력 형태로 변환"""
    img = Image.open(io.BytesIO(file.read())).convert('RGB')
    img = img.resize((150, 150))
    img_array = np.array(img, dtype=np.float32) / 255.0  # 학습 시 rescale과 동일
    img_array = np.expand_dims(img_array, axis=0)
    return img_array


@app.route('/predict', methods=['POST'])
def predict():
    # FormData에서 이미지 받기
    if 'image' not in request.files:
        return jsonify({'error': 'image 파일이 없습니다.'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': '선택된 파일이 없습니다.'}), 400

    # FormData로 함께 보낸 다른 정보도 받을 수 있음
    # user_name = request.form.get('userName')
    # description = request.form.get('description')

    try:
        img_array = preprocess_image(file)
        probability = float(model.predict(img_array, verbose=0)[0][0])

        # sigmoid 출력: 0.5 기준으로 분류
        label = CLASS_NAMES[1] if probability > 0.5 else CLASS_NAMES[0]
        confidence = probability if probability > 0.5 else 1 - probability

        return jsonify({
            'label': label,
            'confidence': round(confidence, 4),
            'probability': round(probability, 4),  # dog일 확률 (1에 가까울수록 개)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)