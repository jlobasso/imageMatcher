from function.start import *

config = configparser.ConfigParser()
config.read('conf.ini')

conn = MongoClient()
db = conn.imageMatcher


# def categoriesForImages(collections = "suspected-HH1", categories = "sports_car"):

collections = ["suspected-666666666666666", "suspected-HH1",] 
categories = ["convertible","pickup"]

for collection in collections:
    
    for category in categories:
        
        categoriesImage = db[collection].find({"category": category},{"imageName": 1, "categories":1})

        print(db[collection].find_one({"category": category},{"_id":0, "imageName": 1, "categories":1}))