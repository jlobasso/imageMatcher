import numpy as np
import cv2
import urllib.request
import time
import json
from pymongo import MongoClient
from threading import Timer

conn = MongoClient()
db = conn.imageMatcher

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

def downloadImage():

    now = time.time()  

    images = db.download_live_search.find({"downloaded":False})

    for x in range(0, images.count()):

        try:
            archivoDescargar = urllib.request.urlopen(images[x]['url'], timeout=10)
            ficheroGuardar = open('../frontend/repo/joico/download/'+images[x]['imageId']+'.jpg',"wb")
            ficheroGuardar.write(archivoDescargar.read())
            ficheroGuardar.close()
        except urllib.request.URLError:
            print("Salteamos la imagen y continuamos")
            continue
            # r = Timer(600.0, downloadImage)
            # r.start()
        
        img = cv2.imread('../frontend/repo/joico/download/'+images[x]['imageId'], 0)
        # img = json.dumps(img, cls=NumpyEncoder)
        db.download_live_search.update({ "imageId" : images[x]['imageId']  },{ "$set": { "downloaded" : True } })
        print(db.download_live_search.find({"downloaded":True}).count())

    elapsed = time.time() - now        
    print ('tiempo de descarga total de archivos: ',elapsed)


def insertImage(data):   

    collection = db.download_live_search
    images = db.download_live_search.find({},{"imageId": 1})

    for x in range(0, len(data)):      

        for y in range(0, len(data[x]['images'])):

            print(data[x]['images'][y]['imageId'])
            print(data[x]['sellerId'])

            exist = db.download_live_search.find({"imageId":data[x]['images'][y]['imageId'], "sellerId":data[x]['sellerId']}).count()
            
            if not exist:

                rec = {} 
                rec['imageId'] = data[x]['images'][y]['imageId']
                rec['url'] = data[x]['images'][y]['url']
                rec['categoryId'] = data[x]['categoryId']
                rec['articleId'] = data[x]['articleId']
                rec['title'] = data[x]['title']
                rec['link'] = data[x]['link']
                rec['sellerId'] = data[x]['sellerId']
                rec['downloaded'] = False
                rec['compare'] = True

                collection.insert(rec)                

    downloadImage()



