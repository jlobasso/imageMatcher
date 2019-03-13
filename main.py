import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt

img1 = cv.imread('Nike-Air-Force-1-Low-Moto-W-1100x553.png',0) # queryImage
img2 = cv.imread('nike-air-force-1-dominican-republic-de-lo-mio-release-date-2.jpg',0) # trainImage

# # Initiate ORB detector
# orb = cv.ORB_create()
# # find the keypoints and descriptors with ORB
# kp1, des1 = orb.detectAndCompute(img1,None)
# kp2, des2 = orb.detectAndCompute(img2,None)


# Initiate SIFT detector
sift = cv.SIFT()

# sift = cv.xfeatures2d.SIFT_create()
# sift = cv.SIFT_create()
# find the keypoints and descriptors with SIFT
kp1, des1 = sift.detectAndCompute(img1,None)
kp2, des2 = sift.detectAndCompute(img2,None)


# # create BFMatcher object
# # NORM_L1
# # NORM_L2
# # NORM_HAMMING
# # NORM_HAMMING2
# bf = cv.BFMatcher(cv.NORM_HAMMING, crossCheck=True)

# BFMatcher with default params
bf = cv.BFMatcher()
matches = bf.knnMatch(des1,des2, k=2)

# # Match descriptors.
# # matches = bf.knnMatch(des1,des2, k=2)
# matches = bf.match(des1,des2)
# # matches = sorted(matches, key = lambda x:x.distance)

# # Sort them in the order of their distance.
# matches = sorted(matches, key = lambda x:x.distance)
# # print(len(matches))

# # Draw first 10 matches.
# img3 = cv.drawMatches(img1,kp1,img2,kp2,matches[:10],None, flags=2)
# plt.imshow(img3),plt.show()

# BFMatcher with default params
bf = cv.BFMatcher()
matches = bf.knnMatch(des1,des2, k=2)
# Apply ratio test
good = []
for m,n in matches:
    if m.distance < 0.75*n.distance:
        good.append([m])
# cv.drawMatchesKnn expects list of lists as matches.
img3 = cv.drawMatchesKnn(img1,kp1,img2,kp2,good,flags=2)
plt.imshow(img3),plt.show()
