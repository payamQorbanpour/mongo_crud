from marshmallow import fields, Schema, ValidationError
from pymongo import MongoClient
from app import price_limitaion


# Defining database and collection named stuff
table = MongoClient().crud_db.stuff


class Input(Schema):
    body = fields.Str()
    title = fields.String()
    price = fields.Float(validate=price_limitaion)
    email = fields.Email()
