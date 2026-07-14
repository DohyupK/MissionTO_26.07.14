import tensorflow as tf
import numpy as np

#모델 로드
model = tf.keras.models.load_model('cats_and_dogs_classifier.h5')

# 임의의 사진 예측
test_image = tf.keras.preprocessing.image.load_img('data/test_set/dogs/dog.4100.jpg', target_size=(150, 150))
test_image = tf.keras.preprocessing.image.img_to_array(test_image)
test_image = np.expand_dims(test_image, axis=0)
result = model.predict(test_image)
class_names = ['cat', 'dog']
print(class_names[int(result[0][0])])