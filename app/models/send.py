import email
from flask import current_app

from app.daos.ip import IIP, DaoIP
from app.daos.mail import IMail, DaoMail
from app.daos.user import IUser, DaoUser
from app.models.errors import MailNotExist, AddrIsUseless, UserIsUseless, HaveNoReceiver
from app.models.protocol import Protocol


class MailListData:
    def __init__(self, res, count):
        self.res = res
        self.count = count


class MailDetailData:
    def __init__(self, from_addr=None, to_addr=None, content=None, subject=None, time=None):
        self.from_addr = from_addr
        self.to_addr = to_addr
        self.content = content
        self.subject = subject
        self.time = time


class IEmail:
    _page: int
    _limit: int
    _mail: IMail
    _user: IUser
    _ip: IIP

    def __init__(self, user_id, subject=None, page=0, limit=10):
        self._user_id = user_id
        self._subject = subject
        self._page = page
        self._limit = limit
        self._mail = DaoMail()
        self._user = DaoUser()
        self._ip = DaoIP()

    def send_mail(self, sender_ip=None, from_add=None, to_addr=None, content=None, subject=None) -> None:
        return

    def get_mail_list(self) -> MailListData:
        raise NotImplementedError()

    def get_mail_detail(self, mail_id: int) -> MailDetailData:
        raise NotImplementedError()


class AdminEmail(IEmail):
    def send_mail(self, sender_ip=None, from_add=None, to_addr=None, content=None, subject=None) -> None:
        Protocol().send_mail(from_add, self._user.get_all_username(), content, subject)
        return

    def get_mail_list(self) -> MailListData:
        current_app.logger.debug(self._user_id)
        count, mail = self._mail.get_send_email(user_id=self._user_id, limit=self._limit, page=self._page)
        return MailListData(res=mail, count=count)

    def get_mail_detail(self, mail_id: int) -> MailDetailData:
        mail = self._mail.get_mail_by_id(mail_id)
        if mail is None:
            raise MailNotExist('邮件不存在')

        message = email.message_from_string(mail.content)

        content = ''
        for part in message.walk():
            if not part.is_multipart():
                content = part.get_payload(decode=True)

        return MailDetailData(
            from_addr=f'{mail.user.username}@wghtstudio.cn',
            to_addr=list(map(lambda x: f'{x.to_user.username}@wghtstudio.cn', mail.to_user)),
            content=str(content, encoding='utf-8'),
            subject=mail.title,
            time=mail.create_at.strftime('%Y-%m-%d %H:%M')
        )


class UserEmail(IEmail):
    def send_mail(self, sender_ip=None, from_add=None, to_addr=None, content=None, subject=None) -> None:
        if self._ip.query_ip_by_address(sender_ip):
            raise AddrIsUseless('您的ip不可用')
        if self._user.query_user_by_id(self._user_id).user_type == 3:
            raise UserIsUseless('您的账户不可用')
        if to_addr is None:
            raise HaveNoReceiver('没有收件人')
        Protocol().send_mail(from_add, to_addr, content, subject)
        return

    def get_mail_list(self) -> MailListData:
        count, mail = self._mail.get_receive_mail(title=self._subject, user_id=self._user_id, limit=self._limit,
                                                  page=self._page)
        return MailListData(res=mail, count=count)

    def get_mail_detail(self, mail_id: int) -> MailDetailData:
        mail = self._mail.get_mail_by_id(mail_id)
        if mail is None:
            raise MailNotExist('邮件不存在')

        message = email.message_from_string(mail.content)

        content = ''
        for part in message.walk():
            if not part.is_multipart():
                content = part.get_payload(decode=True)

        return MailDetailData(
            from_addr=f'{mail.user.username}@wghtstudio.cn',
            to_addr=list(map(lambda x: f'{x.to_user.username}@wghtstudio.cn', mail.to_user)),
            content=str(content, encoding='utf-8'),
            subject=mail.title,
            time=mail.create_at.strftime('%Y-%m-%d %H:%M')
        )


def get_email(user_type: int, user_id=None, subject=None, page=0, limit=10) -> IEmail.__class__:
    if user_type == 1:
        return AdminEmail(user_id=user_id, page=page, limit=limit, subject=subject)
    else:
        return UserEmail(user_id=user_id, page=page, limit=limit, subject=subject)
