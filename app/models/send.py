import email
from flask import current_app, g
from email.header import decode_header
from app.daos.ip import IIP, DaoIP
from app.daos.mail import IMail, DaoMail
from app.daos.user import IUser, DaoUser
from app.models.errors import MailNotExist, AddrIsUseless, UserIsUseless, HaveNoReceiver, SMTPServerUseless
from app.models.protocol import Protocol
from app.utils.mail_decode import MailDecode
from app.daos.server import IServer, DaoServer
from app.daos.model import Server


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
    _server: IServer

    def __init__(self, user_id, subject=None, page=0, limit=10):
        self._user_id = user_id
        self._subject = subject
        self._page = page
        self._limit = limit
        self._mail = DaoMail()
        self._user = DaoUser()
        self._ip = DaoIP()
        self._server = DaoServer()

    @classmethod
    def _decode_str(cls, encode: str):
        value, charset = decode_header(encode)[0]
        if charset:
            value = value.decode(charset)
        return value

    def send_mail(self, sender_ip=None, to_addr=None, content=None, subject=None) -> None:
        return

    def get_mail_list(self) -> MailListData:
        raise NotImplementedError()

    def get_mail_detail(self, mail_id: int) -> MailDetailData:
        raise NotImplementedError()

    def send_delete(self, mail_id=None) -> None:
        return

    def send_server_state(self):
        server = self._server.query_server()
        return server.smtp_on


class AdminEmail(IEmail):
    def send_mail(self, sender_ip=None, to_addr=None, content=None, subject=None) -> None:
        if self.send_server_state() != 1:
            raise SMTPServerUseless("smtp服务已关闭")
        from_addr = f'{self._user.query_user_by_id(g.user_id).username}@wghtstudio.cn'
        to_addr = self._user.get_all_username()
        Protocol().send_mail(from_addr, to_addr, content,
                             subject)
        return

    def get_mail_list(self) -> MailListData:
        current_app.logger.debug(self._user_id)
        count, mail = self._mail.get_send_email(user_id=self._user_id, limit=self._limit, page=self._page)
        for item in mail:
            item['title'] = MailDecode(b'', item.get('title')).get_subject()
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
            subject=self._decode_str(mail.title),
            time=mail.create_at.strftime('%Y-%m-%d %H:%M')
        )

    def send_delete(self, mail_id=None) -> None:
        pass


class UserEmail(IEmail):
    def send_mail(self, sender_ip=None, to_addr=None, content=None, subject=None) -> None:
        if self.send_server_state() != 1:
            raise SMTPServerUseless("smtp服务已关闭")
        if self._ip.query_ip_by_address(sender_ip):
            raise AddrIsUseless('您的ip不可用')
        if g.user_type == 3:
            raise UserIsUseless('您的账户不可用')
        if to_addr is None:
            raise HaveNoReceiver('没有收件人')
        from_addr = f'{self._user.query_user_by_id(g.user_id).username}@wghtstudio.cn'
        Protocol().send_mail(from_addr, to_addr, content, subject)
        return

    def get_mail_list(self) -> MailListData:
        count, mail = self._mail.get_send_email(user_id=self._user_id, limit=self._limit,
                                                page=self._page)
        for item in mail:
            item['title'] = MailDecode(b'', item.get('title')).get_subject()
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
            subject=self._decode_str(mail.title),
            time=mail.create_at.strftime('%Y-%m-%d %H:%M')
        )

    def send_delete(self, mail_id=None) -> None:
        if self._mail.get_mail_by_id(mail_id) is None:
            raise MailNotExist("邮件不存在")
        self._mail.del_send_user_mail(mail_id)
        return


def get_email(user_type: int, user_id=None, subject=None, page=0, limit=10) -> IEmail.__class__:
    if user_type == 1:
        return AdminEmail(user_id=user_id, page=page, limit=limit, subject=subject)
    else:
        return UserEmail(user_id=user_id, page=page, limit=limit, subject=subject)
