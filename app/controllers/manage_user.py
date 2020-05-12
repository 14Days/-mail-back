from flask import Blueprint, request, current_app, g
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError
from app.models.errors import UserNotFound, DeleteAdminError, ModifyAdminError, PropertyNotExist, \
    PasswordNotSatisfactory, ModifyUserTypeError
from app.models.manage_user import get_manage_user
from app.utils import Warp

manage_user = Blueprint('manage_user', __name__)


class ManageUser(MethodView):
    def get(self, user_id):
        # 管理员执行方法
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
                res = get_manage_user(g.user_type, username=username, page=page, limit=limit).get_all_user()
                return Warp.success_warp(res.__dict__)
            except SQLAlchemyError as e:
                current_app.logger.error(e)
                return Warp.fail_warp(501)
            except NotImplementedError as e:
                current_app.logger.error(e)
                return Warp.fail_warp(403)
        else:
            try:
                res = get_manage_user(g.user_type, user_id=user_id).get_user_detail()
                return Warp.success_warp(res.__dict__)
            except SQLAlchemyError as e:
                current_app.logger.error(e)
                return Warp.fail_warp(501)
            except UserNotFound as e:
                current_app.logger.error(e)
                return Warp.fail_warp(201)
            except NotImplementedError as e:
                current_app.logger.error(e)
                return Warp.fail_warp(403)

    def put(self, user_id):
        try:
            get_manage_user(g.user_type, user_id=user_id).modify_user(request.json)
            return Warp.success_warp('修改成功')
        except (TypeError, ValueError, PropertyNotExist) as e:
            current_app.logger.error(e)
            return Warp.fail_warp(302, msg=str(e))
        except SQLAlchemyError as e:
            current_app.logger.error(e)
            return Warp.fail_warp(501)
        except UserNotFound as e:
            current_app.logger.error(e)
            return Warp.fail_warp(201)
        except ModifyAdminError as e:
            current_app.logger.error(e)
            return Warp.fail_warp(406)
        except PasswordNotSatisfactory as e:
            current_app.logger.error(e)
            return Warp.fail_warp(203)
        except NotImplementedError as e:
            current_app.logger.error(e)
            return Warp.fail_warp(403)
        except ModifyUserTypeError as e:
            current_app.logger.error(e)
            return Warp.fail_warp(403)

    def delete(self, user_id):
        try:
            get_manage_user(g.user_type, user_id=user_id).delete_user()
            return Warp.success_warp('删除成功')
        except SQLAlchemyError as e:
            current_app.logger.error(e)
            return Warp.fail_warp(501)
        except UserNotFound as e:
            current_app.logger.error(e)
            return Warp.fail_warp(201)
        except DeleteAdminError as e:
            current_app.logger.error(e)
            return Warp.fail_warp(406)
        except NotImplementedError as e:
            current_app.logger.error(e)
            return Warp.fail_warp(403)


view = ManageUser.as_view('manage_user')
manage_user.add_url_rule('/user', defaults={'user_id': None}, view_func=view, methods=['GET'])
manage_user.add_url_rule('/user/<int:user_id>', view_func=view, methods=['GET', 'PUT', 'DELETE'])
