import numpy as np
import cv2
from matplotlib import pyplot as plt
import matplotlib.image as mpimg

MIN_MATCH_COUNT = 100

img1 = cv2.imread('images/n0p2.jpeg',0) 
bestMatches = []

for x in range(1, 28):

    img2 = cv2.imread('images/n'+str(x)+'.jpeg',0)
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
        if m.distance < 0.7*n.distance:
            good.append(m)

    if len(good)>MIN_MATCH_COUNT:
        src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
        dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)

        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
        matchesMask = mask.ravel().tolist()

        h,w = img1.shape
        pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
        dst = cv2.perspectiveTransform(pts,M)

        img2 = cv2.polylines(img2,[np.int32(dst)],True,255,3, cv2.LINE_AA)

    else:
        
        matchesMask = None

    bestMatches.append({'image': str(x), 'percentage': str(len(good)/MIN_MATCH_COUNT*100)})

def extract(json):
    try:        
        return float(json['percentage'])
    except KeyError:
        return 0

bestMatches.sort(key=extract, reverse=True)

fig=plt.figure(figsize=(8, 8))
columns = 7
rows = 4
for x in range(1, 28):
    imgMatch = cv2.imread('images/n'+str(bestMatches[x-1]['image'])+'.jpeg',0) 
    fig.add_subplot(rows, columns, x)
    plt.axis("off")
    plt.title(str(round(float(bestMatches[x-1]['percentage']), 2))+'%')
    plt.text(50,10, 'n' + bestMatches[x-1]['image'] + '.jpeg')
     
    plt.imshow(imgMatch, 'gray')
plt.show()
cv2.destroyAllWindows()