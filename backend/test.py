
from pymongo import MongoClient

conn = MongoClient()
db = conn.imageMatcher


collection = "download_live_search"

images = db[collection].find().count()

print(images)