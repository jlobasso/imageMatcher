import numpy as np
import cv2
from matplotlib import pyplot as plt
import matplotlib.image as mpimg
import urllib.request
from function.searchRepo import * 
from json import dumps
import json


def url_to_image(url):
    resp = urllib.request.urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    return image

def match(images, minMatchCount, scale, sensibility, minPercentMatch, compareCategory):
    images2 = getImages(compareCategory)
    images = getImages('imgAnuncio')
    len2 = len(images2)
    globalMatches = []

    kInageComputed = 0

    orb = cv2.ORB_create()


    #Recorre imagenes de livesearch
    for x in range(0, len(images)):
        bestMatches = []
        
        # img1 = url_to_image(images[x]['image'])
        img1 = cv2.imread(images[x], 0)

        kp1 = orb.detect(img1,None)
        kp1, des1 = orb.compute(img1, kp1)

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

            kp2 = orb.detect(img2,None)
            kp2, des2 = orb.compute(img2, kp2)

            bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

            matches = bf.match(des1,des2)

            # Sort them in the order of their distance.
            matches = sorted(matches, key = lambda x:x.distance)

            good = []
            for m in matches:
                if m.distance < sensibility*100:
                        good.append(m)


            if float(len(good)/minMatchCount*100) > float(minPercentMatch):
                bestMatches.append(
                    {
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
            # print(bestMatches)
            globalMatches.append(bestMatches)

    return {'matches': globalMatches, 'imagenes1': len(images), 'imagenes2': len2}

