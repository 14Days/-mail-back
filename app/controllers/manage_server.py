from flask import Blueprint, request, current_app
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError
from app.models.errors import StateNotExist, PortOutOfRange, PropertyNotExist
from app.models.modify_ser import manage_server as my_server
from app.utils import Warp

manage_server = Blueprint('manage_server', __name__)


class ManageServer(MethodView):
    def put(self):
        try:
            my_server(request.json)
            return Warp.success_warp('修改成功')
        except (TypeError, ValueError, PropertyNotExist) as e:
            current_app.logger.error(e)
            return Warp.fail_warp(302, msg=str(e))
        except SQLAlchemyError as e:
            current_app.logger.error(e)
            return Warp.fail_warp(501)
        except StateNotExist as e:
            current_app.logger.error(e)
            return Warp.fail_warp(302)
        except PortOutOfRange as e:
            current_app.logger.error(e)
            return Warp.fail_warp(302)
        except NotImplementedError as e:
            current_app.logger.error(e)
            return Warp.fail_warp(403)


view = ManageServer.as_view('manage_server')
manage_server.add_url_rule('/server', view_func=view, methods=['PUT'])
