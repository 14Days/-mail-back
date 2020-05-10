from flask import Blueprint, request, current_app
from flask.views import MethodView
from app.models.email import Email as MEmail
from app.utils import Warp, errors

mail = Blueprint('login', __name__)


class Mail(MethodView):
    def get(self):
        data = request.json
        sender = data.get('sender')
        receivers = data.get('receivers')
        content = data.get('content')
        subject = data.get('subject')
        try:
            MEmail().send_mail(sender, receivers, content, subject)



mail.add_url_rule('/mail/send', view_func=Mail.as_view('mail'))
