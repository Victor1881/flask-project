from marshmallow import Schema, fields, validate


class RegisterSchemaRequest(Schema):
    first_name = fields.Str(required=True, validate=validate.Length(min=2, max=20))
    last_name = fields.Str(required=True, validate=validate.Length(min=2, max=20))
    iban = fields.String(min_lenght=22, max_lenght=22, required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=8, max=20))


class LoginSchemaRequest(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=8, max=20))