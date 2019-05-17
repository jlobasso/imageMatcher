from pymongo import MongoClient
import urllib.request
import configparser
import base64

config = configparser.ConfigParser()
config.read('conf.ini')

conn = MongoClient()
db = conn.imageMatcher

collections = db.downloadStatus.distinct("collection")

for collection in collections:
    
    notDownloadedFiles = db[collection].find({'downloaded':False, 'attempts': {'$lt': 4}})
    
    print("Archivos pendientes de descarga: ", notDownloadedFiles.count())
    newPath = config['paths']['storage-full-path']+collection+"/"

    for notDownloadedFile in notDownloadedFiles:
    
        print(notDownloadedFile['url'])

        try:
            if (notDownloadedFile['url'].find('http') != -1):
                req = urllib.request.Request(notDownloadedFile['url'])
                archivoDescargar = urllib.request.urlopen(req, timeout=3)
                ficheroGuardar = open(newPath+notDownloadedFile['imageName'], "wb")
                ficheroGuardar.write(archivoDescargar.read())
                ficheroGuardar.close()
            if (notDownloadedFile['url'].find('data:image') != -1):
                url = notDownloadedFile['url'].split(",")
                extension = url[0].split("/")[1].split(";")[0]
                image_binary=base64.b64decode(url[1])

                with open(newPath+notDownloadedFile['imageName'], "wb") as fh:
                   fh.write(image_binary)

                db[collection].find({'downloaded':True})

        except urllib.request.URLError:

            print(collection)

            db[collection].find({'imageName':notDownloadedFile['imageName'], '$inc': { 'attempts': 1 }})
            
            continue