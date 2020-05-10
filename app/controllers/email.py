from flask import Blueprint, current_app, request, g
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError
from app.models.email import get_email
from app.utils import Warp, errors

mail = Blueprint('mail', __name__)


class Mail(MethodView):
    def get(self, name: str):
        current_app.logger.debug(name)
        if name is None:
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

    def post(self):
        pass


view = Mail.as_view('mail')
mail.add_url_rule('/mail', defaults={'name': None}, view_func=view, methods=['GET'])
