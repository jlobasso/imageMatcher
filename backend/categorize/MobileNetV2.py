from tensorflow import keras
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input, decode_predictions

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import time
import json

from pymongo import MongoClient
conn = MongoClient()
db = conn.imageMatcher

start = time.time()

# process an image to be mobilenet friendly
def process_image(img_path,size = 224):
  img = image.load_img(img_path, target_size=(size, size))
  img_array = image.img_to_array(img)
  img_array = np.expand_dims(img_array, axis=0)
  pImg = preprocess_input(img_array)
  return pImg

model = MobileNetV2(weights='imagenet')

predictions = []
predictionsWeight = {}

test_img_path = '/home/andres/Documents/PRUEBAS/imageMatcher/frontend/storage/suspected-autos1/1f8f83d2248aa6771ec71f133e1414bc23bf0c252c02150cd7d5a3ebe9a7c44f.jpg'


pImg = process_image(test_img_path)

features = model.predict(pImg)

decoded = decode_predictions(features, top=5)

readableCategories = []


for cat in decoded[0]:
  # print(cat)
  readableCategories.append({'category':cat[1], 'accuracy': str(cat[2]), 'idCategory': cat[0]})

print(readableCategories)

db.aaaprueba.insert_one({"campo":readableCategories})
