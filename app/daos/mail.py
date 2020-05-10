from typing import Tuple, List, Dict, Any
from app.daos.model import Mail
from app.daos.user import DaoUser


class MailData:
    def __init__(self, from_user, title, send_time, mail_id):
        self.from_user = from_user
        self.title = title
        self.send_time = send_time
        self.mail_id = mail_id


class IMail:
    def get_all_email(self, title: str, page: int, limit: int) -> Tuple[int, list]:
        raise NotImplementedError()

    def get_receive_mail(self, title: str, user_id: int, page: int, limit: int) -> Tuple[int, list]:
        """收件箱列表方法"""
        raise NotImplementedError()

    def get_user_email(self, user_id: int, page: int, limit: int) -> Tuple[int, list]:
        """发件箱获取列表方法"""
        raise NotImplementedError()

    def get_mail_by_id(self, mail_id: int) -> Mail:
        raise NotImplementedError()


class DaoMail(IMail):
    def get_all_email(self, title: str, page: int, limit: int) -> Tuple[int, list]:
        # 查看是否是查找过滤模式
        if title is None:
            sql = Mail.query. \
                filter(Mail.delete_at.is_(None))
        else:
            sql = Mail.query. \
                filter(Mail.delete_at.is_(None)). \
                filter(Mail.title.like('%{}%'.format(title)))
        temp: List[Mail] = sql.limit(limit).offset(page * limit).all()
        count: int = sql.count()

        mail: List[Dict[str, Any]] = []
        for item in temp:
            mail.append(MailData(item.user.nickname, item.title, item.create_at.strftime('%Y-%m-%d %H:%M'),
                                 item.id).__dict__)
        mail.reverse()

        return count, mail

    def get_receive_mail(self, title: str, user_id: int, page: int, limit: int) -> Tuple[int, list]:
        # 处理函数
        def deal_func(x):
            temp_mail = x.mail
            if x.is_to_del == 0:
                return MailData(temp_mail.user.nickname, temp_mail.title,
                                temp_mail.create_at.strftime('%Y-%m-%d %H:%M'),
                                temp_mail.id).__dict__

        user = DaoUser().query_user_by_id(user_id)
        if user is None:
            raise RuntimeError('用户不存在')

        # 过滤用户删除
        mail = list(filter(lambda x: x is not None, map(deal_func, user.to_list)))
        if title is not None:
            mail = list(filter(lambda x: x['title'].find(title) != -1, mail))
        mail.reverse()

        return len(mail), mail

    def get_user_email(self, user_id: int, page: int, limit: int) -> Tuple[int, list]:
        sql = Mail.query. \
            filter(Mail.delete_at.is_(None)). \
            filter(Mail.is_from_del == 0). \
            filter(Mail.user_id == user_id)

        temp: List[Mail] = sql.limit(limit).offset(page * limit).all()
        count: int = sql.count()

        mail: List[Dict[str, Any]] = []
        for item in temp:
            mail.append(MailData(item.user.nickname, item.title, item.create_at.strftime('%Y-%m-%d %H:%M'),
                                 item.id).__dict__)
        mail.reverse()

        return count, mail

    def get_mail_by_id(self, mail_id: int) -> Mail:
        pass
