from marshmallow import Schema, fields
from marshmallow.validate import Range

REQUIRED_ERROR_MESSAGE = {"required": "Campo obrigatório"}


class ProductSchema(Schema):
    _id = fields.Integer(attribute="id", dump_to="id", dump_only=True)
    identifier = fields.String()
    name = fields.String(required=True, error_messages=REQUIRED_ERROR_MESSAGE)
    value = fields.Decimal(required=True, error_messages=REQUIRED_ERROR_MESSAGE, places=2,
                           validate=Range(min=0, error="Não pode ser negativo"))


class ProductListSchema(ProductSchema):
    id_sale = fields.Integer()