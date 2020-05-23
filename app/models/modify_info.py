import re
from typing import Dict, Any
from flask import g
from app.daos import session_commit
from app.daos.model import User
from app.daos.user import IUser, DaoUser
from app.models.errors import PropertyNotExist, PasswordNotSatisfactory, UserNotFound, ModifyAdminError, \
    ModifyUserTypeError
from app.utils import MD5


class ModifyInfo:
    _user: User
    _data: Dict[str, Any]
    _re_password = re.compile(r'(?=.*[A-Za-z])(?=.*[0-9])\w{6,}')
    _dao_user: IUser

    def __init__(self, user_id, data):
        pass

    def _handle_dict(self):
        for key, val in self._data.items():
            method = getattr(self, f'handle_{key}', None)
            if method is None:
                raise PropertyNotExist(f'{key} 属性不存在')
            method(val)

    def handle_password(self, password):
        if self._re_password.match(password) is None:
            raise PasswordNotSatisfactory('密码需要包含字母与数字, 且最少 6 位')
        self._user.password = MD5.encode_md5(password)

    def handle_nickname(self, nickname):
        if nickname == '' or nickname is None:
            raise ValueError('nickname 不能为空')
        self._user.nickname = nickname

    def handle_sex(self, sex):
        if sex != 1 and sex != 2:
            raise TypeError('sex 必须为 1 或 2')
        self._user.sex = sex

    def handle_user_type(self, user_type):
        # if user_type != 2 and user_type != 3:
        #     raise TypeError('user_type 必须为 1 或 2')
        self._user.user_type = user_type

    def _commit(self):
        session_commit()


class AdminModifyInfo(ModifyInfo):
    def __init__(self, user_id, data):
        super().__init__(user_id, data)
        self._data = data
        self._dao_user = DaoUser()
        self._user = self._dao_user.query_user_by_id(user_id)
        if self._user is None:
            raise UserNotFound('用户未找到')

        # if self._user.user_type == 1 and g.user_id != user_id:
        #     raise ModifyAdminError('无法修改管理员账号')

        self._handle_dict()
        self._commit()


class ChangeModifyInfo(ModifyInfo):
    def __init__(self, user_id, data):
        super().__init__(user_id, data)
        self._data = data
        self._dao_user = DaoUser()
        self._user = self._dao_user.query_user_by_id(user_id)
        self._handle_dict()
        self._commit()

    def handle_user_type(self, user_type):
        raise ModifyUserTypeError('没有权限修改你的用户类型')
