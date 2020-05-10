from app.daos.model import User
from app.daos.mail import IMail, DaoMail


class MailListData:
    def __init__(self, res, count):
        self.res = res
        self.count = count


class MailDetailData:
    def __int__(self, from_addr=None, to_addr=None, content=None, subject=None, time=None):
        self.from_addr = from_addr
        self.to_addr = to_addr
        self.content = content
        self.subject = subject
        self.time = time


class IEmail:
    _page: int
    _limit: int
    _mail: IMail
    _user: User

    def __init__(self, user_id, from_addr=None, to_addr=None, content=None, subject=None, page=0, limit=10):
        self._user_id = user_id
        self._from_addr = from_addr
        self._to_addr = to_addr
        self._content = content
        self._subject = subject
        self._page = page
        self._limit = limit
        self._mail = DaoMail()

    def send_mail(self, from_addr=None, to_addr=None, content=None, subject=None) -> None:
        raise NotImplementedError()

    def receive_mail(self) -> None:
        raise NotImplementedError()


class AdminEmail(IEmail):
    def send_mail(self, from_add=None, to_addr=None, content=None, subject=None) -> None:
        return

    def receive_mail(self) -> None:
        return


class UserEmail(IEmail):
    pass


def get_email(user_type: int, user_id=None, subject=None, page=0, limit=10) -> IEmail.__class__:
    if user_type == 1:
        return AdminEmail(user_id=user_id, page=page, limit=limit, subject=subject)
    else:
        return UserEmail(user_id=user_id)
