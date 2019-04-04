from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS
from json import dumps
import json 
# from flask.ext.jsonpify import jsonify
from matchList import *
from datetime import datetime, date, time, timedelta

app = Flask(__name__)
api = Api(app)
CORS(app)
# cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

# min_match_count = 80
# scale = 200
# sensibility = 0.6
# min_percent_match = 10

class Health(Resource):
    def get(self):
        return "Tranki, anda ;)", 200, {'Content-Type':'application/json'}

class Process(Resource):
    def post(self):

        tiempo1 = datetime.now()
        
        print("----------------------------------------")
        print("Fecha y Hora:", tiempo1)  # Muestra fecha y hora
        print("----------------------------------------")
        
        # data = json.loads(request.data)



        data = json.loads(request.data)
        # print(data)
        result = match(data['imagenes'], data['min_match_count'], data['scale'], data['sensibility'], data['min_percent_match'], data['compare_category'])
        
        # tiempo2 = datetime.now()

        # print("----------------------------------------")
        # print("Segundos:", tiempo2-tiempo1)  # Muestra segundo
        # print(result['imagenes1'])
        # print(result['imagenes2'])
        # print("----------------------------------------")

        return result, 200, {'Content-Type':'application/json'}

api.add_resource(Process, '/process') 
api.add_resource(Health, '/health')

if __name__ == '__main__':
    app.run(port='5000', debug=True)
    # app.run(debug=True, host='0.0.0.0')
  
  