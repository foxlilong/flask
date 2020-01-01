from flask import render_template, redirect, url_for, flash
from app import app, db
from werkzeug.security import generate_password_hash
from flask_login import current_user, login_user, logout_user
from app.forms import LoginForm, RegistrationForm
from app.model import User


@app.route('/')
@app.route('/index')
def index():
    print(app.url_map)
    return render_template('index.html', title="index")


@app.route('/login', methods=["get", "post"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash(u'用户或者密码错误')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        flash('Login requested for user={}, remember_me={}'.format(form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title="login", form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['get', 'post'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(u"注册成功!")
        return redirect(url_for('index'))
    return render_template('register.html', title=u"注册", form=form)
