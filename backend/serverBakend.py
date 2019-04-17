import sys
from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS
from json import dumps
import json 
# from flask.ext.jsonpify import jsonify
# from matchList import *
from download import *
from match import *
from fastBatch import *
from datetime import datetime, date, time, timedelta
import urllib

app = Flask(__name__)
api = Api(app)
CORS(app)

class Health(Resource):
    def get(self):
        return "Tranki, anda ;)", 200, {'Content-Type':'application/json'}

class Process(Resource):
    def post(self):

        tiempo1 = datetime.now()
        
        print("----------------------------------------")
        print("Fecha y Hora:", tiempo1)  # Muestra fecha y hora
        print("----------------------------------------")
        
        data = json.loads(request.data)
        
        if str(data['min_match_count'] ) != "":
            result = match(data['imagenes'], data['min_match_count'], data['scale'], data['sensibility'], data['min_percent_match'], data['compare_category'])
            return result, 200, {'Content-Type':'application/json'}
        
        
class Download(Resource):
    def post(self):
        print("----------------------------------------")
        print("DOWNLOAD") 
        print("----------------------------------------")
        
        data = json.loads(request.data)
        insertImage(data)
        # downloadImage()

class Match(Resource):
    def get(self):

        # url1 = request.args.get('url1')
        
        return uniqueMatch(request.args)


class Test(Resource):
    def get(self):

        
        return testFunc()


api.add_resource(Process, '/process') 
api.add_resource(Download, '/download')
api.add_resource(Match, '/match') 
api.add_resource(Health, '/health')
api.add_resource(Test, '/test')


if __name__ == '__main__':
    if len(sys.argv) > 1 and 'dev' in sys.argv:
        app.run(port='5000', debug=True)
    else:    
        app.run()
  
  