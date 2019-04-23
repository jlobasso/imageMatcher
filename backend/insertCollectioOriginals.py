
from function.searchRepo import * 
from pymongo import MongoClient
import configparser
from categorize import *

config = configparser.ConfigParser()
config.read('conf.ini')

collection = 'orginals-joico'

images = getImages(collection)

kindOfStorage = 'originals' 
storageData = images
storageName = 'joico'

conn = MongoClient()
db = conn.imageMatcher

for imagePosition in images:
 
    cleanImg = imagePosition.split("/")
    imageName = cleanImg[len(cleanImg)-1]
    imageId = imageName.split(".")[0]
    
    imageName = imageName.encode('utf-8', 'surrogateescape').decode('utf-8')
    imageId = imageId.encode('utf-8', 'surrogateescape').decode('utf-8')
#     imageName = imageName.encode('ascii', 'ignore').decode('ascii')
#     imageId = imageId.encode('ascii', 'ignore').decode('ascii')
    
    exist = db[collection].find({"imageId":imageId}).count()

    if not exist:

        rec = {} 
        rec['imageId'] = imageId
        rec['imageName'] = imageName
        rec['url'] =  ""
        rec['ext'] =  ""
        rec['categoryId'] =  ""
        rec['articleId'] =  ""
        rec['title'] =  ""
        rec['link'] =  ""
        rec['sellerId'] = ""
        rec['downloaded'] = True
        rec['compare'] = True
        rec['categorized'] = False

        db[collection].insert(rec)


categorize(collection)