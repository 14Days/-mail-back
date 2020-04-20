from flask import Blueprint, request, current_app, g
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError
from app.models.manage_ip import IPManage as MManage
from app.models.errors import AddressNotExist, AddressExist, AddressError
from app.utils import Warp, errors

manage_ip = Blueprint('manage_ip', __name__)


class ManageIP(MethodView):
    def get(self):
        if g.user_type != 1:
            current_app.logger.error('无权限 %s', str({
                'user_type': g.user_type
            }))
            return Warp.fail_warp(403, errors['403'])
        # 获取所有黑名单ip信息
        args = request.args
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
            res = MManage(page=page, limit=limit).get_ip_list()
            return Warp.success_warp(res.__dict__)
        except SQLAlchemyError as e:
            current_app.logger.error(e)
            return Warp.fail_warp(501, errors['501'])

    def post(self):
        if g.user_type != 1:
            current_app.logger.error('无权限 %s', str({
                'user_type': g.user_type
            }))
            return Warp.fail_warp(403, errors['403'])
        data = request.json
        address = data.get('address')
        if address is None or address == '':
            current_app.logger.error('ip地址为空 %s', str({
                'address': address
            }))
            return Warp.fail_warp(301, errors['301'])

        try:
            MManage().add_black_ip(address)
            return Warp.success_warp('拉黑ip成功')
        except SQLAlchemyError as e:
            current_app.logger.error(e)
            return Warp.fail_warp(501, errors['501'])
        except AddressExist as e:
            current_app.logger.error(e)
            return Warp.fail_warp(205, errors['205'])
        except AddressError as e:
            current_app.logger.error(e)
            return Warp.fail_warp(207, errors['207'])

    def delete(self):
        if g.user_type != 1:
            current_app.logger.error('无权限 %s', str({
                'user_type': g.user_type
            }))
            return Warp.fail_warp(403, errors['403'])
        data = request.json
        address = data.get('address')
        if address is None or address == '':
            current_app.logger.error('ip地址为空 %s', str({
                'address': address
            }))
            return Warp.fail_warp(301, errors['301'])

        try:
            MManage().delete_black_ip(address)
            return Warp.success_warp('ip移除黑名单成功')
        except SQLAlchemyError as e:
            current_app.logger.error(e)
            return Warp.fail_warp(501, errors['501'])
        except AddressNotExist as e:
            current_app.logger.error(e)
            return Warp.fail_warp(206, errors['206'])


manage_ip.add_url_rule('/filter', view_func=ManageIP.as_view('manage_ip'), methods=['GET', 'POST', 'DELETE'])
