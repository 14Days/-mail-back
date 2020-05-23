import email
from email.header import decode_header
from email.message import Message


class MailDecode:
    """邮件解码类"""
    _message: Message
    _title: str

    @classmethod
    def _decode(cls, title):
        value, charset = decode_header(title)[0]
        if charset:
            value = value.decode(charset)
        return value

    def __init__(self, s: str, title):
        self._message = email.message_from_bytes(s)
        self._title = title

    def get_subject(self):
        """得到邮件标题"""
        temp = self._message.get('Subject')
        if temp is None:
            return self._decode(self._title)
        return self._decode(temp)

    def get_content(self):
        """获取邮件内容, 假设只有正文"""
        content = ''
        for part in self._message.walk():
            if not part.is_multipart():
                content = part.get_payload(decode=True)

        return str(content, encoding='utf-8')
