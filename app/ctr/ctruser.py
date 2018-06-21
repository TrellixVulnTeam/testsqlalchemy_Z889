from . import ctr
from ..models import User
from .forms import LoginForm
from flask import  render_template

@ctr.route('/router2')
def show_user():
    print('router-user')
    users=User.query.all()
    return render_template('showusers2.html',users=users)


@ctr.route('/login2', methods=[ 'GET', 'POST'])
def login_user_in():
    print('login2')
    form=LoginForm()
    if form.validate_on_submit():
        # print('welcome')
        return render_template('welcome.html')
    # return "invalid"
    return render_template('login_form.html',form=form)

