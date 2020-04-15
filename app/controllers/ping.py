from flask import Blueprint
from flask.views import MethodView
from app.utils import success_warp

ping = Blueprint('ping', __name__)


class Ping(MethodView):
    def get(self):
        return success_warp('get pong')

    def post(self):
        return success_warp('post pong')


ping.add_url_rule('/ping', view_func=Ping.as_view('ping'))
