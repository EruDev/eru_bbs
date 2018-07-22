# coding: utf-8
import os
from flask import Blueprint, views, render_template, \
    request, session, redirect, url_for, g, jsonify
from .forms import LoginForm, ResetPwdForm
from .models import CMSUser
from .decorators import login_required
from exts import db
from apps.utils import restful


bp = Blueprint('cms', __name__, url_prefix='/cms')


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
        form = LoginForm()
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
            message = form.errors.popitem()[1][0]
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
                message = form.get_error()
                # return jsonify({'code': 400, "message": message})
                return restful.params_error(message=message)
        else:
            # message = form.get_error()
            # return jsonify({'code': 400, "message": message})
            return restful.params_error(form.get_error())


class ResetEmailView(views.MethodView):

    decorators = [login_required]

    def get(self):
        return render_template('cms/cms_resetemail.html')

    def post(self):
        pass


bp.add_url_rule('/login/', view_func=LoginView.as_view('login'))
bp.add_url_rule('/resetpwd/', view_func=ResetPwdView.as_view('resetpwd'))
bp.add_url_rule('/resetemail/', view_func=ResetEmailView.as_view('resetemail'))