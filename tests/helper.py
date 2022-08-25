from managers.auth import AuthManager


def generate_user_token(user):
    token = AuthManager.encode_token(user)
    return token