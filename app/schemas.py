from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    email_address = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
    verified = fields.Bool(required=True)
