from flask import current_app
from app.daos.user import IUser, DaoUser
from app.models.errors import UserNotFound, PasswordError
from app.utils import MD5, Token


class UserChangeData:
    def __init__(self, user_id, user_type, token):
        self.user_id = user_id
        self.user_type = user_type
        self.token = token


class IChange:
    def user_change(self, uid: int, username: str, nickname: str, sex: int) -> UserChangeData:
        pass


class Change(IChange):
    user: IUser

    def __init__(self):
        self.user = DaoUser()

    def user_change(self, uid: int) -> UserChangeData:
        user = self.user.query_user_by_id(uid)
        if user is None:
            raise UserNotFound('用户未找到')


        return UserChangeData()
