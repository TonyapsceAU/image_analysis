import tensorflow as tf
import numpy as np
import cv2
import urllib.request

URL = "https://teachablemachine.withgoogle.com/models/z8ceXdsVg/"
model, labelContainer, maxPredictions = None, None, None

def init():
    global model, labelContainer, maxPredictions
    modelURL = URL + "model.json"
    metadataURL = URL + "metadata.json"
    download_file(modelURL, "model.json")
    download_file(metadataURL, "metadata.json")
    model = tf.keras.models.load_model("model.json")
    maxPredictions = model.output_shape[1]
    labelContainer = np.zeros((maxPredictions, 1))
    image_path = "templates/japanese.jpg"  # Replace with the actual image path
    handleImageUpload(image_path)

def predict(image):
    if model:
        prediction = model.predict(image)
        print(prediction[0].round(2))
        for i in range(maxPredictions):
            classPrediction = f"{i}: {prediction[0][i].round(2)}"
            labelContainer[i] = classPrediction

def handleImageUpload(image_path):
    image = cv2.imread(image_path)
    image = cv2.resize(image, (224, 224))
    image = np.expand_dims(image, axis=0)
    predict(image)

def download_file(url, filename):
    urllib.request.urlretrieve(url, filename)

# Trigger the initialization and prediction process
init()
