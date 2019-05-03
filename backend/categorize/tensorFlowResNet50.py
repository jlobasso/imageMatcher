from tensorflow import keras
from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions
import numpy as np
from function.searchRepo import * 

model = ResNet50(weights='imagenet')

images = getImages('download')

differentCategories = []

for x in range(0, len(images)):

    img_path = images[x]
    img = image.load_img(img_path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)

    preds = model.predict(x)
    # decode the results into a list of tuples (class, description, probability)
    # (one such list for each sample in the batch)
    # print('Predicted:', decode_predictions(preds, top=3)[0][0])
    # Predicted: [(u'n02504013', u'
    it = decode_predictions(preds, top=3)
    item = it[0][0][1]
    per = it[0][0][2]

    if item not in differentCategories and per > 0.5:
        differentCategories.append(item)

print(differentCategories)