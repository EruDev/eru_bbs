# coding: utf-8
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from exts import db


class CMSPermission(object):
    # 255的二进制方式来表示 1111 1111
    ALL_PERMISSION = 0b11111111
    # 1. 访问者权限
    VISITOR =        0b00000001
    # 2. 管理帖子权限
    POSTER =         0b00000010
    # 3. 管理评论的权限
    COMMENTER =      0b00000100
    # 4. 管理版块的权限
    BOARDER =        0b00001000
    # 5. 管理前台用户的权限
    FRONTUSER =      0b00010000
    # 6. 管理后台用户的权限
    CMSUSER =        0b00100000
    # 7. 管理后台管理员的权限
    ADMINER =        0b01000000


cms_role_user = db.Table(
    'cms_role_user',
    db.Column('cms_role.id', db.Integer, db.ForeignKey('cms_role.id'), primary_key=True),
    db.Column('cms_user.id', db.Integer, db.ForeignKey('cms_user.id'), primary_key=True),
)


class CMSRole(db.Model):
    __tablename__ = 'cms_role'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), nullable=False)
    desc = db.Column(db.String(128), nullable=True)
    create_time = db.Column(db.DateTime, default=datetime.now)
    permissions = db.Column(db.Integer, default=CMSPermission.VISITOR)

    users = db.relationship('CMSUser', secondary=cms_role_user, backref='roles')


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