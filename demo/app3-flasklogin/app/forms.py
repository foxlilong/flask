from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, BooleanField, SubmitField, FloatField
from wtforms.validators import DataRequired, InputRequired, EqualTo, ValidationError
from app.model import User


class LoginForm(FlaskForm):
    username = StringField(label=u"用户名", validators=[DataRequired()])
    password = PasswordField(label=u"密 码 ", validators=[DataRequired()])
    remember_me = BooleanField(label=u"记住我")
    submit = SubmitField(u"提交")


class RegistrationForm(FlaskForm):
    username = StringField(label=u"用户名", validators=[DataRequired()])
    password = PasswordField(label=u"密 码 ", validators=[DataRequired()])
    password2 = PasswordField(label=u"重复密码 ", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(u"注册")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('用户名存在')


class PayslipForm(FlaskForm):
    username = StringField(label=u"用户名", validators=[DataRequired()])
    bal = FloatField(label=u"充值金额 ", validators=[DataRequired()])
    submit = SubmitField(u"提交")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is None:
            raise ValidationError('用户名不存在')