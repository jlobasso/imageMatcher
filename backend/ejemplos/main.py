import numpy as np
import cv2
from matplotlib import pyplot as plt
import urllib.request

MIN_MATCH_COUNT = 10

def url_to_image(url):
	resp = urllib.request.urlopen(url)
	image = np.asarray(bytearray(resp.read()), dtype="uint8")
	image = cv2.imdecode(image, cv2.IMREAD_COLOR)
	return image


# img1 = cv2.imread('../../frontend/repo/joico/Shampoo/Recortadas/BL_Shampoo_300ml.jpg',0) # queryImage
# img2 = url_to_image('http://mlb-s2-p.mlstatic.com/854454-MLB26525962127_122017-O.jpg') # trainImage
# img1 = cv2.imread('../frontend/repo/pruebaNike-Air-Force-1-Low-Moto-W-1100x553.png',0) # queryImage
# img2 = cv2.imread('../frontend/repo/pruebanike-air-force-1-dominican-republic-de-lo-mio-release-date-2.jpg',0) # trainImage


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

print  (len(good),MIN_MATCH_COUNT)
print  (len(good)/MIN_MATCH_COUNT) 
    

draw_params = dict(matchColor = (0,255,0), # draw matches in green color
                   singlePointColor = None,
                   matchesMask = matchesMask, # draw only inliers
                   flags = 2)

img3 = cv2.drawMatches(img1,kp1,img2,kp2,good,None,**draw_params)

plt.imshow(img3, 'gray'),plt.show()


cv2.destroyAllWindows()