from email.mime.text import MIMEText
from email.header import Header
from flask import current_app
from app.daos.mail import IMail, DaoMail
from app.models.errors import NoReceivers, NoSender, ContentIsNone
from app.utils.mail.smtp_client import SMTP


class MailListData:
    def __init__(self, res, count):
        self.res = res
        self.count = count


class IEmail:
    _page: int
    _limit: int
    _mail: IMail

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

    def get_mail_list(self) -> MailListData:
        raise NotImplementedError


class AdminEmail(IEmail):
    def send_mail(self, from_add=None, to_addr=None, content=None, subject=None) -> None:
        server_address = 'localhost'
        if content is None:
            raise ContentIsNone('内容为空了')
        message = MIMEText(content, 'plain', 'utf-8')
        if from_add is None:
            raise NoSender('没有发件人')
        message['From'] = Header(from_add, 'utf-8')
        if to_addr is None:
            raise NoReceivers('没有收件人')
        message['To'] = Header(to_addr, 'utf-8')
        if subject is None:
            subject = '无主题'
        message['Subject'] = Header(subject, 'utf-8')
        server = SMTP(server_address, 8025)
        server.set_debuglevel(1)
        server.sendmail(from_add, to_addr, message.as_string())
        server.quit()
        return

    def receive_mail(self) -> None:
        return

    def get_mail_list(self) -> MailListData:
        current_app.logger.debug(self._user_id)
        count, mail = self._mail.get_all_email(title=self._subject, limit=self._limit, page=self._page)
        return MailListData(res=mail, count=count)


class UserEmail(IEmail):
    pass


def get_email(user_type: int, user_id=None, subject=None, page=0, limit=10) -> IEmail.__class__:
    if user_type == 1:
        return AdminEmail(user_id=user_id, page=page, limit=limit, subject=subject)
    else:
        return UserEmail(user_id=user_id)
