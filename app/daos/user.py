import datetime
from typing import List, Dict, Any
from app.daos import db, session_commit
from app.daos.model import User


class UserListData:
    def __init__(self, username, nickname, user_type):
        self.username = username
        self.nickname = nickname
        self.user_type = user_type


class IUser:
    def query_user_by_username(self, username: str) -> User:
        raise NotImplementedError()

    def query_user_by_id(self, uid: int) -> User:
        raise NotImplementedError()

    def add_user(self, username: str, password: str) -> None:
        raise NotImplementedError()

    def get_user_list(self, username: str, page: int, limit: int) -> (List[Dict[str, Any]], int):
        raise NotImplementedError()

    def delete_user(self, user: User) -> None:
        raise NotImplementedError()


class DaoUser(IUser):
    def query_user_by_username(self, username):
        return User.query. \
            filter_by(username=username). \
            filter_by(delete_at=None). \
            first()

    def query_user_by_id(self, uid):
        return User.query. \
            filter_by(id=uid). \
            filter_by(delete_at=None). \
            first()

    def add_user(self, username: str, password: str) -> None:
        user = User(username=username, password=password)
        db.session.add(user)
        session_commit()

    def get_user_list(self, username: str, page: int, limit: int) -> (List[Dict[str, Any]], int):
        # 查看是否是查找过滤模式
        if username is None:
            sql = User.query. \
                filter(User.delete_at.is_(None)). \
                filter(User.user_type != 1)
        else:
            sql = User.query. \
                filter(User.delete_at.is_(None)). \
                filter(User.user_type != 1). \
                filter(User.username.like('%{}%'.format(username)))
        temp = sql.limit(limit).offset(page * limit).all()
        count = sql.count()

        user: List[Dict[str, Any]] = []
        for item in temp:
            user.append(UserListData(item.username, item.nickname, item.user_type).__dict__)

        return user, count

    def delete_user(self, user: User) -> None:
        user.delete_at = datetime.datetime.now()
        session_commit()
