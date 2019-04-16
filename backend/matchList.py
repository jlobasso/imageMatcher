import numpy as np
import cv2
from matplotlib import pyplot as plt
import matplotlib.image as mpimg
import urllib.request
from function.searchRepo import * 
from json import dumps
import json
from pymongo import MongoClient

conn = MongoClient()

db = conn.imageMatcher

def url_to_image(url):
    resp = urllib.request.urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    return image

def match(images, minMatchCount, scale, sensibility, minPercentMatch, compareCategory):
   
    images2 = getImages(compareCategory)
    images = getImages('download')
    len2 = len(images2)
    globalMatches = []

    kInageComputed = 0
    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)

    sift = cv2.xfeatures2d.SIFT_create()

    #Recorre imagenes de livesearch
    for x in range(0, len(images)):
        bestMatches = []
        
        img1 = cv2.imread(images[x], 0)

        kp1, des1 = sift.detectAndCompute(img1, None)

        # recorre las imagenes originales del repo local
        for y in range(0, len2):

            kInageComputed = kInageComputed + 1
            
            print("recorriendo "+str(x+1)+" de "+str(len(images))+ " comparando con "+str(y+1)+" de "+str(len2))

            F = open("status.json","w+")

            status = {
                        "absoluteComputed": str(kInageComputed),
                        "running":{
                                    "current":str(x+1), 
                                    "of":str(len(images))
                                    },
                        "comparing":{
                                    "current":str(y+1), 
                                    "of":str(len2)
                                    }                     
                    }            
            F.write(json.dumps(status))
            F.close()


            img2 = cv2.imread(images2[y], 0)
                        
            kp2, des2 = sift.detectAndCompute(img2, None)

            matches = flann.knnMatch(des1, des2, k=2)

            good = []
            for m, n in matches:
                if m.distance < sensibility*n.distance:
                    good.append(m)

            if float(len(good)/minMatchCount*100) > float(minPercentMatch):
                bestMatches.append(
                    {
                        'article_id': db.download_live_search.find({'imageId':images[x], 'downloaded': False},{'articleId':1},
                        'title': str(db.download_live_search.find({'imageId':images[x], 'downloaded': False},{'title':1}),
                        # 'article_id': str(images[x]['id']),
                        # 'image_url': str(images[x]['image']), 
                        'image_url': str(images[x]), 
                        'percentage': str(len(good)/minMatchCount*100),
                        'image_repo': str(images2[y]), 

                    })

            imagenRecorridas = +1

            def extract(json):
                try:
                    return float(json['percentage'])
                except KeyError:
                    return 0

            bestMatches.sort(key=extract, reverse=True)
            
        if len(bestMatches) > 0:
            globalMatches.append(bestMatches)

    return {'matches': globalMatches, 'imagenes1': len(images), 'imagenes2': len2}

