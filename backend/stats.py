from pymongo import MongoClient
from bson import json_util
import json 


def matchStatus(args):
    
    conn = MongoClient()
    db = conn.imageMatcher

    response = [doc for doc in db.matchStatus.find({"sessionId":args['sessionId']},{"_id":0})][0]
    
    return response