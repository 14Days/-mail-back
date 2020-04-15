from flask import current_app
from app.daos.user import IUser, DaoUser
from app.models.errors import UserNotFound, PasswordError
from app.utils import MD5, Token


class UserLoginData:
    def __init__(self, user_id, user_type, token):
        self.user_id = user_id
        self.user_type = user_type
        self.token = token


class ILogin:
    def user_login(self, username: str, password: str) -> UserLoginData:
        pass


class Login(ILogin):
    user: IUser

    def __init__(self):
        self.user = DaoUser()

    def user_login(self, username: str, password: str) -> UserLoginData:
        user = self.user.query_user_by_username(username)
        if user is None:
            raise UserNotFound('用户未找到')
        current_app.logger.debug(MD5.encode_md5(password))
        if user.password != MD5.encode_md5(password):
            raise PasswordError('用户密码错误')

        return UserLoginData(user.id, user.user_type, Token.create_token(user.id, user.user_type))
