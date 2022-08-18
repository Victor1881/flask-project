from werkzeug.exceptions import BadRequest
from werkzeug.security import generate_password_hash, check_password_hash
from managers.auth import AuthManager
from models.user import User
from units.helper.db import add
from units.helper.user_helper import donator_reward, delete


class UserManager:
    @staticmethod
    def register(user_data):
        user_data['password'] = generate_password_hash(user_data['password'])
        user = add(User, user_data)
        return AuthManager.encode_token(user)

    @staticmethod
    def login(login_data):
        user = User.query.filter_by(email=login_data['email']).first()
        if not user:
            raise BadRequest('No such email! Please register')

        if check_password_hash(user.password, login_data["password"]):
            return AuthManager.encode_token(user)

        raise BadRequest('Wrong credentials!')

    @staticmethod
    def reward(id):
        user = User.query.filter_by(id=id).first()
        if not user:
            raise BadRequest('No such user!')

        message = donator_reward(user)
        return message

    @staticmethod
    def delete_user(id):
        user = User.query.filter_by(id=id).first()
        if not user:
            raise BadRequest('No such user!')

        delete(user)


