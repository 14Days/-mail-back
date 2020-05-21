from typing import List
from app.daos.mail import IMail, DaoMail


class SendMailData:
    def __init__(self, from_user, to_users, title, send_time, mail_id):
        self.from_user = from_user
        self.to_users = to_users
        self.title = title
        self.send_time = send_time
        self.mail_id = mail_id


class ReceiveMailData:
    def __init__(self, from_user, title, send_time, mail_id, is_read):
        self.from_user = from_user
        self.title = title
        self.send_time = send_time
        self.mail_id = mail_id
        self.is_read = is_read


class MailListData:
    """邮件列表数据定义"""

    def __init__(self, res: List[SendMailData] or List[ReceiveMailData], count: int):
        self.res = res
        self.count = count


class MailDetailData:
    """邮件详情数据定义"""

    def __init__(self, from_addr=None, to_addr=None, content=None, subject=None, time=None):
        self.from_addr = from_addr
        self.to_addr = to_addr
        self.content = content
        self.subject = subject
        self.time = time


class IEmail:
    _page: int  # 页数
    _limit: int  # 每页条目数
    _mail: IMail  # 数据库操作类

    def __init__(self, user_id, subject=None, page=0, limit=10):
        self._user_id = user_id
        self._subject = subject
        self._page = page
        self._limit = limit
        self._mail = DaoMail()

    def get_mail_list(self) -> MailListData:
        """获取收件箱列表"""
        raise NotImplementedError()

    def get_mail_detail(self, mail_id: int) -> MailDetailData:
        """获取邮件详情"""
        raise NotImplementedError()

    def receive_delete(self, mail_id: int):
        """删除收件箱邮件"""
        raise
