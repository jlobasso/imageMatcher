from tensorflow import keras
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input, decode_predictions

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from glob import glob
import time
start = time.time()

# process an image to be mobilenet friendly
def process_image(img_path,size = 224):
  img = image.load_img(img_path, target_size=(size, size))
  img_array = image.img_to_array(img)
  img_array = np.expand_dims(img_array, axis=0)
  pImg = preprocess_input(img_array)
  return pImg

def getImages(path):
    img = glob("repo/joico/"+path+"/*")
    return img

model = MobileNetV2(weights='imagenet')

predictions = []
predictionsWeight = {}

test_imgs_paths = getImages('download1300')
totalAmountToAnalize = len(test_imgs_paths)

print("Cantidad de Imagenes a analizar: ", totalAmountToAnalize)

for test_img_path in test_imgs_paths:

    pImg = process_image(test_img_path)

    features = model.predict(pImg)

    decoded = decode_predictions(features, top=1)

    img=mpimg.imread(test_img_path)

    if str(decoded[0][0][1]) not in predictions:
        predictions.append(str(decoded[0][0][1]))
        predictionsWeight[str(decoded[0][0][1])] = 1
    else:
        predictionsWeight[str(decoded[0][0][1])] = predictionsWeight[str(decoded[0][0][1])] + 1

print(predictionsWeight)        
end = time.time()
eachImageTime = (end - start)/totalAmountToAnalize 
print("Tiempo total (segundos): ", end - start)
print("Tiempo por cada imagen (segundos): ", eachImageTime)
print("Tiempo por cada 1k imagenes (segundos): ", eachImageTime*1000)
print("Tiempo por cada 10k imagenes (minutos): ", eachImageTime*10000/60)
