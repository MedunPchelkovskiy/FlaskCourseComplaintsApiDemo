from flask import request
from werkzeug.exceptions import BadRequest, Forbidden

from managers.authentication import auth


def validate_schema(schema_name):
    def decorated_function(funct):
        def wrapper(*args, **kwargs):
            schema = schema_name()
            data = request.get_json()
            errors = schema.validate(data)
            if not errors:
                return funct(*args, **kwargs)
            raise BadRequest(errors)
        return wrapper
    return decorated_function


def permission_required(role):
    def decorated_function(func):
        def wrapper(*args, **kwargs):
            user = auth.current_user()
            if user.role == role:
                return func(*args, **kwargs)
            raise Forbidden("You can't create complaint, no permission")
        return wrapper
    return decorated_function
