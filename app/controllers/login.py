from flask import Blueprint, request, current_app
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError
from app.models.login import Login as MLogin
from app.models.errors import UserNotFound, PasswordError
from app.utils import Warp, errors

login = Blueprint('login', __name__)


class Login(MethodView):
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
            return Warp.fail_warp(301, errors['301'])

        try:
            res = MLogin().user_login(username, password)
            return Warp.success_warp(res.__dict__)
        except SQLAlchemyError as e:
            current_app.logger.error(e)
            return Warp.fail_warp(501, errors['501'])
        except UserNotFound as e:
            current_app.logger.error(e)
            return Warp.fail_warp(201, errors['201'])
        except PasswordError as e:
            current_app.logger.error(e)
            return Warp.fail_warp(202, errors['202'])


login.add_url_rule('/login', view_func=Login.as_view('login'))
