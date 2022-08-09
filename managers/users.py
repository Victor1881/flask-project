from werkzeug.exceptions import BadRequest
from werkzeug.security import generate_password_hash, check_password_hash

from db import db
from managers.auth import AuthManager
from models.user import User


class UserManager:
    @staticmethod
    def register(user_data):
        user_data['password'] = generate_password_hash(user_data['password'])
        user = User(**user_data)
        db.session.add(user)
        db.session.commit()
        return AuthManager.encode_token(user)

    @staticmethod
    def login(login_data):
        user = User.query.filter_by(email=login_data['email']).first()
        if not user:
            raise BadRequest('No such email! Please register')

        if check_password_hash(user.password, login_data["password"]):
            return AuthManager.encode_token(user)

        raise BadRequest('Wrong credentials!')