from datetime import datetime, timedelta
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
import jwt
from decouple import config
from flask_httpauth import HTTPTokenAuth
from werkzeug.exceptions import Unauthorized

from models import User


class AuthManager:
    @staticmethod
    def encode_token(user):
        payload = {"sub": user.id, "exp": datetime.utcnow() + timedelta(days=2)}
        return jwt.encode(payload, key=config('JWT_SECRET'), algorithm='HS256')

    @staticmethod
    def decode_token(token):
        if not token:
            raise Unauthorized('Missing token')
        try:
            payload = jwt.decode(token, key=config('JWT_SECRET'), algorithms=["HS256"])
            return payload["sub"]
        except ExpiredSignatureError:
            raise Unauthorized("Token expired")
        except InvalidTokenError:
            raise Unauthorized("Invalid token")


auth = HTTPTokenAuth()


@auth.verify_token
def verify(token):
    user_id = AuthManager.decode_token(token)
    return User.query.filter_by(id=user_id).first()