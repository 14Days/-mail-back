from app.daos.model import User


class IUser:
    def query_user_by_username(self, username: str) -> User:
        pass

    def query_user_by_id(self, uid: int) -> User:
        pass


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
