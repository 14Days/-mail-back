import re
from app.daos.user import IUser, DaoUser
from app.models.errors import UserHaveExist, PasswordNotSatisfactory
from app.utils import MD5


class IRegister:
    def create_new_user(self, username, password) -> None:
        raise NotImplementedError()


class Register(IRegister):
    _user: IUser
    _re_password = re.compile(r'(?=.*[A-Za-z])(?=.*[0-9])\w{6,}')

    def __init__(self):
        self._user = DaoUser()

    def create_new_user(self, username, password) -> None:
        if self._re_password.match(password) is None:
            raise PasswordNotSatisfactory('密码需要包含字母与数字, 且最少 6 位')
        user = self._user.query_user_by_username(username)
        if user is not None:
            raise UserHaveExist('用户已存在')
        self._user.add_user(username, MD5.encode_md5(password))
        return
