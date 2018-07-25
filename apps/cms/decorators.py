from functools import wraps
from flask import session, redirect, url_for, g

def login_required(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if 'user_id' in session:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('cms.login'))
    return inner


def permission_required(permission):
    def outter(func):
        @wraps(func)
        def inner(*args, **kwargs):
            if g.cms_user.has_permission(permission):
                return func(*args, **kwargs)
            else:
                return redirect(url_for('cms.index'))
        return inner
    return outter