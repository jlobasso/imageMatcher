import numpy as np
import cv2
from matplotlib import pyplot as plt
from pymongo import MongoClient
import configparser

config = configparser.ConfigParser()
config.read('conf.ini')

conn = MongoClient()
db = conn.imageMatcher

def uniqueMatchSift(params):
    path = config['paths']['frontend-path']

    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    sift = cv2.xfeatures2d.SIFT_create()

    imageA = cv2.imread(path+params.get('url1'), 0)
    kp1, des1 = sift.detectAndCompute(imageA, None) 
    imageB = cv2.imread(path+params.get('url2'), 0)                              
    kp2, des2 = sift.detectAndCompute(imageB, None)

    matches = flann.knnMatch(des1, des2, k=2)  

    good = []
    for m, n in matches:
        if m.distance < float(params.get('sensibility'))*n.distance:
            good.append(m)    


    draw_params = dict(matchColor = (0,255,0), # draw matches in green color
                    singlePointColor = None,
                    matchesMask = None, # draw only inliers
                    flags = 2)

    img3 = cv2.drawMatches(imageA,kp1,imageB,kp2,good[:int(params.get('min_match_count'))], None,**draw_params)

    plt.imshow(img3)
    plt.savefig(config['paths']['frontend-path']+config['paths']['tmp-path']+'match.png')

    return config['paths']['tmp-path']+'match.png'