from functools import wraps
from flask import abort,session,redirect,url_for,flash
# from app import login_manager
# from .models import User



def loggedin_required(f):
    @wraps(f)
    def decorated_function(*args,**kwargs):
        # print(session)
        # print('userid' in session)
        if ('userid'in session):
            return f(*args, **kwargs)
        flash("需要先登录")
        return redirect(url_for('ctr.log_user_in'))

    return decorated_function

