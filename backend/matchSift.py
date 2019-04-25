import numpy as np
import cv2
from matplotlib import pyplot as plt
import urllib.request
import configparser

config = configparser.ConfigParser()
config.read('conf.ini')

def uniqueMatchSift(params):

    img1 = cv2.imread(config['paths']['frontend-path']+params.get('url1'), 0)
    img2 = cv2.imread(config['paths']['frontend-path']+params.get('url2'), 0)

    orb = cv2.ORB_create()

    kp1 = orb.detect(img1,None)
    kp1, des1 = orb.compute(img1, kp1)

    kp2 = orb.detect(img2,None)
    kp2, des2 = orb.compute(img2, kp2)

    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(des1,des2)
    matches = sorted(matches, key = lambda x:x.distance)

    good = []
    for m in matches:
        if m.distance < float(params.get('sensibility'))*100:
            good.append(m)

    draw_params = dict(matchColor = (0,255,0), # draw matches in green color
                    singlePointColor = None,
                    matchesMask = None, # draw only inliers
                    flags = 2)

    # # Draw first 10 matches.
    img3 = cv2.drawMatches(img1,kp1,img2,kp2,good[:int(params.get('min_match_count'))], None,**draw_params)

    plt.imshow(img3)
    plt.savefig(config['paths']['frontend-path']+config['paths']['tmp-path']+'match.png')

    return config['paths']['tmp-path']+'match.png'