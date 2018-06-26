from flask import render_template,url_for,redirect,flash,session,request
# from flask_login import login_user,logout_user,current_user,login_required
from .forms import LoginForm,RegistrationForm,AddOprForm,EditOprForm,EditReworkOprForm
from ..models import Opr,Material,User
from . import ctr
from ..__init__ import db
from ..decorators import loggedin_required
from main_config import oprenum,Oprenum
import datetime

@ctr.route('/login', methods=['GET', 'POST'])
def log_user_in():
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(user_name=form.username.data).first()
        if user == None:
            flash("用户不存在")
            return redirect(url_for('ctr.log_user_in'))
        elif not user.verify_pass(password=form.userpass.data):
            flash("密码不正确")
            return redirect(url_for('ctr.log_user_in'))
        else:
            # login_user(user)
            # next = request.args.get('next')
            # if next is None or not next.startswith('/'):
            #     return redirect(url_for('ctr.welcome_user'))
            # print(session)
            session['userid'] = user.user_id
            session['username'] = user.user_name
            session['userpass'] = user.user_pass
            flash("登录成功")
            return redirect(url_for('ctr.welcome_user'))
    else:
        flash("需要登录")
    return render_template('login_form.html',form=form)

@ctr.route('/registration', methods=['GET', 'POST'])
def register():
    form=RegistrationForm()
    if form.validate_on_submit():
        if User.query.filter_by(user_name=form.username.data).first() == None:
            u=User(user_name=form.username.data,user_pass=form.userpass.data)
            db.session.add(u)
            db.session.commit()
            flash('账户创建成功')
            return redirect(url_for('ctr.log_user_in'))
        else:
            flash('账户已存在')
    else:
        flash('需要注册')
    return render_template('registration_form.html',form=form)




@ctr.route('/_add_opr', methods=['GET', 'POST'])
@loggedin_required
def add_material():
    form=AddOprForm()
    if form.validate_on_submit():
        # if session['userid'] != None:
        if Material.query.filter_by(material_name=form.materialname.data).first()== None:
            m=Material(material_name=form.materialname.data, countnum=form.countnum.data)
            db.session.add(m)
            db.session.commit()
            m= Material.query.filter_by(material_name=form.materialname.data).first()
            o=Opr(material_id=m.material_id,diff=form.countnum.data,user_id=session['userid'],oprtype=oprenum[Oprenum.INITADD], \
                    momentary = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") )
            db.session.add(o)
            db.session.commit()
            flash('新材料添加成功')
            return redirect(url_for('ctr.show_materials'))
        else:
            flash('材料名已存在')
        # else:
        #     flash('Your need logged in')
        #     return redirect(url_for('ctr.login_user_in'))
    else:
        flash('需要添加新材料')
    return render_template("_edit_opr_form.html", form=form)


@ctr.route('/_edit_opr/<materialid>', methods=['GET', 'POST'])
@loggedin_required
def change_countnum(materialid):
    form=EditOprForm()
    if form.validate_on_submit():
        m=Material.query.filter_by(material_id=materialid).first()
        if m.isvalid_opr(form.diff.data):
            oprtype =oprenum[Oprenum.INBOUND] if form.diff.data>0 else oprenum[Oprenum.OUTBOUND]
            o=Opr(material_id=materialid, diff=form.diff.data, user_id=session['userid'],oprtype=oprtype,\
                  momentary=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") )
            db.session.add(o)
            db.session.commit()
            m.change_countnum(form.diff.data)
            flash('材料数量更新成功')
            return redirect(url_for('ctr.show_materials'))
        else:
            flash("减少的数量超标")
    else:
        flash('需要填写数量')
    return render_template("_edit_opr_form.html", form=form)


@ctr.route('/_edit_rework_opr/<materialid>', methods=['GET', 'POST'])
@loggedin_required
def change_reworknum(materialid):
    form=EditReworkOprForm()
    if form.validate_on_submit():
        m=Material.query.filter_by(material_id=materialid).first()
        if m.isvalid_rework_opr(form.diff.data):
            oprtype =oprenum[Oprenum.REWORK] if form.diff.data>0 else oprenum[Oprenum.DELIVERY]
            o=Opr(material_id=materialid, diff=form.diff.data, user_id=session['userid'],oprtype=oprtype,\
                  momentary=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") )
            db.session.add(o)
            db.session.commit()
            m.change_reworknum(form.diff.data)
            flash('返修数量更新成功')
            return redirect(url_for('ctr.show_materials'))
        else:
            flash("减少的数量超标")
    else:
        flash('需要填写数量')
    return render_template("_edit_opr_form.html", form=form)


# @ctr.route('/change-password', methods=['GET', 'POST'])
# @login_required
# def change_password():
#     form = ChangePasswordForm()
#     if form.validate_on_submit():
#         if current_user.verify_password(form.old_password.data):
#             current_user.password = form.password.data
#             db.session.add(current_user)
#             db.session.commit()
#             flash('Your password has been updated.')
#             return redirect(url_for('main.index'))
#         else:
#             flash('Invalid password.')
#     return render_template("auth/change_password.html", form=form)

