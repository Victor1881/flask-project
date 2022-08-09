from flask import request
from flask_restful import Resource
from db import db
from managers.users import UserManager
from models.user import User
from schemas.request import RegisterSchemaRequest, LoginSchemaRequest
from units.decorators import validate_schema


class Register(Resource):
    @validate_schema(RegisterSchemaRequest)
    def post(self):
        data = request.get_json()
        token = UserManager.register(data)

        return {"token": token}, 201


class LoginResource(Resource):
    @validate_schema(LoginSchemaRequest)
    def post(self):
        data = request.get_json()
        token = UserManager.login(data)
        return {"token": token}, 200