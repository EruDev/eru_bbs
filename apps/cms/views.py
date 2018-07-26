# coding: utf-8
import string
import random
from flask import Blueprint, views, render_template, \
    request, session, redirect, url_for, g
from flask_mail import Message
from .forms import LoginForm, ResetPwdForm, ResetEmailForm
from .models import CMSUser, CMSPermission
from .decorators import login_required, permission_required
from exts import db, mail
from apps.utils import restful, eru_cache


bp = Blueprint('cms', __name__, url_prefix='/cms')

@bp.route('/posts')
@login_required
@permission_required(CMSPermission.POSTER)
def posts():
    return render_template('cms/cms_posts.html')


@bp.route('/boards')
@login_required
@permission_required(CMSPermission.BOARDER)
def boards():
    return render_template('cms/cms_boards.html')


@bp.route('/comments')
@login_required
@permission_required(CMSPermission.COMMENTER)
def comments():
    return render_template('cms/cms_comments.html')


@bp.route('/croles')
@login_required
@permission_required(CMSPermission.ALL_PERMISSION)
def croles():
    return render_template('cms/cms_croles.html')


@bp.route('/cusers')
@login_required
@permission_required(CMSPermission.CMSUSER)
def cusers():
    return render_template('cms/cms_cusers.html')


@bp.route('/fusers')
@login_required
@permission_required(CMSPermission.FRONTUSER)
def fusers():
    return render_template('cms/cms_fusers.html')


@bp.route('/email_captcha/')
def email_captcha():
    # http://cms/email_captcha?email=xxx@xx.com
    email = request.args.get('email')
    if not email:
        return restful.params_error('参数错误')
    else:
        captchas = string.ascii_letters + string.digits
        captcha = ''.join(random.sample(captchas, 6))
        message = Message('Eru论坛邮箱验证码', recipients=[email], body='这是您的邮箱验证码: %s' % captcha)
        try:
            mail.send(message)
        except:
            return restful.server_error()
        eru_cache.set(email, captcha)
        return restful.success('success')


@bp.route('/email')
def send_email():
    message = Message('验证邮箱', recipients=['455772170@qq.com'], body='测试')
    mail.send(message)
    return 'success'


@bp.route('/profile')
@login_required
def profile():
    return render_template('cms/cms_profile.html')


@bp.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('cms.login'))


@bp.route('/')
@login_required
def index():
    return render_template('cms/cms_index.html')


class LoginView(views.MethodView):

    def get(self, message=None):
        return render_template('cms/cms_login.html', message=message)

    def post(self):
        form = LoginForm(request.form)

        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            remember = form.remember.data
            user = CMSUser.query.filter_by(email=email).first()

            if user and user.check_password(password):
                session['user_id'] = user.id
                if remember:
                    # 设置session过期时间，默认31天
                    session.permanent = True
                return redirect(url_for('cms.index'))
            else:
                message = '邮箱或密码错误'
                return self.get(message=message)
        else:
            # 如果验证失败, 刷新登录页面
            message = form.get_error()
            print(message)
            return self.get(message=message)


class ResetPwdView(views.MethodView):

    decorators = [login_required]

    def get(self):
        return render_template('cms/cms_resetpwd.html')

    def post(self):
        form = ResetPwdForm(request.form)

        if form.validate_on_submit():
            oldpwd = form.oldpwd.data
            newpwd = form.newpwd.data
            user = g.cms_user
            if user.check_password(oldpwd):
                user.password = newpwd
                db.session.commit()
                # return jsonify({'code': 200, 'message': 'ok'})
                return restful.success(message='ok')
            else:
                # return jsonify({'code': 400, "message": message})
                return restful.params_error(message='旧密码错误')
        else:
            # message = form.get_error()
            # return jsonify({'code': 400, "message": message})
            return restful.params_error(form.get_error())


class ResetEmailView(views.MethodView):

    decorators = [login_required]

    def get(self):
        return render_template('cms/cms_resetemail.html')

    def post(self):
        form = ResetEmailForm(request.form)
        if form.validate():
            email = form.email.data
            g.cms_user.email = email
            db.session.commit()
            return restful.success('修改邮箱成功')
        else:
            return restful.params_error(form.get_error())


bp.add_url_rule('/login/', view_func=LoginView.as_view('login'))
bp.add_url_rule('/resetpwd/', view_func=ResetPwdView.as_view('resetpwd'))
bp.add_url_rule('/resetemail/', view_func=ResetEmailView.as_view('resetemail'))