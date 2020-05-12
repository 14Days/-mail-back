from flask import Blueprint, request, current_app
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError
from app.models.register import Register as MRegister
from app.models.errors import UserHaveExist, PasswordNotSatisfactory
from app.utils import Warp

register = Blueprint('register', __name__)


class Register(MethodView):
    def post(self):
        data = request.json
        username = data.get('username')
        password = data.get('password')
        if username is None or username == '' or \
                password is None or password == '':
            current_app.logger.error('用户名或密码为空 %s', str({
                'username': username,
                'password': password
            }))
            return Warp.fail_warp(301)

        try:
            MRegister().create_new_user(username, password)
            return Warp.success_warp('注册成功')
        except SQLAlchemyError as e:
            current_app.logger.error(e)
            return Warp.fail_warp(501)
        except PasswordNotSatisfactory as e:
            current_app.logger.error(e)
            return Warp.fail_warp(203)
        except UserHaveExist as e:
            current_app.logger.error(e)
            return Warp.fail_warp(204)


register.add_url_rule('/register', view_func=Register.as_view('register'))
