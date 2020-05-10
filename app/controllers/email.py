from flask import Blueprint, current_app, request, g
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError
from app.models.email import get_email
from app.models.errors import MailNotExist, NotYourMail
from app.utils import Warp, errors

mail = Blueprint('mail', __name__)


class Mail(MethodView):
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
        pass


view = Mail.as_view('mail')
mail.add_url_rule('/receive', defaults={'mail_id': None}, view_func=view, methods=['GET'])
mail.add_url_rule('/receive/<int:mail_id>', view_func=view, methods=['GET'])
