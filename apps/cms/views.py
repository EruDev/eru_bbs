# coding: utf-8
import os
from flask import Blueprint, views, render_template, request, session, redirect, url_for
from .forms import LoginForm
from .models import CMSUser
from .decorators import login_required


bp = Blueprint('cms', __name__, url_prefix='/cms')

@bp.route('/')
@login_required
def index():
    return 'cms index'


class LoginView(views.MethodView):

    def get(self, form=None):
        form = LoginForm()
        return render_template('cms/cms_login.html', form=form)

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
                return render_template('cms/cms_login.html', form=form, message='邮箱或密码错误')
        else:
            # 如果验证失败, 刷新登录页面
            message = form.errors.popitem()[1][0]
            print(message)
            return render_template('cms/cms_login.html', form=form, message=message)


bp.add_url_rule('/login/', view_func=LoginView.as_view('login'))