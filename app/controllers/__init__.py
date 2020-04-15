from flask import Flask
from app.controllers.ping import ping
from app.controllers.login import login


def register_router(app: Flask):
    # ping
    app.register_blueprint(ping)
    app.register_blueprint(login)
