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
    nickname = db.Column(db.String, nullable=False, default='新建用户')
    sex = db.Column(db.Integer, nullable=True, default=1)
    user_type = db.Column(db.Integer, nullable=False, default=2)
    mails = db.relationship('Mail', backref='user', lazy=True)
    to_list: list = db.relationship('UserMail', backref='to_user', foreign_keys='UserMail.to_user_id')


class Filter(db.Model):
    """
    IP列表模型
    """
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    create_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    update_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    delete_at = db.Column(db.DateTime, nullable=True)
    address = db.Column(db.String, nullable=False)


class Mail(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    create_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    update_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    delete_at = db.Column(db.DateTime, nullable=True)
    title = db.Column(db.String, nullable=False, default='无标题')
    file_name = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=True)
    size = db.Column(db.Integer, nullable=False)
    # dir_name_id = db.Column(db.Integer, db.ForeignKey('dir_name.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    is_from_del = db.Column(db.Integer, nullable=False, default=0)


class UserMail(db.Model):
    to_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), name='to', nullable=False, primary_key=True)
    mail_id = db.Column(db.Integer, db.ForeignKey('mail.id'), nullable=False, primary_key=True)
    is_to_del = db.Column(db.Integer, nullable=False, default=0)
    mail = db.relationship('Mail', backref='to_user', foreign_keys=[mail_id])
