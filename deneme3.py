from flask import Flask, request
from flask_restful import Api, Resource, reqparse
import pandas as pd

app = Flask(_name_)
api = Api(app)

class Users(Resource):
    def _init_(self):
        self.data = pd.read_csv('kullanicilar.csv')
    def get(self):
        self.data = self.data.to_dict('records')
        return {'data' : self.data}, 200

    def post(self):
        data_arg=reqparse.RequestParser()
        data_arg.add_argument("name" , type=str)
        data_arg.add_argument("age" , type=int)
        data_arg.add_argument("city" , type=str)

        args = data_arg.parse_args()

        self.data = pd.concat([self.data, pd.DataFrame([args])], ignore_index=True)
        self.data.to_csv("kullanicilar.csv", index=False)
        
        return {'message' : 'Record successfully added.'}, 200

    def delete(self):
        name = request.args['name']

        if name in self.data['name'].values:
            self.data = self.data[self.data['name'] != name]
            self.data.to_csv('kullanicilar.csv', index=False)
            return {'message': 'Record successfully deleted.'}, 200
        else:
            return {'message': 'Record not found.'}, 404

class Cities(Resource):
    def get(self):
        data = pd.read_csv('kullanicilar.csv', usecols=[2])
        data = data.to_dict('records')
        return {'data' : data}, 200

class Name(Resource):
    def get(self, name):
        data = pd.read_csv('kullanicilar.csv')
        data = data.to_dict('records')
        for entry in data:
            if entry['name'] == name:
                return {'data' : entry}, 207
        return {'message' : 'No entry found with this name!'}, 405

class AddNumbers(Resource):
    def get(self):
        # İstek parametrelerinden "num" anahtarını alıyoruz
        numbers = request.args.getlist('num', type=int)  # "num" parametresini bir liste olarak al

        # Sayıları topluyoruz
        result = sum(numbers)

        # Sonucu döndürüyoruz
        return {'result': result}, 200

# URL endpointlerini ekleme
api.add_resource(Users, '/users')
api.add_resource(Cities, '/cities')
api.add_resource(Name, '/<string:name>')
api.add_resource(AddNumbers, '/add_numbers')  # Yeni endpoint

if _name_ == '_main_':
    app.run()