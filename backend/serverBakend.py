import sys
from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS
import json 

from getGroups import getGroups

app = Flask(__name__)
api = Api(app)
CORS(app)

class Health(Resource):
    def get(self):
        return "Tranki, anda ;)", 200, {'Content-Type':'application/json'}

class ProcessFastStrict(Resource):
    def post(self):        
        print("//*-*-*-*-*-*-*// MATCH PROCESS FAST STRICT //*-*-*-*-*-*-*//") 
        
        data = json.loads(request.data)
        from fastBatchStrict import matchFastStrict
        result = matchFastStrict(data['sessionId'], data['min_match_count'], data['sensibility'], data['min_percent_match'], data['storageA'], data['storageB'], data['categories'])
        return result, 200, {'Content-Type':'application/json'}

class ProcessFastWhole(Resource):
    def post(self):        
        print("//*-*-*-*-*-*-*// MATCH PROCESS FAST WHOLE //*-*-*-*-*-*-*//") 
        
        data = json.loads(request.data)
        from fastBatchWhole import matchFastWhole
        result = matchFastWhole(data['min_match_count'], data['sensibility'], data['min_percent_match'], data['storageA'], data['storageB'], data['categories'])
        return result, 200, {'Content-Type':'application/json'}


class ProcessSiftStrict(Resource):
    def post(self):        
        print("//*-*-*-*-*-*-*// MATCH PROCESS SIFT STRICT //*-*-*-*-*-*-*//") 
        
        data = json.loads(request.data)
        from siftBatchStrict import matchSiftStrict
        result = matchSiftStrict(data['min_match_count'], data['sensibility'], data['min_percent_match'], data['storageA'], data['storageB'], data['categories'])
        return result, 200, {'Content-Type':'application/json'}

class ProcessSiftWhole(Resource):
    def post(self):        
        print("//*-*-*-*-*-*-*// MATCH PROCESS SIFT WHOLE //*-*-*-*-*-*-*//") 
        
        data = json.loads(request.data)
        from siftBatchWhole import matchSiftWhole 
        result = matchSiftWhole(data['min_match_count'], data['sensibility'], data['min_percent_match'], data['storageA'], data['storageB'], data['categories'])
        return result, 200, {'Content-Type':'application/json'}
                
        
class Download(Resource):
    def post(self):
        print("//*-*-*-*-*-*-*// DOWNLOAD //*-*-*-*-*-*-*//") 
        
        data = json.loads(request.data)
        from download import insertImage
        insertImage(data)

class MatchFast(Resource):
    def get(self):        
        print("//*-*-*-*-*-*-*// MATCH FAST //*-*-*-*-*-*-*//")
        from matchFast import uniqueMatchFast
        return uniqueMatchFast(request.args)


class MatchSift(Resource):
    def get(self):        
        print("//*-*-*-*-*-*-*// MATCH SIFT //*-*-*-*-*-*-*//")
        from matchSift import uniqueMatchSift
        return uniqueMatchSift(request.args)

class Groups(Resource):
    def get(self):
        return getGroups(), 200, {'Content-Type':'application/json'}

class Test(Resource):
    def get(self):
        print("//*-*-*-*-*-*-*// TEST //*-*-*-*-*-*-*//")
        from test import testFunc
        return testFunc()


api.add_resource(Health, '/health')
api.add_resource(Groups, '/groups')

api.add_resource(ProcessFastStrict, '/process-fast-strict')
api.add_resource(ProcessFastWhole, '/process-fast-whole')

api.add_resource(ProcessSiftStrict, '/process-sift-strict')
api.add_resource(ProcessSiftWhole, '/process-sift-whole')

api.add_resource(MatchFast, '/match-fast') 
api.add_resource(MatchSift, '/match-sift')

api.add_resource(Download, '/download')

api.add_resource(Test, '/test')

if __name__ == '__main__':
    if len(sys.argv) > 1 and 'dev' in sys.argv:
        app.run(port='5000', debug=True)
    else:    
        app.run()
  
  