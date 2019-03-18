import cv2

img = cv2.imread('images/n1.jpeg')
hist = cv2.calcHist([img],[0],None,[256],[0,256])


for x in range(1, 14):
    img2 = cv2.imread('images/n'+str(x)+'.jpeg')
    hist2 = cv2.calcHist([img2],[0],None,[256],[0,256])
    a = cv2.compareHist(hist,hist2,cv2.HISTCMP_CORREL)
    b = cv2.compareHist(hist,hist2,cv2.HISTCMP_CHISQR/ cv2.HISTCMP_CHISQR_ALT)
    c = cv2.compareHist(hist,hist2,cv2.HISTCMP_INTERSECT)
    d = cv2.compareHist(hist,hist2,cv2.HISTCMP_BHATTACHARYYA)
    print a
    print b
    print c
    print d
    print "--------------------------"