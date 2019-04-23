from pymongo import MongoClient
from bson import json_util
import json 


def getGroups():

    conn = MongoClient()
    db = conn.imageMatcher

    # response = [json.dumps(doc, default=json_util.default) for doc in db.groupCategories.find({},{"_id":0})]
    response = [doc for doc in db.groupCategories.find({},{"_id":0})]
    return response