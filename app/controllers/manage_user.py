from flask import Blueprint
from flask.views import MethodView

manage_user = Blueprint('manage_user', __name__)


class ManageUser(MethodView):
    def get(self, user_id):
        if user_id is None:
            pass
        else:
            pass


manage_user.add_url_rule('/user', defaults={'user_id': None}, view_func=ManageUser.as_view('manage_user'),
                         methods=['GET'])
manage_user.add_url_rule('/user', view_func=ManageUser.as_view('manage_user'), methods=['POST'])
