import numpy as np
import cv2
import urllib.request
import time
import json
from pymongo import MongoClient
from threading import Timer
import configparser

config = configparser.ConfigParser()
config.read('conf.ini')


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

def downloadImage(collection):

    conn = MongoClient()
    db = conn.imageMatcher
    now = time.time()  
    images = db[collection].find({ 'downloaded': False })

    print("Imagenes por bajar:"+str(images.count()))

    for x in images:
        try:
            archivoDescargar = urllib.request.urlopen(x['url'], timeout=10)
            ficheroGuardar = open(config['paths']['frontend-path']+collection+x['imageId']+".jpg","wb")
            ficheroGuardar.write(archivoDescargar.read())
            ficheroGuardar.close()
        except urllib.request.URLError:
            print("Salteamos la imagen y continuamos")
            continue
        
        db[collection].update({ "imageId" : x['imageId']  },{ "$set": { "downloaded" : True } })
        
    elapsed = time.time() - now        
    print ('tiempo de descarga total de archivos: ',elapsed)




def insertImage(data):   


    kindOfStorage = data['kindOfStorage'] 
    storageData = data['storageData']
    storageName = data['storageName']

    print("Cantidad de imagenes a insertar en la base de datos: "+str(len(storageData)))

    conn = MongoClient()
    db = conn.imageMatcher
    collection = kindOfStorage+"-"+storageName
    images = db[collection].find({},{"imageId": 1})

    for x in range(0, len(storageData)-1):     
        for y in range(0, len(storageData[x]['images'])):

            exist = db[collection].find({"imageId":storageData[x]['images'][y]['imageId'], "sellerId":storageData[x]['sellerId']}).count()

            if not exist:

                rec = {} 
                rec['imageId'] = storageData[x]['images'][y]['imageId']
                rec['url'] = storageData[x]['images'][y]['url']
                rec['categoryId'] = storageData[x]['categoryId']
                rec['articleId'] = storageData[x]['articleId']
                rec['title'] = storageData[x]['title']
                rec['link'] = storageData[x]['link']
                rec['sellerId'] = storageData[x]['sellerId']
                rec['downloaded'] = False
                rec['compare'] = True
                rec['categorized'] = False

                db[collection].insert(rec, w=0)
                

    downloadImage(collection)



