import numpy as np
import cv2
from matplotlib import pyplot as plt
import matplotlib.image as mpimg

MIN_MATCH_COUNT = 80

img1 = cv2.imread('../frontend/repo/prueban0p2.jpeg',0) # queryImage
# img1 = cv2.imread('../frontend/repo/pruebaNike-Air-Force-1-Low-Moto-W-1100x553.png',0) # queryImage
# img2 = cv2.imread('../frontend/repo/pruebanike-air-force-1-dominican-republic-de-lo-mio-release-date-2.jpg',0) # trainImage

bestMatches = []

for x in range(1, 28):

    img2 = cv2.imread('../frontend/repo/prueban'+str(x)+'.jpeg',0) # trainImage

    # Initiate SIFT detector
    # sift = cv2._SIFT()
    sift = cv2.xfeatures2d.SIFT_create()

    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(img1,None)
    kp2, des2 = sift.detectAndCompute(img2,None)

    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks = 50)

    flann = cv2.FlannBasedMatcher(index_params, search_params)

    matches = flann.knnMatch(des1,des2,k=2)

    # store all the good matches as per Lowe's ratio test.
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

    # print  ('Imagen comparada: ' + str(x)) 
    # print  ('Cantidad de puntos matcheados: ' + str(len(good)) + ' de ' + str(MIN_MATCH_COUNT))
    # print  ('Porcentaje de macheo: ' + str(len(good)/MIN_MATCH_COUNT*100) + '%')
    # print  ('')    

    bestMatches.append({'image': str(x), 'percentage': str(len(good)/MIN_MATCH_COUNT*100)})

def extract(json):
    try:
        # Also convert to int since update_time will be string.  When comparing
        # strings, "10" is smaller than "2".
        return float(json['percentage'])
    except KeyError:
        return 0

# lines.sort() is more efficient than lines = lines.sorted()
bestMatches.sort(key=extract, reverse=True)

# for x in range(0, 27):
#     # print (bestMatches[x]['image'])
#     imgMatch = cv2.imread('../frontend/repo/prueban'+str(bestMatches[x]['image'])+'.jpeg',0) 
#     plt.imshow(imgMatch, 'gray')

# plt.show()

# w=10
# h=10
fig=plt.figure(figsize=(8, 8))
columns = 7
rows = 4
# for i in range(1, columns*rows +1):
for x in range(1, 28):
    # img = np.random.randint(10, size=(h,w))
    imgMatch = cv2.imread('../frontend/repo/prueban'+str(bestMatches[x-1]['image'])+'.jpeg',0) 
    fig.add_subplot(rows, columns, x)
    plt.axis("off")
    # image = mpimg.imread(imgMatch)
    # plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    # plt.imshow(image)
    plt.title(str(round(float(bestMatches[x-1]['percentage']), 2))+'%')
    plt.text(50,10, 'n' + bestMatches[x-1]['image'] + '.jpeg')
     
    plt.imshow(imgMatch, 'gray')
plt.show()
cv2.destroyAllWindows()

# print  (bestMatches) 

    # draw_params = dict(matchColor = (0,255,0), # draw matches in green color
    #                 singlePointColor = None,
    #                 matchesMask = matchesMask, # draw only inliers
    #                 flags = 2)

    # img3 = cv2.drawMatches(img1,kp1,img2,kp2,good,None,**draw_params)

    # plt.imshow(img3, 'gray'),plt.show()
