from flask import Flask, request
from flask_restful import Resource, Api, abort
from marshmallow import fields, Schema, ValidationError
from pymongo import MongoClient
from bson import ObjectId
from models import *

app = Flask(__name__)
api = Api(app)


def does_exist(stuff_id):
    this_stuff = table_stuff.find_one({"title": stuff_id})
    if not this_stuff:
        abort(404, message="doesn't exist.")


def price_limitaion(price):
    if price < 0:
        raise ValidationError('Price couldn\'t be negative!')
    if price > 1000:
        abort(400, message="The price is too high!")


class Stuff(Resource):
    # READ individually
    def get(self, stuff_id):
        does_exist(stuff_id)
        this_stuff = table_stuff.find_one({"title": stuff_id}, {"_id": 0})
        return this_stuff

    # CREATE
    def post(self, stuff_id):
        schema = Input()
        stuff = request.get_json()
        result = schema.load(stuff)
        print (result)
        if not result.errors:
            table_stuff.insert_one(result.data)
            return str(result.data), 201
        else:
            return result.errors, 400

    # UPDATE
    def put(self, stuff_id):
        does_exist(stuff_id)
        schema = Input()
        stuff = request.get_json()
        result = schema.load(stuff)
        if not result.errors:
            table_stuff.update_one({"title": stuff_id}, {"$set": stuff})
            return result, 201
        else:
            return result.errors, 400

    # DELETE
    def delete(self, stuff_id):
        does_exist(stuff_id)
        table_stuff.delete_one({"title": stuff_id})
        return 'Data deleted!', 204


# READ totally
class AllStuff(Resource):
    def get(self):
        cursor = table_stuff.find({}, {"_id": 0})
        return [result for result in cursor]


api.add_resource(Stuff, '/<string:stuff_id>')
api.add_resource(AllStuff, '/')

if __name__ == '__main__':
    app.run(debug=True)