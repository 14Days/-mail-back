from flask import Flask
from app.controllers.ping import ping
from app.middlewares import jwt_middleware


def register_router(app: Flask):
    # ping
    app.register_blueprint(ping)
