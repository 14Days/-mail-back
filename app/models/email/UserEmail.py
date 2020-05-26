from app.daos import session_commit
from app.daos.server import DaoServer
from app.models.errors import MailNotExist, NotYourMail, POPServerUseless
from app.models.protocol import Protocol
from app.models.email.IEmail import IEmail, MailListData, MailDetailData, ReceiveMailData
from app.utils.mail_decode import MailDecode


class UserEmail(IEmail):
    @classmethod
    def confirm_pop_server_is_on(cls):
        server = DaoServer().query_server()
        return server.pop_on == 1

    def get_mail_list(self) -> MailListData:
        if not self.confirm_pop_server_is_on():
            raise POPServerUseless('POP3 服务未运行')
        count, mail = self._mail.get_receive_mail(title=self._subject, user_id=self._user_id, limit=self._limit,
                                                  page=self._page)

        res = []
        for _, item in mail:
            decode = MailDecode(b'', item.title)
            res.append(
                ReceiveMailData(
                    from_user=item.user.nickname, title=decode.get_subject(),
                    send_time=item.create_at.strftime('%Y-%m-%d %H:%M'),
                    mail_id=item.id, is_read=1
                ).__dict__
            )

        return MailListData(res=res, count=count)

    def get_mail_detail(self, mail_id: int) -> MailDetailData:
        if not self.confirm_pop_server_is_on():
            raise POPServerUseless('POP3 服务未运行')
        mail = self._mail.get_mail_by_id(mail_id)
        # 一定要判断是否存在这封邮件
        if mail is None:
            raise MailNotExist('邮件不存在')

        to_user = None
        for item in mail.to_user:
            if item.to_user_id == self._user_id and item.is_to_del == 0:
                to_user = item.to_user
                break
        if to_user is None:
            raise NotYourMail('不是你的邮件')

        data = Protocol().get_mail_detail(mail.file_name, to_user)
        decode = MailDecode(data, mail.title)

        return MailDetailData(
            from_addr=f'{mail.user.username}@wghtstudio.cn',
            to_addr=list(map(lambda x: f'{x.to_user.username}@wghtstudio.cn', mail.to_user)),
            content=decode.get_content(),
            subject=decode.get_subject(),
            time=mail.create_at.strftime('%Y-%m-%d %H:%M')
        )

    def receive_delete(self, mail_id: int):
        if self._mail.get_mail_by_id(mail_id) is None:
            raise MailNotExist("邮件不存在")

        self._mail.del_user_mail_weak(self._user_id, mail_id)
        session_commit()
