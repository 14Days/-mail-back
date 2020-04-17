from flask import current_app, g
from app.daos.model import User
from app.daos.user import IUser, DaoUser
from app.models.errors import UserNotFound, DeleteAdminError, ModifyAdminError
from app.models.modify_info import ModifyInfo


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


class AdminModifyInfo(ModifyInfo):
    _dao_user: IUser

    def __init__(self, user_id, data):
        self._data = data
        self._dao_user = DaoUser()
        self._user = self._dao_user.query_user_by_id(user_id)
        if self._user is None:
            raise UserNotFound('用户未找到')

        if self._user.user_type == 1 and g.user_id != user_id:
            raise ModifyAdminError('无法修改管理员账号')

        self._handle_dict()
        self._commit()


class IManageUser:
    def get_all_user(self) -> UserListData:
        pass

    def get_user_detail(self) -> UserDetailData:
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

    def get_user_detail(self) -> UserDetailData:
        user = self._user.query_user_by_id(int(self._user_id))
        if user is None:
            raise UserNotFound('用户未找到')

        return UserDetailData(user)

    def modify_user(self, info: dict) -> None:
        AdminModifyInfo(self._user_id, info)

    def delete_user(self) -> None:
        user = self._user.query_user_by_id(int(self._user_id))
        if user is None:
            raise UserNotFound('用户未找到')

        if user.user_type == 1:
            raise DeleteAdminError('无法删除管理员账号')

        self._user.delete_user(user)
