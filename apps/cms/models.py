# coding: utf-8
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from exts import db


class CMSUser(db.Model):
    __tablename__ = 'cms_user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), nullable=False)
    _password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    join_time = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, username, password, email):
        self.username = username
        self.password = password  # 这里的 password 指的是调用了password属性
        self.email = email

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw_password):
        self._password = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        result = check_password_hash(self.password, raw_password)  # 第一个参数: hash过的密码, 第二个参数:原始密码
        return result