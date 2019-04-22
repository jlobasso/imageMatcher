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

def downloadImage():

    conn = MongoClient()
    db = conn.imageMatcher
    now = time.time()  
    images = db.download_live_search.find({ 'downloaded': False })

    print("Imagenes por bajar:"+str(images.count()))

    for x in images:
        try:
            archivoDescargar = urllib.request.urlopen(x['url'], timeout=10)
            ficheroGuardar = open(config['paths']['frontend-path']+"repo/joico/download/"+x['imageId']+".jpg","wb")
            ficheroGuardar.write(archivoDescargar.read())
            ficheroGuardar.close()
        except urllib.request.URLError:
            print("Salteamos la imagen y continuamos")
            continue
        
        db.download_live_search.update({ "imageId" : x['imageId']  },{ "$set": { "downloaded" : True } })
        
    elapsed = time.time() - now        
    print ('tiempo de descarga total de archivos: ',elapsed)




def insertImage(data):   

    print("Cantidad de imagenes a insertar en la base de datos: "+str(len(data)))

    conn = MongoClient()
    db = conn.imageMatcher
    collection = db.download_live_search
    images = db.download_live_search.find({},{"imageId": 1})

    for x in range(0, len(data)-1):     
        for y in range(0, len(data[x]['images'])):

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
                rec['categorized'] = False

                collection.insert(rec, w=0)
                

    downloadImage()



