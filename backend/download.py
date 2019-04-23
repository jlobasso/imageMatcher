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

    for ximg in images:
        try:
            archivoDescargar = urllib.request.urlopen(ximg['url'], timeout=10)
            ficheroGuardar = open(config['paths']['storage-full-path']+collection+'/'+ximg['imageId']+".jpg","wb")
            ficheroGuardar.write(archivoDescargar.read())
            ficheroGuardar.close()
        except urllib.request.URLError:
            print("Salteamos la imagen y continuamos")
            continue
        
        db[collection].update({ "imageId" : ximg['imageId']  },{ "$set": { "downloaded" : True } })
        
    elapsed = time.time() - now        
    print ('tiempo de descarga total de archivos: ',elapsed)




def insertImage(data):   


    print(data)

    kindOfStorage = data['kindOfStorage'] 
    storageData = data['storageData']
    storageName = data['storageName']

    print("Cantidad de imagenes a insertar en la base de datos: "+str(len(storageData)))

    conn = MongoClient()
    db = conn.imageMatcher
    collection = kindOfStorage+"-"+storageName
    images = db[collection].find({},{"imageId": 1})

    for storagePosition in range(0, len(storageData)-1):     
        for imagePosition in range(0, len(storageData[storagePosition]['images'])):

            exist = db[collection].find({"imageId":storageData[storagePosition]['images'][imagePosition]['imageId'], "sellerId":storageData[storagePosition]['sellerId']}).count()

            if not exist:

                rec = {} 
                rec['imageId'] = storageData[storagePosition]['images'][imagePosition]['imageId']
                rec['url'] = storageData[storagePosition]['images'][imagePosition]['url']
                rec['categoryId'] = storageData[storagePosition]['categoryId']
                rec['articleId'] = storageData[storagePosition]['articleId']
                rec['title'] = storageData[storagePosition]['title']
                rec['link'] = storageData[storagePosition]['link']
                rec['sellerId'] = storageData[storagePosition]['sellerId']
                rec['downloaded'] = False
                rec['compare'] = True
                rec['categorized'] = False

                db[collection].insert(rec, w=0)
                

    downloadImage(collection)



