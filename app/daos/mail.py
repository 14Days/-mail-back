import datetime
from typing import Tuple, List
from app.daos.model import Mail, UserMail
from app.daos import db


class IMail:
    def get_all_email(self, title: str, page: int, limit: int) -> Tuple[int, list]:
        """得到所有邮件 (加入搜索)"""
        raise NotImplementedError()

    def get_receive_mail(self, title: str, user_id: int, page: int, limit: int) -> Tuple[int, list]:
        """得到指定用户邮件 (加入搜索)"""
        raise NotImplementedError()

    def get_send_email(self, user_id: int, page: int, limit: int) -> Tuple[int, list]:
        """发件箱获取列表方法"""
        raise NotImplementedError()

    def get_mail_by_id(self, mail_id: int) -> Mail:
        raise NotImplementedError()

    def del_send_user_mail(self, mail_id: int) -> None:
        """用户发件箱删除邮件"""
        raise NotImplementedError()

    def del_user_mail(self, mail_id: int) -> None:
        """删除多对多关系表记录"""
        raise NotImplementedError()

    def del_user_mail_weak(self, user_id: int, mail_id: int) -> None:
        """删除用户收件箱, 针对管理员来说需要保留邮件信息, 所以不能直接删除记录"""
        raise NotImplementedError()

    def del_mail_weak(self, mail_id: int) -> None:
        """软删除邮件表中的邮件"""
        raise NotImplementedError


class DaoMail(IMail):
    def get_all_email(self, title: str, page: int, limit: int) -> Tuple[int, List[Mail]]:
        # 查看是否是查找过滤模式
        if title is None:
            sql = Mail.query. \
                filter(Mail.delete_at.is_(None))
        else:
            sql = Mail.query. \
                filter(Mail.delete_at.is_(None)). \
                filter(Mail.title.like('%{}%'.format(title)))
        mail: List[Mail] = sql.order_by(Mail.create_at.desc()).limit(limit).offset(page * limit).all()
        count: int = sql.count()

        return count, mail

    def get_receive_mail(self, title: str, user_id: int, page: int, limit: int) -> Tuple[int, list]:
        mail = db.session. \
            query(UserMail, Mail).join(Mail). \
            filter(UserMail.to_user_id == user_id). \
            filter(UserMail.is_to_del == 0). \
            order_by(Mail.create_at.desc()). \
            limit(limit).offset(page * limit). \
            all()

        # 过滤用户查询
        if title is not None:
            mail = list(filter(lambda x: x[1].title.find(title) != -1, mail))

        return len(mail), mail

    #
    # def get_send_email(self, user_id: int, page: int, limit: int) -> Tuple[int, list]:
    #     sql = Mail.query. \
    #         filter(Mail.delete_at.is_(None)). \
    #         filter(Mail.is_from_del == 0). \
    #         filter(Mail.user_id == user_id)
    #
    #     temp: List[Mail] = sql.limit(limit).offset(page * limit).all()
    #     count: int = sql.count()
    #
    #     mail: List[Dict[str, Any]] = []
    #     for item in temp:
    #         to_user = list(map(lambda y: f'{y.to_user.username}@wghtstudio.cn', item.to_user))
    #         mail.append(
    #             MailData(item.user.username, to_user, self._decode_str(item.title),
    #                      item.create_at.strftime('%Y-%m-%d %H:%M'),
    #                      item.id).__dict__)
    #     mail.reverse()
    #     mail = mail[(page * limit):(page * limit + limit)]
    #
    #     return count, mail
    #
    def get_mail_by_id(self, mail_id: int) -> Mail:
        return Mail.query. \
            filter(Mail.id == mail_id). \
            filter(Mail.delete_at.is_(None)). \
            first()

    #
    #
    # def del_send_user_mail(self, mail_id: int) -> None:
    #     _mail = self.get_mail_by_id(mail_id)
    #     _mail.is_from_del = 1
    #     session_commit()
    #     return
    #
    def del_user_mail(self, mail_id: int) -> None:
        # 删除多对多关系表
        _user_mail = UserMail.query. \
            filter(UserMail.mail_id == mail_id). \
            all()
        for item in _user_mail:
            db.session.delete(item)

    def del_user_mail_weak(self, user_id: int, mail_id: int) -> None:
        mail = UserMail.query. \
            filter(UserMail.to_user_id == user_id). \
            filter(UserMail.mail_id == mail_id). \
            first()

        mail.is_to_del = 1

    def del_mail_weak(self, mail_id: int) -> None:
        # 删除邮件本身
        mail = self.get_mail_by_id(mail_id)
        mail.delete_at = datetime.datetime.now()
