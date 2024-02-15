from marshmallow import fields
from schemas.base import ComplaintBaseSchema
from models.enums import State


class CreateComplaintResponseSchema(ComplaintBaseSchema):
    id = fields.Integer(required=True)
    created_on = fields.DateTime(required=True)
    status = fields.Enum(State, by_value=True)
    user_id = fields.Integer(required=True)
    photo_url = fields.String(required=True)


class GetComplaintResponseSchema(CreateComplaintResponseSchema):
    pass

