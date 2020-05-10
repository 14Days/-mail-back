from flask import Flask
from app.controllers.login import login
from app.controllers.ping import ping
from app.controllers.register import register
from app.controllers.manage_user import manage_user
from app.controllers.manage_ip import manage_ip
from app.controllers.email import mail
from app.middlewares import jwt_middleware


def register_router(app: Flask):
    # ping
    app.register_blueprint(ping)
    # 登录
    app.register_blueprint(login)
    # 注册
    app.register_blueprint(register)
    # 用户管理
    jwt_middleware(manage_user)
    app.register_blueprint(manage_user)
    # ip黑名单
    jwt_middleware(manage_ip)
    app.register_blueprint(manage_ip)
    # 收发邮件
    jwt_middleware(mail)
    app.register_blueprint(mail)
