from marshmallow import Schema, fields


class SalesSchema(Schema):
    _id = fields.Integer(attribute="id", dump_to="id")
    description = fields.String()