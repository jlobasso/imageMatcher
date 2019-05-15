import urllib.request
import os
from function.start import *
from categorize.categorize import *
from imageToHash import *

config = configparser.ConfigParser()
config.read('conf.ini')

conn = MongoClient()
db = conn.imageMatcher

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

def downloadImage(collection, kindOfStorage, sessionId):
    startTimeDownload = time.time()
    collDownload = 'downloadStatus'
    images = db[collection].find({ 'downloaded': False })
    count = images.count()
    errorDownload = 0
    correctDownload = 0
    urlImageError = []
    db[collDownload].insert_one({'sessionId': sessionId,
                                'collection' : collection,
                                'count' : count,
                                'correctDownload' : 0,
                                'errorDownload' : 0,
                                'timeCategorize' : 0,
                                'timeDownload' : 0,
                                'processing' : True 
                                })


    newPath = config['paths']['storage-full-path']+collection

    if not os.path.exists(newPath):
        os.mkdir(newPath)

    for ximg in images:

        try:
            req = urllib.request.Request(ximg['url'])
            req.add_header('User-Agent', 'Mozilla/5.0 (compatible; MSIE 10.0; Macintosh; Intel Mac OS X 10_7_3; Trident/6.0)')
            archivoDescargar = urllib.request.urlopen(req, timeout=3)
            ficheroGuardar = open(newPath+'/'+ximg['imageName'],"wb")
            ficheroGuardar.write(archivoDescargar.read())
            ficheroGuardar.close()
            correctDownload = correctDownload + 1
        except urllib.request.URLError:
            # print("No se pudo descargar la imagen desde "+ximg['url'])
            errorDownload = errorDownload + 1 
            urlImageError.append(ximg['url'])
            db[collDownload].update_one({ "collection" : collection },{ "$set": { "errorDownload" : errorDownload} })
            continue

        imageHash = imageToHash(newPath+'/'+ximg['imageName'])
        db[collection].update_one({ "imageId" : ximg['imageId']  },{ "$set": { "downloaded" : True, "imageHash":imageHash } })
        db[collDownload].update_one({ "collection" : collection },{ "$set": { "correctDownload" : correctDownload } })
            
    endTimeDownload = time.time()
    
    # cantidad = db[collection].find({ "downloaded" : True } ).count()
    if correctDownload > 0:
        startTimeCategorize = time.time()
        categorize(collection, kindOfStorage)
        endTimeCategorize = time.time()
        timeCategorize = round(endTimeCategorize - startTimeCategorize,2)
        timeDownload = round(endTimeDownload - startTimeDownload,2)

        db[collDownload].update_one({ "collection" : collection },{ "$set": { "timeCategorize" : timeCategorize, 'timeDownload' : timeDownload, "processing" : False } })
        
    else:
        print("No se descargaron las imagenes en el storage")

    

def insertImage(data):   

    kindOfStorage = data['kindOfStorage'] 
    storageData = data['storageData']
    storageName = data['storageName']
    sessionId = data['sessionId']

    # print("Cantidad de imagenes a insertar en la base de datos: "+str(len(storageData)))

    conn = MongoClient()
    db = conn.imageMatcher
    collection = kindOfStorage+"-"+storageName
    images = db[collection].find({},{"imageId": 1})

    for storagePosition in range(0, len(storageData)):   
        for imagePosition in range(0, len(storageData[storagePosition]['images'])):
    

            imageName = storageData[storagePosition]['images'][imagePosition]['url'].split("/")
            imageName = imageName[len(imageName)-1]

            exist = db[collection].find({"imageId":storageData[storagePosition]['images'][imagePosition]['imageId'], "sellerId":storageData[storagePosition]['sellerId']}).count()
            
            prevImage = db[collection].find_one({"imageName":imageName},{"imageId":1, '_id':0})

            # db[collection].find_one({"imageName":imageName},{"imageId":1, '_id':0})['imageId'] == 'NOT_IMG_ID'

            if not exist or (prevImage and prevImage['imageId'] == 'NOT_IMG_ID'):
                rec = {} 
                rec['imageId'] = ('NOT_IMG_ID' if storageData[storagePosition]['images'][imagePosition]['imageId']=='' else storageData[storagePosition]['images'][imagePosition]['imageId']) 
                rec['imageName'] = imageName
                rec['imageHash'] = False
                rec['url'] = storageData[storagePosition]['images'][imagePosition]['url']
                rec['categoryId'] = ('NOT_CATEGORY' if storageData[storagePosition]['categoryId']=='' else storageData[storagePosition]['categoryId'])            
                rec['articleId'] = ('NOT_ARTICLE' if storageData[storagePosition]['articleId']=='' else storageData[storagePosition]['articleId'])            
                rec['title'] = ('NOT_TITLE' if storageData[storagePosition]['title']=='' else storageData[storagePosition]['title'])            
                rec['link'] = ('NOT_LINK' if storageData[storagePosition]['link']=='' else storageData[storagePosition]['link']) 
                rec['sellerId'] = ('NOT_SELLER' if storageData[storagePosition]['sellerId']=='' else storageData[storagePosition]['sellerId']) 
                rec['downloaded'] = False
                rec['compare'] = True
                rec['categorized'] = False

                db[collection].insert_one(rec)
                

    downloadImage(collection, kindOfStorage, sessionId)



