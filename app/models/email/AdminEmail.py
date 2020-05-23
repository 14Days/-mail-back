from flask import current_app
from app.daos import session_commit
from app.models.errors import MailNotExist
from app.models.email.IEmail import IEmail, MailListData, MailDetailData, ReceiveMailData
from app.utils.mail_decode import MailDecode


class AdminEmail(IEmail):
    def get_mail_list(self) -> MailListData:
        current_app.logger.debug(self._user_id)
        count, mail = self._mail.get_all_email(title=self._subject, limit=self._limit, page=self._page)

        res = []
        for item in mail:
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
        mail = self._mail.get_mail_by_id(mail_id)
        # 一定要判断是否存在这封邮件
        if mail is None:
            raise MailNotExist('邮件不存在')
        # 通过解码类解码
        decode = MailDecode(s=bytes(mail.content, 'utf-8'), title=mail.title)

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
        # 依次删除本身及多对多
        self._mail.del_user_mail(mail_id)
        self._mail.del_mail_weak(mail_id)

        session_commit()
