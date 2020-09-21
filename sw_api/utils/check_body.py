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
            mult_form_data = "multipart/form-data"

            content_type = request.content_type

            if content_type != application_json and mult_form_data not in content_type:
                msg = f'Content-Type must be "{application_json}" or "{mult_form_data}"'
                return badrequest(msg)

            try:
                r_json = request.get_json()
            except BadRequest:
                r_json = {}

            if mult_form_data in content_type:
                r_json = {**request.files.to_dict(flat=False), **request.form.to_dict(flat=False)}

            serial = schema if isinstance(schema, Schema) else schema()
            document = serial.load(r_json)

            if document.errors:
                return badrequest(document.errors)

            kwargs["data"] = document.data

            return func(*args, **kwargs)
        return wrapper
    return real_decorator