from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS
from json import dumps
import json 
# from flask.ext.jsonpify import jsonify
from matchListScaled import *

app = Flask(__name__)
api = Api(app)
CORS(app)

class Process(Resource):
    def post(self):
        # print("----------------------------------------")
        # print(request.data)
        

        # print("----------------------------------------")
        # print(request.data)
        # array = bytearray(request.data)
        # print(b"abcde".decode("utf-8") array[1])
        data = json.loads(request.data)
        
        # print(data[0])
        result = match(data)
        # s = '[{"i":"imap.gmail.com","p":"someP@ss"},{"i":"imap.aol.com","p":"anoterPass"}]'
        # jdata = json.loads(s)
        # print(data[0])
        # data = [{"a":"1"}]
        # print(data[0]["a"])
        # print(type(data))


        x = {
            "name": "John",
            "age": 30,
            "city": "New York"
        }
        
        
        return result, 200, {'Content-Type':'application/json'}


        # return self.post.__init__

api.add_resource(Process, '/process') # Route_1


if __name__ == '__main__':
    app.run(port='5002', debug=True)
  
  