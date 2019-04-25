import sys
from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS
from json import dumps
import json 
from datetime import datetime, date, time, timedelta

from matchList import *
from matchSift import *
from fastBatch import *
from matchFast import *
from download import *
from getGroups import *

app = Flask(__name__)
api = Api(app)
CORS(app)

class Health(Resource):
    def get(self):
        return "Tranki, anda ;)", 200, {'Content-Type':'application/json'}

class ProcessFast(Resource):
    def post(self):        
        print("----------------------------------------")
        print("MATCH PROCESS") 
        print("----------------------------------------")
        
        data = json.loads(request.data)
        
        # if str(data['min_match_count'] ) != "":
        result = matchFast(data['min_match_count'], data['sensibility'], data['min_percent_match'], data['storageA'], data['storageB'], data['categories'])
        return result, 200, {'Content-Type':'application/json'}

class ProcessSift(Resource):
    def post(self):        
        print("----------------------------------------")
        print("MATCH PROCESS SIFT") 
        print("----------------------------------------")
        
        data = json.loads(request.data)
        
        # if str(data['min_match_count'] ) != "":
        result = matchSift(data['min_match_count'], data['sensibility'], data['min_percent_match'], data['storageA'], data['storageB'], data['categories'])
        return result, 200, {'Content-Type':'application/json'}
        
        
        
class Download(Resource):
    def post(self):
        print("----------------------------------------")
        print("DOWNLOAD") 
        print("----------------------------------------")
        
        data = json.loads(request.data)
        insertImage(data)

class MatchFast(Resource):
    def get(self):        
        return uniqueMatchFast(request.args)


class MatchSift(Resource):
    def get(self):        
        return uniqueMatchSift(request.args)

class Groups(Resource):
    def get(self):
        return getGroups(), 200, {'Content-Type':'application/json'}

class Test(Resource):
    def get(self):
        print("----------------------------------------")
        print("TEST") 
        print("----------------------------------------")

        return testFunc()


api.add_resource(ProcessFast, '/process-fast') 
api.add_resource(ProcessSift, '/process-sift') 
api.add_resource(Download, '/download')
api.add_resource(MatchFast, '/match-fast') 
api.add_resource(MatchSift, '/match-sift') 
api.add_resource(Health, '/health')
api.add_resource(Groups, '/groups')
api.add_resource(Test, '/test')


if __name__ == '__main__':
    if len(sys.argv) > 1 and 'dev' in sys.argv:
        app.run(port='5000', debug=True)
    else:    
        app.run()
  
  