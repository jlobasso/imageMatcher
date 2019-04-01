from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS
from json import dumps
import json 
# from flask.ext.jsonpify import jsonify
from matchList import *

app = Flask(__name__)
api = Api(app)
CORS(app)

min_match_count = 80
scale = 200
sensibility = 0.6
min_percent_match = 20

class Process(Resource):
    def post(self):

        # print("----------------------------------------")
        # print(request.data)
        # print("----------------------------------------")

        data = json.loads(request.data)
        result = match(data, min_match_count, scale, sensibility, min_percent_match)
        
        return result, 200, {'Content-Type':'application/json'}

api.add_resource(Process, '/process') 

if __name__ == '__main__':
    app.run(port='5002', debug=True)
  
  