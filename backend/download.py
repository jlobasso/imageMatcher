import numpy as np
import cv2
import os
import urllib.request
import time
import json
from pymongo import MongoClient
from threading import Timer
import configparser
from categorize import *


config = configparser.ConfigParser()
config.read('conf.ini')


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

def downloadImage(collection, kindOfStorage):

    conn = MongoClient()
    db = conn.imageMatcher
    now = time.time()  
    images = db[collection].find({ 'downloaded': False })

    print("Imagenes por bajar:"+str(images.count()))

    newPath = config['paths']['storage-full-path']+collection

    if not os.path.exists(newPath):
        os.mkdir(newPath)

    for ximg in images:

        try:
            archivoDescargar = urllib.request.urlopen(ximg['url'], timeout=10)
            ficheroGuardar = open(newPath+'/'+ximg['imageName'],"wb")
            ficheroGuardar.write(archivoDescargar.read())
            ficheroGuardar.close()
        except urllib.request.URLError:
            print("Salteamos la imagen y continuamos")
            continue
        
        db[collection].update({ "imageId" : ximg['imageId']  },{ "$set": { "downloaded" : True } })
        
    elapsed = time.time() - now        
    print ('tiempo de descarga total de archivos: ',elapsed)

    categorize(collection, kindOfStorage)


def insertImage(data):   

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

            imageName = storageData[storagePosition]['images'][imagePosition]['url'].split("/")
            imageName = imageName[len(imageName)-1]

            exist = db[collection].find({"imageId":storageData[storagePosition]['images'][imagePosition]['imageId'], "sellerId":storageData[storagePosition]['sellerId']}).count()

            if not exist:

                rec = {} 
                rec['imageId'] = storageData[storagePosition]['images'][imagePosition]['imageId']
                rec['imageName'] = imageName
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
                

    downloadImage(collection, kindOfStorage)



