import numpy as np
import cv2
from matplotlib import pyplot as plt

# img1 = cv2.imread('../frontend/repo/joico/Tratamento/Original/Joi-0079.jpg',0)
# img2 = cv2.imread('../frontend/repo/joico/Tratamento/Original/CE_TreatmentMasque_500ml_Joi-0210.jpg', 0)

# Initiate STAR detector
orb = cv2.ORB_create()

# print(help(orb.detect))
kp1 = orb.detect(img1,None)
kp1, des1 = orb.compute(img1, kp1)

kp2 = orb.detect(img2,None)
kp2, des2 = orb.compute(img2, kp2)

bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

# Match descriptors.
matches = bf.match(des1,des2)


# Sort them in the order of their distance.
matches = sorted(matches, key = lambda x:x.distance)

good = []
for m in matches:
    if m.distance < 20:
        good.append(m)


print(len(good))        

matchesMask = None

draw_params = dict(matchColor = (0,255,0), # draw matches in green color
                   singlePointColor = None,
                   matchesMask = matchesMask, # draw only inliers
                   flags = 2)


# Draw first 10 matches.
img3 = cv2.drawMatches(img1,kp1,img2,kp2,good[:30], None,**draw_params)

plt.imshow(img3),plt.show()