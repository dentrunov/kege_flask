from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5

from app import login, db


class Groups(db.Model):
    group_id = db.Column(db.Integer, primary_key=True)
    gr_name = db.Column(db.String(64), index=True, unique=True)
    stud_year = (db.String(64))

    def __repr__(self):
        return '<Groups {}>'.format(self.gr_name)


class Users(UserMixin, db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    user_ = db.Column(db.String(64))
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(120), index=True, unique=True)
    role = db.Column(db.Integer, default=0) #0-default/1-user/2-admin/3-student/4-teacher/5-parent
    group_id = db.Column(db.ForeignKey('groups.group_id'), default=1)
    reg_time = db.Column(db.DateTime, index=True, default=datetime.now)
    last_visit_time = db.Column(db.DateTime, default=datetime.now)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.user_id)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Tests(db.Model):
    test_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey('users.user_id'), default=1)
    time_added = db.Column(db.DateTime, index=True, default=datetime.now)
    path = db.Column(db.String(64))
    test_name = db.Column(db.String(64))
    for i in range(1, 28):
        locals()['task_'+str(i)] = db.Column(db.String(64))

    def __repr__(self):
        return '<Tests {}>'.format(self.test_name)


class Test_started(db.Model):
    try_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey('users.user_id'), default=1)
    test_id = db.Column(db.ForeignKey('tests.test_id'), default=1)
    time_start = db.Column(db.DateTime, index=True, default=datetime.now)
    time_end = db.Column(db.DateTime, index=True)
    ended = db.Column(db.Boolean, index=True, default=False)
    path = db.Column(db.String(64))
    test_name = db.Column(db.String(64), index=True)
    for i in range(1, 28):
        locals()['task_'+str(i)] = db.Column(db.String(64))
    primary_mark = db.Column(db.Integer, default=0)
    final_mark = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<Tests_started {}>'.format(self.test_name)


@login.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))
