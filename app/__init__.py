from flask import Flask
from flask_cors import CORS
from app.basic import set_config, set_logger


def create_new_app() -> Flask:
    app = Flask(__name__)
    CORS(app, supports_credentials=True)

    # 加载配置文件
    set_config(app)

    # 配置 logger
    set_logger(app)

    app.logger.info('app 配置成功')

    return app
