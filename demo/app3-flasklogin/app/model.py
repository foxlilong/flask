from datetime import datetime
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    balance = db.Column(db.Float(), default=0.0)
    is_overdue = db.Column(db.Boolean, default=False)
    remark = db.Column(db.String(64), default=u'正常')
    password_hash = db.Column(db.String(64))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    # user_name = db.relationship('Payslip', backref='user_name', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<user: {}>'.format(self.username)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post: {}>'.format(self.body)


class Payslip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    balance = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('user.username'))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return '<payslip: {}>'.format(self.username)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
