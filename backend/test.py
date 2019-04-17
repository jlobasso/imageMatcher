
from pymongo import MongoClient

conn = MongoClient(connect=False)

db = conn.imageMatcher

def testFunc():
    print('antes')
    
    exist = db.download_live_search.find({"imageId":''}).count()
    
    print(exist)
    
