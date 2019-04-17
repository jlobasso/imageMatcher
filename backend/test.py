
from pymongo import MongoClient

conn = MongoClient()

db = conn.imageMatcher

def testFunc():
    print('antes')
    
    exist = db.download_live_search.find({"imageId":'', "sellerId":''}).count()
    
    print(exist)
    
