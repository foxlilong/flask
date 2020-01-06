from flask import render_template, redirect, url_for, flash, request
from app import app, db
from werkzeug.security import generate_password_hash
from werkzeug.urls import url_parse
from flask_login import current_user, login_user, logout_user, login_required
from app.forms import LoginForm, RegistrationForm, PayslipForm
from app.model import User, Payslip
from sqlalchemy.sql import func
from sqlalchemy import desc


@app.route('/')
@app.route('/index')
def index():
    print(app.url_map)
    # data = Payslip.query.filter_by()
    data = db.session.query(User).order_by(desc(User.balance)).all()
    return render_template('index.html', title="index", data=data)


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
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
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
        flash(u"注册成功! %s" % user)
        login_user(user)
        return redirect(url_for('index'))
    return render_template('register.html', title=u"注册", form=form)


@app.route('/payslip', methods=['get', 'post'])
@login_required
def payslip():
    # if current_user.is_authenticated:
    #     return redirect(url_for('index'))
    form = PayslipForm()
    if form.validate_on_submit():
        slip = Payslip(username=form.username.data, balance=form.bal.data)
        db.session.add(slip)
        db.session.commit()

        amount = db.session.query(func.sum(Payslip.balance)).filter_by(username=form.username.data).all()[0][0]
        is_over = False
        remark = "正常"
        if amount < 0:
            is_over = True
            remark = "欠费"
        db.session.query(User).filter(User.username == form.username.data).update(
            {'balance': amount, 'is_overdue': is_over, 'remark': remark})
        db.session.commit()

        flash(u"充值成功! 用户:%s,  充值金额:%s " % (form.username.data, form.bal.data))
        return redirect(url_for('payslip'))
    return render_template('payslip.html', title=u"充值", form=form)
