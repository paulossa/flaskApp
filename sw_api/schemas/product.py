from marshmallow import Schema, fields


class ProductGetSchema(Schema):
    _id = fields.Integer(attribute="id", dump_to="id")
    name = fields.String()
    value = fields.Decimal(places=2)