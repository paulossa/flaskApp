from collections import OrderedDict

import simplejson
from flask import current_app, make_response
from flask_restplus import Api

from sw_api.database import rollback_session


def error_handler(error):
    rollback_session()
    code = getattr(error, "code", 500)
    message = "bad gateway" if code == 502 else "internal server error"
    return {"message": message}, code


def custom_output_json(data, code, headers=None):
    settings = current_app.config.get("RESTPLUS_JSON", {})
    dumped = simplejson.dumps(data, **settings) + "\n"
    resp = make_response(dumped, code)
    resp.headers.extend(headers or {})
    return resp


class CustomApi(Api):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.representations = OrderedDict([("application/json", custom_output_json)])
        self._default_error_handler = error_handler
