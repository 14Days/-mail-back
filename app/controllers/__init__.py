from flask import Flask
from app.controllers.login import login
from app.controllers.ping import ping
from app.controllers.register import register


def register_router(app: Flask):
    # ping
    app.register_blueprint(ping)
    # 登录
    app.register_blueprint(login)
    # 注册
    app.register_blueprint(register)
