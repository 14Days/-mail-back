import email
from email.header import decode_header
from flask import current_app
from app.daos.mail import IMail, DaoMail
from app.models.errors import MailNotExist, NotYourMail
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

    def __init__(self, user_id, subject=None, page=0, limit=10):
        self._user_id = user_id
        self._subject = subject
        self._page = page
        self._limit = limit
        self._mail = DaoMail()

    @classmethod
    def _decode_str(cls, encode: str):
        value, charset = decode_header(encode)[0]
        if charset:
            value = value.decode(charset)
        return value

    def get_mail_list(self) -> MailListData:
        raise NotImplementedError()

    def get_mail_detail(self, mail_id: int) -> MailDetailData:
        raise NotImplementedError()

    def receive_delete(self, mail_id: int):
        raise


class AdminEmail(IEmail):
    def get_mail_list(self) -> MailListData:
        current_app.logger.debug(self._user_id)
        count, mail = self._mail.get_all_email(title=self._subject, limit=self._limit, page=self._page)
        return MailListData(res=mail, count=count)

    def get_mail_detail(self, mail_id: int) -> MailDetailData:
        mail = self._mail.get_mail_by_id(mail_id)
        if mail is None:
            raise MailNotExist('邮件不存在')

        message = email.message_from_string(mail.content)

        title = mail.title if message.get('Subject') is None else self._decode_str(message.get('Subject'))

        content = ''
        for part in message.walk():
            if not part.is_multipart():
                content = part.get_payload(decode=True)

        return MailDetailData(
            from_addr=f'{mail.user.username}@wghtstudio.cn',
            to_addr=list(map(lambda x: f'{x.to_user.username}@wghtstudio.cn', mail.to_user)),
            content=str(content, encoding='utf-8'),
            subject=title,
            time=mail.create_at.strftime('%Y-%m-%d %H:%M')
        )

    def receive_delete(self, mail_id: int):
        if self._mail.get_mail_by_id(mail_id) is None:
            raise MailNotExist("邮件不存在")
        self._mail.del_mail(mail_id)
        return


class UserEmail(IEmail):
    def get_mail_list(self) -> MailListData:
        count, mail = self._mail.get_receive_mail(title=self._subject, user_id=self._user_id, limit=self._limit,
                                                  page=self._page)
        return MailListData(res=mail, count=count)

    def get_mail_detail(self, mail_id: int) -> MailDetailData:
        mail = self._mail.get_mail_by_id(mail_id)

        to_user = None
        for item in mail.to_user:
            if item.to_user_id == self._user_id:
                to_user = item.to_user
                break
        if to_user is None:
            raise NotYourMail('不是你的邮件')

        data = Protocol().get_mail_detail(mail.file_name, to_user)
        message = email.message_from_bytes(data)

        title = mail.title if message.get('Subject') is None else self._decode_str(message.get('Subject'))

        content = ''
        for part in message.walk():
            if not part.is_multipart():
                content = part.get_payload(decode=True)

        return MailDetailData(
            from_addr=f'{mail.user.username}@wghtstudio.cn',
            to_addr=list(map(lambda x: f'{x.to_user.username}@wghtstudio.cn', mail.to_user)),
            content=str(content, encoding='utf-8'),
            subject=title,
            time=mail.create_at.strftime('%Y-%m-%d %H:%M')
        )

    def receive_delete(self, mail_id: int):
        if self._mail.get_user_mail_by_id(mail_id) is None:
            raise MailNotExist("邮件不存在")
        self._mail.del_receive_user_mail(mail_id)
        return


def get_email(user_type: int, user_id=None, subject=None, page=0, limit=10) -> IEmail.__class__:
    if user_type == 1:
        return AdminEmail(user_id=user_id, page=page, limit=limit, subject=subject)
    else:
        return UserEmail(user_id=user_id, page=page, limit=limit, subject=subject)
