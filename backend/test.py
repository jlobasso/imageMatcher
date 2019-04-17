
from pymongo import MongoClient

conn = MongoClient()

db = conn.imageMatcher

print('antes de la funcion')
    
exist = db.download_live_search.find()

print(exist)

print('despues de la funcion')


def testFunc():
    print('antes dentro de la funcion')
    
    exist = db.download_live_search.find()
    
    print(exist)

    print('despues dentro de la funcion')
    
