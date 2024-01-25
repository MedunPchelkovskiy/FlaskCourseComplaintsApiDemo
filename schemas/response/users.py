from marshmallow import Schema, fields


class UserAuthenticationResponseSchema(Schema):
    token = fields.String(required=True)
