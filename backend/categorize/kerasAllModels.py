from tensorflow import keras
from tensorflow.keras.applications import VGG16, InceptionV3, ResNet50, MobileNet, MobileNetV2
# from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input, decode_predictions

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from function.searchRepo import * 
import time
start = time.time()

# process an image to be mobilenet friendly
def process_image(img_path,size = 224):
  img = image.load_img(img_path, target_size=(size, size))
  img_array = image.img_to_array(img)
  img_array = np.expand_dims(img_array, axis=0)
  pImg = preprocess_input(img_array)
  return pImg

# model1 = VGG16(weights='imagenet')
# model2 = InceptionV3(weights='imagenet') #size 299 299
# model3 = ResNet50(weights='imagenet')
model4 = MobileNetV2(weights='imagenet')
# model5 = MobileNetV2(weights='imagenet')

predictions = []
predictionsWeight = {}

test_imgs_paths = getImages('download')

for test_img_path in test_imgs_paths:

    pImg = process_image(test_img_path)
    pImg2 = process_image(test_img_path, 299)

    # features1 = model1.predict(pImg)
    # features2 = model2.predict(pImg2)
    # features3 = model3.predict(pImg)
    features4 = model4.predict(pImg)
    # features5 = model5.predict(pImg)

    # decoded1 = decode_predictions(features1, top=3)
    # print('Predicted:', decoded1)
    # decoded2 = decode_predictions(features2, top=3)
    # prediction2 = str(round(decoded2[0][0][2]*100, 2))
    # print('Predicted InceptionV3:', decoded2)

    # decoded3 = decode_predictions(features3, top=3)
    # prediction3 = str(round(decoded3[0][0][2]*100, 2))
    # print('Predicted ResNet50:', decoded3)

    decoded4 = decode_predictions(features4, top=3)
    prediction4 = str(round(decoded4[0][0][2]*100, 2))
    print('Predicted MobileNet:', decoded4)

    # decoded5 = decode_predictions(features5, top=3)
    # prediction5 = str(round(decoded5[0][0][2]*100, 2))
    # print('Predicted MobileNetV2:', decoded5)


    img=mpimg.imread(test_img_path)

    text = ""
    # text += "InceptionV3: " +str(decoded2[0][0][1]) + ": " + prediction2+"% \n"
    # text += "ResNet50: " +str(decoded3[0][0][1]) + ": " + prediction3+"% \n"
    text += "MobileNet: " +str(decoded4[0][0][1]) + ": " + prediction4+"% \n"
    # text += "MobileNeV2: " +str(decoded5[0][0][1]) + ": " + prediction5+"%"

    # plt.text(12, 53,  text, fontsize=12, bbox=dict(facecolor='white', alpha=0.6))
    # # plt.text(12, 53,  "InceptionV3: " +str(decoded2[0][0][1]) + ": " + prediction2+"%", fontsize=12, bbox=dict(facecolor='white', alpha=0.6))
    # # plt.text(12, 143, "ResNet50: " +str(decoded3[0][0][1]) + ": " + prediction3+"%", fontsize=12, bbox=dict(facecolor='white', alpha=0.6))
    # # plt.text(12, 233, "MobileNet: " +str(decoded4[0][0][1]) + ": " + prediction4+"%", fontsize=12, bbox=dict(facecolor='white', alpha=0.6))
    # # plt.text(12, 323, "MobileNeV2: " +str(decoded5[0][0][1]) + ": " + prediction5+"%", fontsize=12, bbox=dict(facecolor='white', alpha=0.6))
    # imgplot = plt.imshow(img)
    # plt.show()

    if str(decoded4[0][0][1]) not in predictions:
        predictions.append(str(decoded4[0][0][1]))
        predictionsWeight[str(decoded4[0][0][1])] = 1
    else:
        predictionsWeight[str(decoded4[0][0][1])] = predictionsWeight[str(decoded4[0][0][1])] + 1

    # if str(decoded5[0][0][1]) not in predictions:
    #     predictions.append(str(decoded5[0][0][1])) 
    #     predictionsWeight[str(decoded5[0][0][1])] = 1   
    # else:
    #     predictionsWeight[str(decoded5[0][0][1])] = predictionsWeight[str(decoded5[0][0][1])] + 1    


print(predictionsWeight)        
end = time.time()
print(end - start)