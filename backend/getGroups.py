from pymongo import MongoClient
from bson import json_util
import json 


def getGroups():

    conn = MongoClient()
    db = conn.imageMatcher

    response = [doc for doc in db.groupCategories.find({},{"_id":0})]
    return response