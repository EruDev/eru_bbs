from flask import g, session
from .models import CMSUser
from .views import bp


@bp.before_request
def before_request():
    if 'user_id' in session:
        user_id = session.get('user_id')
        user = CMSUser.query.get(user_id)
        if user:
            g.cms_user = user