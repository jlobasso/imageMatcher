from pymongo import MongoClient

conn = MongoClient()
db = conn.imageMatcher

imageName = 'chevrolet_3800_pickup_xoptimizadax-kgRF--620x349@abc.jpg'

print(db['suspected-DDGG1'].find_one({"imageName":imageName},{"imageId":1, '_id':0})['imageId'])


