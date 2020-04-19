from abc import ABC
from flask import current_app, g
from app.daos.model import User
from app.daos.user import IUser, DaoUser
from app.models.errors import UserNotFound, DeleteAdminError
from app.models.modify_info import ModifyInfo, AdminModifyInfo, ChangeModifyInfo


class UserListData:
    def __init__(self, res, count):
        self.res = res
        self.count = count


class UserDetailData:
    def __init__(self, user: User):
        self.id = user.id
        self.username = user.username
        self.nickname = user.nickname
        self.sex = user.sex
        self.user_type = user.user_type


class IManageUser:
    _user_id: str
    _page: int
    _limit: int
    _user: IUser
    _modify_user: ModifyInfo.__class__

    def __init__(self, user_id=None, username=None, page=0, limit=10, modify_user=None):
        self._user_id = user_id
        self._username = username
        self._page = page
        self._limit = limit
        self._user = DaoUser()
        self._modify_user = modify_user

    def get_all_user(self) -> UserListData:
        raise NotImplementedError()

    def get_user_detail(self) -> UserDetailData:
        user = self._user.query_user_by_id(int(self._user_id))
        if user is None:
            raise UserNotFound('用户未找到')

        return UserDetailData(user)

    def modify_user(self, info: dict) -> None:
        self._modify_user(self._user_id, info)

    def delete_user(self) -> None:
        raise NotImplementedError()


class AdminManageUser(IManageUser):
    def get_all_user(self) -> UserListData:
        current_app.logger.debug('username: %s, page: %s, limit: %s', self._username, self._page, self._limit)
        user_list, count = self._user.get_user_list(self._username, self._page, self._limit)
        return UserListData(user_list, count)

    def delete_user(self) -> None:
        user = self._user.query_user_by_id(int(self._user_id))
        if user is None:
            raise UserNotFound('用户未找到')

        if user.user_type == 1:
            raise DeleteAdminError('无法删除管理员账号')

        self._user.delete_user(user)


class UserManageUser(IManageUser, ABC):
    def get_user_detail(self) -> UserDetailData:
        if self._user_id != g.user_id:
            raise NotImplementedError()
        return super().get_user_detail()

    def modify_user(self, info: dict) -> None:
        if self._user_id != g.user_id:
            raise NotImplementedError()
        super().modify_user(info)


def get_manage_user(user_type: int, user_id=None, username=None, page=0, limit=10) -> IManageUser.__class__:
    if user_type == 1:
        return AdminManageUser(user_id, username, page, limit, AdminModifyInfo)
    else:
        return UserManageUser(user_id, username, page, limit, ChangeModifyInfo)
