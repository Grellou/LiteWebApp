from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    email_address = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
    verified = fields.Bool(required=True)

class AuthSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)

class AuthResponseSchema(Schema):
    access_token = fields.Str()

class ItemSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    type = fields.Str(required=True)
    language = fields.Str(required=True)
    price = fields.Float(required=True)
    quantity = fields.Int(required=True)
