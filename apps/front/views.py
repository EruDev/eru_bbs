# coding: utf-8
from io import BytesIO

from flask import Blueprint, views, render_template, make_response
from utils.captcha.captcha_1 import gene_captcha

bp = Blueprint('front', __name__)

@bp.route('/')
def index():
    return 'front index'


@bp.route('/captcha')
def graph_captcha():
    gene_captcha()
    # image.save(out, 'png')
    # out.seek(0)
    # resp = make_response(out.read())
    # resp.content_type = 'image/png'
    return 1

class SignupView(views.MethodView):

    def get(self):
        return render_template('front/front_signup.html')

    def post(self):
        pass


bp.add_url_rule('/signup', view_func=SignupView.as_view('signup'))


