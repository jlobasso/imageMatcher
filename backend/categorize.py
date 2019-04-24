from tensorflow import keras
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input, decode_predictions

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import time
from pymongo import MongoClient
import configparser

config = configparser.ConfigParser()
config.read('conf.ini')


# process an image to be mobilenet friendly
def process_image(img_path,size = 224):
  img = image.load_img(img_path, target_size=(size, size))
  img_array = image.img_to_array(img)
  img_array = np.expand_dims(img_array, axis=0)
  pImg = preprocess_input(img_array)
  return pImg

model = MobileNetV2(weights='imagenet')

def categorize(collection):
    start = time.time()
    conn = MongoClient()
    db = conn.imageMatcher
    images = db[collection].find({ 'downloaded': True, 'categorized': False })

    predictions = []
    predictionsWeight = {}

    totalAmountToAnalize = images.count()
    newPath = config['paths']['storage-full-path']+collection

    print("Cantidad de Imagenes a analizar: ", totalAmountToAnalize)

    for test_img_path in images:
      imageName = test_img_path['imageName'] #.encode('ascii', 'ignore').decode('ascii')
      pImg = process_image(newPath+"/"+imageName)

      features = model.predict(pImg)

      decoded = decode_predictions(features, top=1)

      db[collection].update({ "imageId" : test_img_path['imageId']  },{ "$set": { "categorized" : True, "category": decoded[0][0][1]} })

      if str(decoded[0][0][1]) not in predictions:
          predictions.append(str(decoded[0][0][1]))
          predictionsWeight[str(decoded[0][0][1])] = 1
      else:
          predictionsWeight[str(decoded[0][0][1])] = predictionsWeight[str(decoded[0][0][1])] + 1

    print(predictionsWeight) 
    db.groupCategories.insert({'group':collection,'predictionsWeight':predictionsWeight}, w=0)       
    end = time.time()
    eachImageTime = (end - start)/totalAmountToAnalize 
    print("Tiempo total (segundos): ", end - start)
    print("Tiempo por cada imagen (segundos): ", eachImageTime)
    print("Tiempo por cada 1k imagenes (segundos): ", eachImageTime*1000)
    print("Tiempo por cada 10k imagenes (minutos): ", eachImageTime*10000/60)

# categorize()