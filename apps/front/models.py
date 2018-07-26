import enum
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import shortuuid
from exts import db


class Gender(enum.Enum):
    MALE = 1
    FEMALE = 2
    SECRET = 3
    UNKNOW = 4


class FrontUser(db.Model):
    __tablename__ = 'front_user'
    id = db.Column(db.String(100), primary_key=True, default=shortuuid.uuid)
    telephone = db.Column(db.String(128), nullable=False)
    username = db.Column(db.String(128), nullable=False)
    _password = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), unique=True)
    realname = db.Column(db.String(50))
    avatar = db.Column(db.String(100))
    signature = db.Column(db.String(100))
    gender = db.Column(db.Enum(Gender), default=Gender.UNKNOW)
    join_time = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, *args, **kwargs):
        if "password" in kwargs:
            self.password = kwargs.get('password')
            kwargs.pop('password')
        super(FrontUser, self).__init__(*args, **kwargs)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, new_pwd):
        self._password = generate_password_hash(new_pwd)

    def check_password(self, raw_password):
        return check_password_hash(self._password, raw_password)