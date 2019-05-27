from function.start import *

conn = MongoClient()
db = conn.imageMatcher

def categoriesForImage(collections, categories):

    for collection in collections:        
        for category in categories:                
            categoriesImage = db[collection].find_one({"category": category},{"_id":0, "imageName": 1, "categories":1})
            return categoriesImage