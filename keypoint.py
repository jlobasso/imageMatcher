import numpy as np
import cv2 
from matplotlib import pyplot as plt


img2 = cv2.imread('images/Z6.webp',0) # trainImage
# img1 = cv2.imread('images/mochila-nike-elemental-negra-importada-original-ba5405010-D_NQ_NP_753682-MLA28367807721_102018-O.webp')
img1 = cv2.imread('images/MELI.jpeg',0) # queryImage
# img2 = cv2.imread('images/mochila-nike-elemental-negra-importada-original-ba5405010-D_NQ_NP_753682-MLA28367807721_102018-O.webp')

# Initiate ORB detector
orb = cv2.ORB_create()
# find the keypoints and descriptors with ORB
kp1, des1 = orb.detectAndCompute(img1,None)
kp2, des2 = orb.detectAndCompute(img2,None)

# create BFMatcher object

# # NORM_L1
# # NORM_L2
# # NORM_HAMMING
# # NORM_HAMMING2
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

# Match descriptors.
matches = bf.match(des1,des2)

# Sort them in the order of their distance.
matches = sorted(matches, key = lambda x:x.distance)
print(len(matches))



# Draw first 10 matches.
img3 = cv2.drawMatches(img1,kp1,img2,kp2,matches[:88],None, flags=2)
plt.imshow(img3),plt.show()


cv2.destroyAllWindows()