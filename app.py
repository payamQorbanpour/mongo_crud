from flask import Flask, request
from flask_restful import Resource, Api, abort
from marshmallow import fields, Schema, ValidationError
from pymongo import MongoClient
from bson import ObjectId
from models import *

app = Flask(__name__)
api = Api(app)


def does_exist(data_id):
    title = table.find_one({"title": data_id})
    if not title:
        abort(404, message="doesn't exist.")


def price_limitaion(price):
    if price < 0:
        raise ValidationError('Price couldn\'t be negative!')
    if price > 1000:
        abort(400, message="The price is too high!")


class CRUD(Resource):
    # READ individually
    def get(self, data_id):
        does_exist(data_id)
        data = table.find_one({"title": data_id}, {"_id": 0})
        return data

    # CREATE
    def post(self, data_id):
        schema = Input()
        data = request.get_json()
        result = schema.load(data)
        print (result)
        if not result.errors:
            table.insert_one(result.data)
            return str(result.data), 201
        else:
            return result.errors, 400

    # UPDATE
    def put(self, data_id):
        does_exist(data_id)
        schema = Input()
        data = request.get_json()
        result = schema.load(data)
        if not result.errors:
            table.update_one({"title": data_id}, {"$set": data})
            return result, 201
        else:
            return result.errors, 400

    # DELETE
    def delete(self, data_id):
        does_exist(data_id)
        table.delete_one({"title": data_id})
        return 'Data deleted!', 204


# READ totally
class AllDataRetrive(Resource):
    def get(self):
        cursor = table.find({}, {"_id": 0})
        return [result for result in cursor]


api.add_resource(CRUD, '/<string:data_id>')
api.add_resource(AllDataRetrive, '/')

if __name__ == '__main__':
    app.run(debug=True)
