from app import app,lm
from app.models.forms import LoginForm
from flask_login import login_user,login_required,current_user,logout_user
from flask import render_template,redirect,url_for,jsonify,flash,session
from app.models.tables import SysUser
from datetime import timedelta

@lm.user_loader
def load_user(id):
    return SysUser.query.filter_by(id=id).first()

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        usr = SysUser.query.filter_by(username=form.userName.data,senha=form.password.data).first()
        if usr:
            if usr.ativo:
                login_user(usr)
                return redirect(url_for("index"))
            else:
                flash("Usuário Inativo, por favor contate um administrador!")
        else:
            flash("Login e(ou) senha invalido(s)!",'danger')

    flash("Login e(ou) senha invalido(s)!",'danger')
    return render_template("login.html",form=form,user=current_user)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@lm.unauthorized_handler
def unauthorized():
    return redirect(url_for("login"))


from datetime import timedelta

@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=30)
