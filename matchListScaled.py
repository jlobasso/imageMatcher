import numpy as np
import cv2
from matplotlib import pyplot as plt
import matplotlib.image as mpimg

MIN_MATCH_COUNT = 80

img1 = cv2.imread('images/n0p5.jpeg',0) 
img1 = cv2.resize(img1, (200, 200)) 

bestMatches = []

for x in range(1, 62):

    img2 = cv2.imread('images/n'+str(x)+'.jpeg',0)
    
    img2 = cv2.resize(img2, (200, 200)) 

    sift = cv2.xfeatures2d.SIFT_create()

    kp1, des1 = sift.detectAndCompute(img1,None)
    kp2, des2 = sift.detectAndCompute(img2,None)

    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks = 50)

    flann = cv2.FlannBasedMatcher(index_params, search_params)

    matches = flann.knnMatch(des1,des2,k=2)

    good = []
    for m,n in matches:
        if m.distance < 0.6*n.distance:
            good.append(m)

    bestMatches.append({'image': str(x), 'percentage': str(len(good)/MIN_MATCH_COUNT*100)})

def extract(json):
    try:        
        return float(json['percentage'])
    except KeyError:
        return 0

bestMatches.sort(key=extract, reverse=True)

fig=plt.figure(figsize=(8, 8))
columns = 4
rows = 10
for x in range(1, 62):
    if float(bestMatches[x-1]['percentage']) > float(0):
        imgMatch = cv2.imread('images/n'+str(bestMatches[x-1]['image'])+'.jpeg',0) 
        fig.add_subplot(rows, columns, x)
        plt.axis("off")
        # plt.title(str(round(float(bestMatches[x-1]['percentage']), 2))+'%', size = 'small', color = 'g')
        plt.text(0,0, 'n' + bestMatches[x-1]['image'] + ' - ' + str(round(float(bestMatches[x-1]['percentage']), 2))+'%',  size = 'small', color = 'b')
        
        plt.imshow(imgMatch, 'gray')

plt.show()
cv2.destroyAllWindows()