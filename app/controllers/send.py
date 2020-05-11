from flask import Blueprint, current_app, request, g
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError
from app.models.send import get_email
from app.models.errors import MailNotExist, NotYourMail
from app.utils.mail.smtp_client import SMTPException
from app.utils import Warp, errors

send = Blueprint('send', __name__)


class Send(MethodView):
    def get(self, mail_id: str):
        current_app.logger.debug(mail_id)
        if mail_id is None:
            # 获取所有邮件列表
            args = request.args
            subject = args.get('subject')
            # 做类型验证
            try:
                current_app.logger.debug(args.get('limit'))
                limit = int(args.get('limit'))
            except (TypeError, ValueError):
                limit = 10
            try:
                page = int(args.get('page'))
            except (TypeError, ValueError):
                page = 0

            try:
                res = get_email(g.user_type, g.user_id, subject=subject, page=page, limit=limit).get_mail_list()
                return Warp.success_warp(res.__dict__)
            except SQLAlchemyError as e:
                current_app.logger.error(e)
                return Warp.fail_warp(501, errors['501'])
            except NotImplementedError as e:
                current_app.logger.error(e)
                return Warp.fail_warp(403, errors['403'])
            except RuntimeError as e:
                current_app.logger.error(e)
                return Warp.fail_warp(201, errors['201'])
        else:
            try:
                res = get_email(g.user_type, user_id=g.user_id).get_mail_detail(mail_id)
                return Warp.success_warp(res.__dict__)
            except SQLAlchemyError as e:
                current_app.logger.error(e)
                return Warp.fail_warp(501, errors['501'])
            except MailNotExist as e:
                current_app.logger.error(e)
                return Warp.fail_warp(208, errors['208'])
            except NotYourMail as e:
                current_app.logger.error(e)
                return Warp.fail_warp(403, errors['403'])
            except NotImplementedError as e:
                current_app.logger.error(e)
                return Warp.fail_warp(403, errors['403'])

    def post(self):
        data = request.json
        sender_ip = request.remote_addr
        if g.user_type == 2:
            to_addr = data.get('receivers')
        else:
            to_addr = []
        content = data.get('content')
        subject = data.get('subject')
        try:
            get_email(g.user_type, user_id=g.user_id).send_mail(sender_ip, to_addr, content, subject)
            return Warp.success_warp('发送成功')
        except SMTPException as e:
            current_app.logger.error(e)
            return Warp.fail_warp(500, errors['500'])
        except NotImplementedError as e:
            current_app.logger.error(e)
            return Warp.fail_warp(403, errors['403'])


view = Send.as_view('send')
send.add_url_rule('/send', view_func=view, methods=['POST'])
send.add_url_rule('/send', defaults={'mail_id': None}, view_func=view, methods=['GET'])
send.add_url_rule('/send/<int:mail_id>', view_func=view, methods=['GET'])
