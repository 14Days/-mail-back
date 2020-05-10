from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from app.basic import Config
from app.models.errors import NoReceivers, NoSender
from app.utils.mail.smtp_client import SMTP
from app.utils.mail.pop_client import POP3


class IProtocol:
    def get_mail_detail(self, name: str):
        raise NotImplementedError()

    def send_mail(self, from_addr=None, to_addr=None, content=None, subject=None) -> None:
        raise NotImplementedError()


class Protocol(IProtocol):
    _server_address: str = ''
    pop_server: POP3
    smtp_server: SMTP

    def __init__(self):
        self._server_address = Config.get_instance()['protocol_addr']
        self.pop_server = POP3(host=self._server_address, port=8026)
        self.smtp_server = SMTP(host=self._server_address, port=8025)

    def get_mail_detail(self, name: str):
        pass

    def send_mail(self, from_addr=None, to_addr=None, content=None, subject=None) -> None:
        message = MIMEMultipart()
        if from_addr is None:
            raise NoSender('没有发件人')
        message['From'] = Header(from_addr, 'utf-8')
        if to_addr is None:
            raise NoReceivers('没有收件人')
        message['To'] = Header(to_addr, 'utf-8')
        if subject is None:
            subject = '无主题'
        message['Subject'] = Header(subject, 'utf-8')
        if content is None:
            content = ""

        message.attach(MIMEText(content, 'plain', 'utf-8'))

        server = SMTP(self._server_address, 8025)
        server.set_debuglevel(1)
        server.sendmail(from_addr, to_addr, message.as_string())
        server.quit()
