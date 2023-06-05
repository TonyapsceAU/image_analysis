#From AI: https://www.codeconvert.ai/javascript-to-python-converter

import tensorflow as tf
import numpy as np
import cv2

URL = "https://teachablemachine.withgoogle.com/models/z8ceXdsVg/"
model, labelContainer, maxPredictions = None, None, None

async def init(event):
    global model, labelContainer, maxPredictions
    modelURL = URL + "model.json"
    metadataURL = URL + "metadata.json"
    model = tf.keras.models.load_model(modelURL)
    maxPredictions = model.output_shape[1]
    labelContainer = np.zeros((maxPredictions, 1))
    image_path = "templates/japanese.jpg"  # Replace with the actual image path
    handleImageUpload(image_path)

async def predict(image):
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
