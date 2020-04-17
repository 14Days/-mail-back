from app.models.modify_info import ModifyInfo
from flask import g
from app.models.errors import ModifyUserTypeError
from app.daos.user import IUser, DaoUser


class ChangeModifyInfo(ModifyInfo):
    user: IUser

    def __init__(self, data):
        self._data = data
        self.user = DaoUser()
        self._user = self.user.query_user_by_id(g.user_id)
        self._handle_dict()
        self._commit()

    def handle_user_type(self, user_type):
        raise ModifyUserTypeError('没有权限修改你的用户类型')


class Change:
    def modify_message(self, data):
        ChangeModifyInfo(data)
