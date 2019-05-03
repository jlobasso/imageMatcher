import urllib.request
import os
from function.start import *
from categorize.categorize import *

config = configparser.ConfigParser()
config.read('conf.ini')

conn = MongoClient()
db = conn.imageMatcher

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

def downloadImage(collection, kindOfStorage):
    start = time.time()
    images = db[collection].find({ 'downloaded': False })

    print("Imagenes por bajar:"+str(images.count()))

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
        except urllib.request.URLError:
            print("No se pudo descargar la imagen desde "+ximg['url'])
            continue
        
        db[collection].update({ "imageId" : ximg['imageId']  },{ "$set": { "downloaded" : True } })
        
    end = time.time()
    # eachImageTime = (time.time() - start)/totalAmountToAnalize 
    print("tiempo de descarga total de archivos: ", end - start)

    cantidad = db[collection].find({ "downloaded" : True } ).count()
    if cantidad > 0:
        categorize(collection, kindOfStorage)
    else:
        print("No se descargaron las imagenes en el storage")


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



