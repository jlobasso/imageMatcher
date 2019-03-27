import numpy as np
import cv2
from matplotlib import pyplot as plt

MIN_MATCH_COUNT = 80

img1 = cv2.resize(cv2.imread('images/n0p1.jpeg',0), (200, 200)) 

img2 = cv2.resize(cv2.imread('images/n49.jpeg',0) , (200, 200)) 

# Initiate SIFT detector
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
    if m.distance < 0.6*n.distance:
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

# print  (len(good),MIN_MATCH_COUNT)
# print  (len(good)/MIN_MATCH_COUNT) 
    

draw_params = dict(matchColor = (0,255,0), # draw matches in green color
                #    singlePointColor = None,
                   matchesMask = matchesMask, # draw only inliers
                   flags = 4)

img3 = cv2.drawMatches(img1,kp1,img2,kp2,good,None,**draw_params)
plt.axis("off")
plt.title(str(round(float(len(good)/MIN_MATCH_COUNT), 2))+'%', size = 'small', color = 'g')
plt.text(0,0, 'n' + str(img2) + '.jpeg ', size = 'small', color = 'b')
        



hsv = cv2.cvtColor(img3, cv2.COLOR_BGR2HSV)


#Rango de colores detectados:
#Verdes:
verde_bajos = np.array([49,50,50])
verde_altos = np.array([107, 255, 255])

#Azules:
azul_bajos = np.array([100,65,75], dtype=np.uint8)
azul_altos = np.array([130, 255, 255], dtype=np.uint8)


#Rojos:
rojo_bajos1 = np.array([0,65,75], dtype=np.uint8)
rojo_altos1 = np.array([12, 255, 255], dtype=np.uint8)
rojo_bajos2 = np.array([240,65,75], dtype=np.uint8)
rojo_altos2 = np.array([256, 255, 255], dtype=np.uint8)

#Crear las mascaras
mascara_verde = cv2.inRange(hsv, verde_bajos, verde_altos)
mascara_rojo1 = cv2.inRange(hsv, rojo_bajos1, rojo_altos1)
mascara_rojo2 = cv2.inRange(hsv, rojo_bajos2, rojo_altos2)
mascara_azul = cv2.inRange(hsv, azul_bajos, azul_altos)

#Juntar todas las mascaras
mask = cv2.add(mascara_rojo1, mascara_rojo2)
mask = cv2.add(mask, mascara_verde)
mask = cv2.add(mask, mascara_azul)

#Mostrar la mascara final y la imagen
cv2.imshow('Finale', mask)
cv2.imshow('Imagen', img3)

 #Salir con ESC
while(1):
    tecla = cv2.waitKey(5) & 0xFF
    if tecla == 27:
        break
 
cv2.destroyAllWindows()

# plt.imshow(img3, 'gray'),plt.show()


cv2.destroyAllWindows()