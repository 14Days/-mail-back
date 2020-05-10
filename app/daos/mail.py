from typing import Tuple, List, Dict, Any
from app.daos import db
from app.daos.model import Mail


class MailData:
    def __init__(self, from_user, title, send_time, name):
        self.from_user = from_user
        self.title = title
        self.send_time = send_time
        self.name = name


class IMail:
    def get_all_email(self, title: str, page: int, limit: int) -> Tuple[int, list]:
        raise NotImplementedError()

    def get_user_email(self) -> Tuple[int, dict]:
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
                                 item.file_name).__dict__)

        return count, mail
