from http import HTTPStatus

from flask import abort, jsonify, make_response

from sw_api.database import rollback_session


def nocontent(message="no content.", **kwargs):
    abort(make_response(jsonify(message=message, **kwargs), 204))


def badrequest(message="bad request.", **kwargs):
    rollback_session()
    abort(make_response(jsonify(message=message, **kwargs), 400))


def notfound(message="not found.", **kwargs):
    rollback_session()
    abort(make_response(jsonify(message=message, **kwargs), HTTPStatus.NOT_FOUND))
