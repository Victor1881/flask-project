from marshmallow import Schema, fields


class DonateSchemaRequest(Schema):
    amount = fields.Integer(required=True)