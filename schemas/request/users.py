from marshmallow import fields

from schemas.base import BaseUserRequestSchema


class UserRegisterRequestSchema(BaseUserRequestSchema):
    first_name = fields.String(min_length=2, max_length=20, required=True)
    last_name = fields.String(min_length=2, max_length=20, required=True)
    phone = fields.String(min_length=10, max_length=13, required=True)
    iban = fields.String(required=True)


class UserLoginRequestSchema(BaseUserRequestSchema):
    pass