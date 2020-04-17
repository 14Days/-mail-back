import re
from typing import Dict, Any
from app.daos import session_commit
from app.daos.model import User
from app.models.errors import PropertyNotExist, PasswordNotSatisfactory
from app.utils import MD5


class ModifyInfo:
    _user: User
    _data: Dict[str, Any]
    _re_password = re.compile(r'(?=.*[A-Za-z])(?=.*[0-9])\w{6,}')

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
        if user_type != 2 and user_type != 3:
            raise TypeError('user_type 必须为 1 或 2')
        self._user.user_type = user_type

    def _commit(self):
        session_commit()
