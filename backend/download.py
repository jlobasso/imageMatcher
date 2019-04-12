import numpy as np
import cv2
import urllib.request
import time
import json
from pymongo import MongoClient
from threading import Timer

conn = MongoClient()

db = conn.imageMatcher

def downloadImage():

    now = time.time()  

    images = db.local_live_search.find({"downloaded":False})

    for x in range(0, images.count()):

        try:
            archivoDescargar = urllib.request.urlopen(images[x]['url'], timeout=5)
            ficheroGuardar = open('../frontend/repo/joico/download/'+images[x]['imageId'],"wb")
            ficheroGuardar.write(archivoDescargar.read())
            ficheroGuardar.close()
        except urllib.request.URLError:
            print("Waiting...")
            r = Timer(600.0, downloadImage)
            r.start()
        
        img = cv2.imread('../frontend/repo/joico/download/'+images[x]['imageId'], 0)
        db.local_live_search.update_one({ "imageId" : images[x]['imageId']  },{ "$set": { "downloaded" : True, "arrImg":img } })
        print(db.local_live_search.find({"downloaded":True}).count())

    elapsed = time.time() - now        
    print ('tiempo de descarga total de archivos: ',elapsed)




def insertImage(data):   

    collection = db.local_live_search
    images = db.local_live_search.find({},{"imageId": 1})

    for x in range(0, len(data)):      


        for y in range(0, len(data[x]['images'])):

            exist = db.local_live_search.find({"imageId":data[x]['images'][y]['imageId'], "sellerId":data[x]['sellerId']}).count()
            
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

                collection.insert_one(rec)
                

    downloadImage()



