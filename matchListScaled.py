import numpy as np
import cv2
from matplotlib import pyplot as plt
import matplotlib.image as mpimg
import urllib.request
from imgDir import * 

MIN_MATCH_COUNT = 80
SCALE = 200
SENSIBILITY = 0.6
MINPERCENTMATCH = 40


def url_to_image(url):
    resp = urllib.request.urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    return image


def match(images):

    images2 = getImages()
    len2 = len(images2)
    globalMatches = []

    #Recorre imagenes de livesearch
    for x in range(0, len(images)):
        bestMatches = []
        img1 = cv2.resize(url_to_image(images[x]['image']), (200, 200))

        # recorre las imagenes originales del repo local
        for y in range(0, len2):
            img2 = cv2.resize(cv2.imread(images2[y], 0), (200, 200))

            sift = cv2.xfeatures2d.SIFT_create()

            kp1, des1 = sift.detectAndCompute(img1, None)
            kp2, des2 = sift.detectAndCompute(img2, None)

            FLANN_INDEX_KDTREE = 0
            index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
            search_params = dict(checks=50)

            flann = cv2.FlannBasedMatcher(index_params, search_params)

            matches = flann.knnMatch(des1, des2, k=2)

            good = []
            for m, n in matches:
                if m.distance < 0.6*n.distance:
                    good.append(m)


            if float(len(good)/MIN_MATCH_COUNT*100) > float(20):

                bestMatches.append(
                    {
                        'image_url': str(images[x]['image']), 
                        'percentage': str(len(good)/MIN_MATCH_COUNT*100),
                        'image_repo': str(images2[y]), 

                    })

        

            def extract(json):
                try:
                    return float(json['percentage'])
                except KeyError:
                    return 0

            bestMatches.sort(key=extract, reverse=True)
            
        if len(bestMatches) > 0:
            globalMatches.append(bestMatches)


    return globalMatches


#     fig=plt.figure(figsize=(8, 8))
#     columns = 4
#     rows = 10
#     for x in range(1, 65):
#             if float(bestMatches[x-1]['percentage']) > float(0):
#                     imgMatch = cv2.imread('images/n'+str(bestMatches[x-1]['image'])+'.jpeg',0)
#                     fig.add_subplot(rows, columns, x)
#                     plt.axis("off")
#                     # plt.title(str(round(float(bestMatches[x-1]['percentage']), 2))+'%', size = 'small', color = 'g')
#                     plt.text(0,0, 'n' + bestMatches[x-1]['image'] + ' - ' + str(round(float(bestMatches[x-1]['percentage']), 2))+'%',  size = 'small', color = 'b')

#                     plt.imshow(imgMatch, 'gray')

#     plt.show()
#     cv2.destroyAllWindows()

