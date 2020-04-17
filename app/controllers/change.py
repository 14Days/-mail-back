from flask import Blueprint, request, current_app
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError
from app.models.change import Change as MChange
from app.utils import Warp, errors

change = Blueprint('change', __name__)


class Change(MethodView):
    def post(self):
        data = request.json
        try:
            MChange().modify_message(data)
            return Warp.success_warp('修改成功')
        except SQLAlchemyError as e:
            current_app.logger.error(e)
            return Warp.fail_warp(501, errors['501'])


change.add_url_rule('/change', view_func=Change.as_view('change'))
