from functools import wraps

from flask import request
from marshmallow import Schema
from werkzeug.exceptions import BadRequest

from sw_api.utils.responses import badrequest


def check_body(schema):
    def real_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            application_json = "application/json"

            content_type = request.content_type

            if content_type != application_json:
                msg = f'Content-Type must be "{application_json}"'
                return badrequest(msg)

            r_json = request.get_json()
            serial = schema if isinstance(schema, Schema) else schema()
            document = serial.load(r_json)

            if document.errors:
                return badrequest(document.errors)

            kwargs["data"] = document.data

            return func(*args, **kwargs)
        return wrapper
    return real_decorator
