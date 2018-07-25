from flask import g, session
from .models import CMSUser, CMSPermission
from .views import bp


@bp.before_request
def before_request():
    if 'user_id' in session:
        user_id = session.get('user_id')
        user = CMSUser.query.get(user_id)
        if user:
            g.cms_user = user


@bp.context_processor
def cms_context_processor():
    return {"CMSPermission": CMSPermission}