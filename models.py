from marshmallow import fields, Schema
from pymongo import MongoClient
from app import price_limitaion


class Data(Schema):
    body = fields.Str()
    title = fields.String()
    price = fields.Float(validate=price_limitaion)
    email = fields.Email()
