import numpy as np
import cv2
from matplotlib import pyplot as plt
import matplotlib.image as mpimg
from function.searchRepo import * 
import json
from pymongo import MongoClient
import configparser

config = configparser.ConfigParser()
config.read('conf.ini')

conn = MongoClient()
db = conn.imageMatcher
def match(minMatchCount, sensibility, minPercentMatch, storageA, storageB):
    
    imagesA = db[storageA].find()
    pathA = config['paths']['storage-full-path']+storageA+'/'

    imagesB = db[storageB].find()
    pathB = config['paths']['storage-full-path']+storageB+'/'
     
    lenA = imagesA.count()    
    lenB = imagesB.count()

    globalMatches = []
    kInageComputed = 0
    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    sift = cv2.xfeatures2d.SIFT_create()
    # orb = cv2.ORB_create()

    if lenA == 0:
        return {'matches': [], 'imagenes1': 0, 'imagenes2': 0, "status": "No hay imagenes en "+pathA}
    if lenB == 0:
        return {'matches': [], 'imagenes1': 0, 'imagenes2': 0, "status": "No hay imagenes en "+pathB}    
 
    for imgA in imagesA:
        print('AAAA')
        bestMatches = []        
        imageA = cv2.imread(pathA+imgA['imageName'], 0)
        kp1, des1 = sift.detectAndCompute(imageA, None)

        # kp1 = orb.detect(imageA,None)
        # kp1, des1 = orb.compute(imageA, kp1)        

        # recorre las imagenes originales del repo local
        imagesB = db[storageB].find()
        for imgB in imagesB:
            print('B')
            # print(imgB['imageName'].encode("ascii", "ignore").decode("ascii"))
            kInageComputed = kInageComputed + 1
            
            # print("recorriendo "+str(x+1)+" de "+str(len(images))+ " comparando con "+str(y+1)+" de "+str(len2))
            F = open(config['paths']['status-path']+"status.json","w+")

            status = {
                        "absoluteComputed": str(kInageComputed),
                        "running":{
                                    "current":str(1), 
                                    "of":str(lenA)
                                    },
                        "comparing":{
                                    "current":str(1), 
                                    "of":str(lenB)
                                    }                     
                    }            
            F.write(json.dumps(status))
            F.close()

            imageB = cv2.imread(pathB+imgB['imageName'], 0)                              
            kp2, des2 = sift.detectAndCompute(imageB, None)

            # kp2 = orb.detect(imageB,None)
            # kp2, des2 = orb.compute(imageB, kp2)

            # bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
            try:
                # matches = bf.match(des1,des2)     
                matches = flann.knnMatch(des1, des2, k=2)           
            except:
                break
                print(imgA['imageName'].encode("ascii", "ignore").decode("ascii"))
                print(imgB['imageName'].encode("ascii", "ignore").decode("ascii"))                
                  

            # good = []
            # for m in matches:
            #     if m.distance < sensibility*100:
            #         good.append(m)

            good = []
            for m, n in matches:
                if m.distance < sensibility*n.distance:
                    good.append(m)

            if float(len(good)/minMatchCount*100) > float(minPercentMatch):
                bestMatches.append(
                    {
                        'article_id_a': imgA['articleId'],
                        'title_a': imgA['title'],
                        'image_path_a': config['paths']['storage-path']+storageA+'/'+imgA['imageName'], 
                        'image_name_a': imgA['imageName'], 
                        'article_id_b': imgB['articleId'],
                        'title_b': imgB['title'],
                        'image_path_b': config['paths']['storage-path']+storageB+'/'+imgB['imageName'],
                        'image_name_b': imgB['imageName'], 
                        'percentage': str(len(good)/minMatchCount*100),

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

     
    return {'matches': globalMatches, 'imagenesA': lenA, 'imagenesB': lenB, "status":"OK"}

