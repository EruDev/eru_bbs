from flask import g
from wtforms import StringField, IntegerField
from wtforms.validators import Email, Length, InputRequired, EqualTo, ValidationError
from ..forms import BaseForm
from ..utils import eru_cache

class LoginForm(BaseForm):
    email = StringField('邮箱', validators=[Email(message='请输入正确的邮箱格式!'), InputRequired(message='请输入邮箱')])
    password = StringField('密码', validators=[Length(min=6, max=20,
                                                    message='密码必须为6-20之间')])
    remember = IntegerField()


class ResetPwdForm(BaseForm):
    oldpwd = StringField('旧密码', validators=[Length(6, 20, message='密码必须为6-20之间')])
    newpwd = StringField('新密码', validators=[Length(6, 20, message='密码必须为6-20之间')])
    newpwd2 = StringField('新密码2', validators=[Length(6, 20, message='密码必须为6-20之间'), EqualTo('newpwd', message='两次输入的密码必须一致')])


class ResetEmailForm(BaseForm):
    email = StringField('邮箱', validators=[Email(message='请输入正确格式的邮箱')])
    captcha = StringField('验证码', validators=[Length(min=6, max=6, message='请输入正确长度的验证码')])

    def validate_captcha(self, field):
        captcha = field.data
        email = self.email.data
        captcha_cache = eru_cache.get(email)

        if not captcha_cache or captcha.lower() != captcha_cache.lower():
            raise ValidationError('邮箱验证码错误')

    def validate_email(self, field):
        email = field.data
        user = g.cms_user
        if user.email == email:
            raise ValidationError('不能修改为相同的邮箱')
