from pymongo import MongoClient
from bson import json_util
import json 


def matchStatus(args):
    
    conn = MongoClient()
    db = conn.imageMatcher

    response = [doc for doc in db.matchStatus.find({"sessionId":args['sessionId']},{"_id":0})][0]
    
    return response

def downloadStatus(args):
    
    conn = MongoClient()
    db = conn.imageMatcher
    try:
        response = [doc for doc in db.downloadStatus.find({"sessionId":args['sessionId']},{"_id":0})][0]
    except:
        response = {"correctInsert" : 0}
    return response    