from flask import request
from flask_restful import Resource


from helpers.decorators import validate_schema
from managers.authentication import UserAuthenticationManager
from schemas.request.users import UserRegisterRequestSchema, UserLoginRequestSchema
from schemas.response.users import UserAuthenticationResponseSchema


class UserRegisterResource(Resource):
    @validate_schema(UserRegisterRequestSchema)
    def post(self):
        data = request.get_json()
        user = UserAuthenticationManager.create_user(data)
        token = UserAuthenticationManager.encode_token(user)
        return UserAuthenticationResponseSchema().dump({'token': token})


class UserLoginResource(Resource):
    @validate_schema(UserLoginRequestSchema)
    def post(self):
        data = request.get_json()
        user = UserAuthenticationManager.login_user(data)
        token = UserAuthenticationManager.encode_token(user)
        return UserAuthenticationResponseSchema().dump({'token': token})
