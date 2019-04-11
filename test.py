from pymongo import MongoClient

conn = MongoClient()

db = conn.imageMatcher

collection = db.suspectedImages

a = {"hola":"chau"}  

rec_id1 = collection.insert_one(a)

cursor = collection.find() 
for record in cursor: 
    print(record) 

