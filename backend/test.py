
from pymongo import MongoClient

conn = MongoClient()
db = conn.imageMatcher



images = db.download_live_search.find({ 'downloaded': False })

print(images.count()-1)