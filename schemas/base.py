from marshmallow import Schema, fields


class BaseUserRequestSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)


class ComplaintBaseSchema(Schema):
    title = fields.String(requred=True)
    description = fields.String(requred=True)
    photo_url = fields.String(requred=True)
    amount = fields.Float(requred=True)
