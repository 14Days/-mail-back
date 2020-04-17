import re
from app.daos.user import IUser, DaoUser
from app.models.errors import UserNotFound


class IChange:
    def user_change(self, uid: int, user_type: int, nickname: str, sex: int) -> None:
        pass


class Change(IChange):
    _user: IUser

    def __init__(self):
        self.user = DaoUser()

    def user_change(self, uid: int, user_type: int, nickname: str, sex: int) -> None:
        user = self.user.query_user_by_id(uid)
        if user is None:
            raise UserNotFound('用户未找到')
        self._user.change_user(uid, user_type, nickname, sex)
        return
