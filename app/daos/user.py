from app.daos import db
from app.daos.model import User


class IUser:
    def query_user_by_username(self, username: str) -> User:
        pass

    def add_user(self, username: str, password: str) -> None:
        pass


class DaoUser(IUser):
    def query_user_by_username(self, username):
        return User.query. \
            filter_by(username=username). \
            filter_by(delete_at=None). \
            first()

    def add_user(self, username: str, password: str) -> None:
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
