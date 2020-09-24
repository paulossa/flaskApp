from marshmallow import Schema, fields
from marshmallow.validate import Range

REQUIRED_ERROR_MESSAGE = {"required": "Campo obrigatório"}


class CartItemLoadSchema(Schema):
    id_product = fields.Integer(required=True, error_messages=REQUIRED_ERROR_MESSAGE)
    quantity = fields.Integer(
        validate=Range(min=1, error="Quantidade mínima de produtos é 1"),
        required=True,
        error_messages=REQUIRED_ERROR_MESSAGE
    )


class CartItemDumpSchema(Schema):
    product = fields.String()
    sale = fields.String()
    value = fields.Decimal(places=2)
    quantity = fields.Integer()


class CartLoadSchema(Schema):
    products = fields.Nested(CartItemLoadSchema, many=True, required=True, error_messages=REQUIRED_ERROR_MESSAGE)
