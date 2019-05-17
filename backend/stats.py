from pymongo import MongoClient
from bson import json_util
import json 


def matchStatus(args):
    
    conn = MongoClient()
    db = conn.imageMatcher

    response = db.matchStatus.find_one({"sessionId":args['sessionId']},{"_id":0})
    
    return response

def downloadStatus(args):
    
    conn = MongoClient()
    db = conn.imageMatcher
    try:
        response = db.downloadStatus.find_one({"sessionId":args['sessionId'], "collection":args['collection'], 'processing' : True},{"_id":0})
    except:
        response = {'count' : 0,
                    'correctDownload' : 0,
                    'errorDownload' : 0,
                    'timeCategorize' : 0,
                    'timeDownload' : 0
                    }

    if not response:
        response = db.downloadStatus.find_one({"sessionId":args['sessionId'], "collection":args['collection'], 'processing' : False},{"_id":0})
        
        if not response:
            response = {'count' : 0,
                        'correctDownload' : 0,
                        'errorDownload' : 0,
                        'timeCategorize' : 0,
                        'timeDownload' : 0
                        }

    return response    