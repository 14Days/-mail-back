from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from flask import current_app
from app.basic import Config
from app.daos.mail import IMail, DaoMail
from app.models.errors import NoReceivers, NoSender
from app.utils.mail.smtp_client import SMTP


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
    _server_address: str = ''

    def __init__(self, user_id, from_addr=None, to_addr=None, content=None, subject=None, page=0, limit=10):
        self._user_id = user_id
        self._from_addr = from_addr
        self._to_addr = to_addr
        self._content = content
        self._subject = subject
        self._page = page
        self._limit = limit
        self._server_address = Config.get_instance()['protocol_addr']
        self._mail = DaoMail()

    def send_mail(self, from_addr=None, to_addr=None, content=None, subject=None) -> None:
        raise NotImplementedError()

    def receive_mail(self) -> None:
        raise NotImplementedError()

    def get_mail_list(self) -> MailListData:
        raise NotImplementedError()

    def get_mail_detail(self, mail_id: int) -> MailDetailData:
        raise NotImplementedError()


class AdminEmail(IEmail):
    def send_mail(self, from_add=None, to_addr=None, content=None, subject=None) -> None:
        message = MIMEMultipart()
        if from_add is None:
            raise NoSender('没有发件人')
        message['From'] = Header(from_add, 'utf-8')
        if to_addr is None:
            raise NoReceivers('没有收件人')
        message['To'] = Header(to_addr, 'utf-8')
        if subject is None:
            subject = '无主题'
        message['Subject'] = Header(subject, 'utf-8')
        if content is None:
            content = ""

        message.attach(MIMEText(content, 'plain', 'utf-8'))

        server = SMTP(self._server_address, 8025)
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

    def get_mail_detail(self, mail_id: int) -> MailDetailData:
        pass


class UserEmail(IEmail):
    def get_mail_list(self) -> MailListData:
        count, mail = self._mail.get_receive_mail(user_id=self._user_id, limit=self._limit, page=self._page)
        return MailListData(res=mail, count=count)


def get_email(user_type: int, user_id=None, subject=None, page=0, limit=10) -> IEmail.__class__:
    if user_type == 1:
        return AdminEmail(user_id=user_id, page=page, limit=limit, subject=subject)
    else:
        return UserEmail(user_id=user_id)
