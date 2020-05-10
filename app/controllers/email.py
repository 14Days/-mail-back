from flask import Blueprint
from flask.views import MethodView

mail = Blueprint('login', __name__)


class Mail(MethodView):
    def get(self):
        pass


mail.add_url_rule('/mail', view_func=Mail.as_view('mail'))
