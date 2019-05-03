import cv2

def imageToHash(path):

    img = cv2.imread(path)
    hist = cv2.calcHist([img],[0],None,[256],[0,256])
    hist.flags.writeable = False

    imageHash = hash(str(hist))

    return imageHash