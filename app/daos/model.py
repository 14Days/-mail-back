import datetime
from app.daos import db


class User(db.Model):
    """
    用户数据模型
    """
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    create_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    update_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    delete_at = db.Column(db.DateTime, nullable=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    nickname = db.Column(db.String, nullable=False)
    sex = db.Column(db.Integer, nullable=True, default=1)
    user_type = db.Column(db.Integer, nullable=False, default=2)
    user_status = db.Column(db.Integer, nullable=False, default=1)
