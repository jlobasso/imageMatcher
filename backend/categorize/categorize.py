import numpy as np
import cv2
import json
from pymongo import MongoClient
import configparser
import datetime
import time
from tensorflow import keras
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input, decode_predictions

config = configparser.ConfigParser()
config.read('conf.ini')

conn = MongoClient()
db = conn.imageMatcher

# process an image to be mobilenet friendly


def process_image(img_path, size=224):
    img = image.load_img(img_path, target_size=(size, size))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    pImg = preprocess_input(img_array)
    return pImg


model = MobileNetV2(weights='imagenet')


def categorize(collection, kindOfStorage):
    start = time.time()
    conn = MongoClient()
    db = conn.imageMatcher
    images = db[collection].find({'downloaded': True, 'categorized': False})

    predictions = []
    predictionsWeight = {}

    totalAmountToAnalize = images.count()
    newPath = config['paths']['storage-full-path']+collection

    print("Cantidad de Imagenes a analizar: ", totalAmountToAnalize)

    for test_img_path in images:
        # .encode('ascii', 'ignore').decode('ascii')
        imageName = test_img_path['imageName']

        try:
            pImg = process_image(newPath+"/"+imageName)
        except:
            continue

        features = model.predict(pImg)

        decoded = decode_predictions(features, top=5)

        readableCategories = []   

        for cat in decoded[0]:
            readableCategories.append({'category':cat[1], 'accuracy': str(cat[2]), 'idCategory': cat[0]})

        db[collection].update_one({"_id": test_img_path['_id']}, {
                              "$set": {"categorized": True, "category": decoded[0][0][1], "categories":readableCategories}})

        if str(decoded[0][0][1]) not in predictions:
            predictions.append(str(decoded[0][0][1]))
            predictionsWeight[str(decoded[0][0][1])] = 1
        else:
            predictionsWeight[str(decoded[0][0][1])] = predictionsWeight[str(
                decoded[0][0][1])] + 1

    print(predictionsWeight)

    predictionsWeight = sorted(
        predictionsWeight.items(), key=lambda kv: kv[1], reverse=True)

    for i in range(len(predictionsWeight)):
        predictionsWeight[i] = {
            predictionsWeight[i][0]: predictionsWeight[i][1]}

    db.groupCategories.insert_one({'group': collection, 'kindOfStorage': kindOfStorage,
                               'total': totalAmountToAnalize, 'predictionsWeight': predictionsWeight})
    end = time.time()
    eachImageTime = (end - start)/totalAmountToAnalize
    print("Tiempo total (segundos): ", end - start)
    print("Tiempo por cada imagen (segundos): ", eachImageTime)
    print("Tiempo por cada 1k imagenes (segundos): ", eachImageTime*1000)
    print("Tiempo por cada 10k imagenes (minutos): ", eachImageTime*10000/60)

# categorize()
