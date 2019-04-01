from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS

from json import dumps
# from flask.ext.jsonpify import jsonify

app = Flask(__name__)
api = Api(app)
CORS(app)

class Process(Resource):
    def post(self):
        print("----------------------------------------")
        # print(request.get_json())
        print("----------------------------------------")
        return 'PUTO', 200, {'Content-Type':'text/plain'}


        # return self.post.__init__

api.add_resource(Process, '/process') # Route_1


if __name__ == '__main__':
    app.run(port='5002', debug=True)
  
  