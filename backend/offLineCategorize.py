import numpy as np
import cv2
import json
from pymongo import MongoClient
import configparser
import datetime
import time
import json
from tensorflow import keras
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input, decode_predictions

config = configparser.ConfigParser()
config.read('conf.ini')

conn = MongoClient()
db = conn.imageMatcher


def process_image(img_path, size=224):
    img = image.load_img(img_path, target_size=(size, size))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    pImg = preprocess_input(img_array)
    return pImg

start = time.time()

model = MobileNetV2(weights='imagenet')

collections = db.downloadStatus.distinct("collection")

for collection in collections:

    notCategorizedFiles = db[collection].find({'downloaded': True, 'categorized':False})
    
    predictions = []
    predictionsWeight = {}

    totalAmountToAnalize = notCategorizedFiles.count()
    newPath = config['paths']['storage-full-path']+collection

    print("Cantidad de Imagenes a analizar: ", totalAmountToAnalize)

    for notCategorizedFile in notCategorizedFiles:

        imageName = notCategorizedFile['imageName']

        try:
            pImg = process_image(newPath+"/"+imageName)
        except:
            continue

        features = model.predict(pImg)

        decoded = decode_predictions(features, top=5)
        readableCategories = []   

        for cat in decoded[0]:
            readableCategories.append({'category':cat[1], 'accuracy': str(cat[2]), 'idCategory': cat[0]})



        db[collection].update_one({"_id": notCategorizedFile['_id']}, {
                              "$set": {"categorized": True, "category": decoded[0][0][1], "categories": readableCategories}})