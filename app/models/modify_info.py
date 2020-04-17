from typing import Dict, Any
from app.daos import session_commit
from app.daos.model import User
from app.models.errors import PropertyNotExist
from app.utils import MD5


class ModifyInfo:
    _user: User
    _data: Dict[str, Any]

    def _handle_dict(self):
        for key, val in self._data.items():
            method = getattr(self, f'handle_{key}', None)
            if method is None:
                raise PropertyNotExist(f'{key} 属性不存在')
            method(val)

    def handle_password(self, password):
        self._user.password = MD5.encode_md5(password)

    def handle_nickname(self, nickname):
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
