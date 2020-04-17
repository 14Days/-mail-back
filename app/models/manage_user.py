from flask import current_app
from app.daos.user import IUser, DaoUser


class UserListData:
    def __init__(self, res, count):
        self.res = res
        self.count = count


class IManageUser:
    def get_all_user(self) -> UserListData:
        pass

    def get_user_detail(self):
        pass

    def add_user(self, username: str, password: str):
        pass

    def modify_user(self, info: dict) -> None:
        pass

    def delete_user(self) -> None:
        pass


class ManageUser(IManageUser):
    _user_id: str
    _page: int
    _limit: int
    _user: IUser

    def __init__(self, user_id=None, username=None, page=0, limit=10):
        self._user_id = user_id
        self._username = username
        self._page = page
        self._limit = limit
        self._user = DaoUser()

    def get_all_user(self) -> UserListData:
        current_app.logger.debug('username: %s, page: %s, limit: %s', self._username, self._page, self._limit)
        user_list, count = self._user.get_user_list(self._username, self._page, self._limit)
        return UserListData(user_list, count)
