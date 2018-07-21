from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import Email, Length, InputRequired, EqualTo
from ..forms import BaseForm

class LoginForm(BaseForm):
    email = StringField('邮箱', validators=[Email(message='请输入正确的邮箱格式!'), InputRequired(message='请输入邮箱')])
    password = StringField('密码', validators=[Length(min=6, max=20,
                                                    message='密码必须为6-20之间')])
    remember = IntegerField()


class ResetPwdForm(BaseForm):
    oldpwd = StringField('旧密码', validators=[Length(6, 20, message='密码必须为6-20之间')])
    newpwd = StringField('新密码', validators=[Length(6, 20, message='密码必须为6-20之间')])
    newpwd2 = StringField('新密码2', validators=[Length(6, 20, message='密码必须为6-20之间'), EqualTo('newpwd', message='两次输入的密码必须一致')])