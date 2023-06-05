import tensorflow
from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np

np.set_printoptions(suppress=True)
model = tensorflow.keras.models.load_model(
  "Training_data/keras/keras_Model.h5", compile=False)
class_names = open("Training_data/keras/labels.txt", "r").readlines()
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
size = (224, 224)


def check_img_for_word(image):
  image.convert("RGB")
  image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
  image_array = np.asarray(image)
  normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
  data[0] = normalized_image_array
  prediction = model.predict(data)
  return round(prediction[0][0], 1)
