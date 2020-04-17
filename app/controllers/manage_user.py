from flask import Blueprint, request, current_app
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError
from app.models.errors import UserNotFound, DeleteAdminError, ModifyAdminError, PropertyNotExist
from app.models.manage_user import ManageUser as MManageUser
from app.utils import Warp, errors, Permission, auth_require

manage_user = Blueprint('manage_user', __name__)


class ManageUser(MethodView):
    decorators = [auth_require(Permission.ADMIN)]

    def get(self, user_id):
        if user_id is None:
            # 获取所有用户信息
            args = request.args
            username = args.get('username')
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
                res = MManageUser(username=username, page=page, limit=limit).get_all_user()
                return Warp.success_warp(res.__dict__)
            except SQLAlchemyError as e:
                current_app.logger.error(e)
                return Warp.fail_warp(501, errors['501'])
        else:
            try:
                res = MManageUser(user_id=user_id).get_user_detail()
                return Warp.success_warp(res.__dict__)
            except SQLAlchemyError as e:
                current_app.logger.error(e)
                return Warp.fail_warp(501, errors['501'])
            except UserNotFound as e:
                current_app.logger.error(e)
                return Warp.fail_warp(201, errors['201'])

    def put(self, user_id):
        try:
            MManageUser(user_id=user_id).modify_user(request.json)
            return Warp.success_warp('修改成功')
        except (TypeError, PropertyNotExist) as e:
            current_app.logger.error(e)
            return Warp.fail_warp(302, str(e))
        except SQLAlchemyError as e:
            current_app.logger.error(e)
            return Warp.fail_warp(501, errors['501'])
        except UserNotFound as e:
            current_app.logger.error(e)
            return Warp.fail_warp(201, errors['201'])
        except ModifyAdminError as e:
            current_app.logger.error(e)
            return Warp.fail_warp(406, errors['406'])

    def delete(self, user_id):
        try:
            MManageUser(user_id=user_id).delete_user()
            return Warp.success_warp('删除成功')
        except SQLAlchemyError as e:
            current_app.logger.error(e)
            return Warp.fail_warp(501, errors['501'])
        except UserNotFound as e:
            current_app.logger.error(e)
            return Warp.fail_warp(201, errors['201'])
        except DeleteAdminError as e:
            current_app.logger.error(e)
            return Warp.fail_warp(406, errors['406'])


view = ManageUser.as_view('manage_user')
manage_user.add_url_rule('/user', defaults={'user_id': None}, view_func=view, methods=['GET'])
manage_user.add_url_rule('/user/<int:user_id>', view_func=view, methods=['GET', 'PUT', 'DELETE'])
