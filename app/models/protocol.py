from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from functools import reduce
from app.basic import Config
from app.utils.mail.smtp_client import SMTP
from app.utils.mail.pop_client import POP3


class IProtocol:
    def get_mail_detail(self, name: str, user):
        raise NotImplementedError()

    def send_mail(self, from_addr=None, to_addr=None, content=None, subject=None) -> None:
        raise NotImplementedError()


class Protocol(IProtocol):
    _server_address: str = ''
    pop_server: POP3
    smtp_server: SMTP

    def __init__(self):
        self._server_address = Config.get_instance()['protocol_addr']

    def get_mail_detail(self, name: str, user):
        pop = POP3(host=self._server_address, port=8026)
        pop.user(user.username)
        pop.pass_(user.password)
        mail_list = pop.uidl()[1]
        index = 0
        for item in mail_list:
            temp = str(item, encoding='utf-8')
            temp = temp.split()
            if temp[1] == name:
                index = int(temp[0])
                break
        content = pop.retr(index)
        return reduce(lambda x, y: x + y, content[1])

    def send_mail(self, from_addr=None, to_addr=None, content=None, subject=None) -> None:
        if subject is None:
            subject = '无主题'
        if content is None:
            content = ""
        message = MIMEMultipart()
        message['From'] = Header(from_addr, 'utf-8')
        message['To'] = Header(';'.join(to_addr), 'utf-8')
        message['Subject'] = Header(subject, 'utf-8')
        message.attach(MIMEText(content, 'plain', 'utf-8'))

        server = SMTP(self._server_address, 8025)
        server.set_debuglevel(1)
        server.sendmail(from_addr, to_addr, message.as_string())
        server.quit()
        return
