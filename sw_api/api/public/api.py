from flask import Blueprint

from sw_api.api.public.products import products_ns
from sw_api.utils.custom_api import CustomApi

public_bp = Blueprint("public_api", __name__)

api = CustomApi(public_bp, doc="/doc/")

api.add_namespace(products_ns)

