from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5

from app import login, db

class Groups(db.Model):
    group_id = db.Column(db.Integer, primary_key=True)
    gr_name = db.Column(db.String(64), index=True, unique=True)
    group_owner = db.Column(db.ForeignKey('users.user_id'),default=None)
    stud_year = db.Column(db.String(64))

    def __repr__(self):
        return '<Groups {}>'.format(self.gr_name)


class Parents(db.Model):
    #TODO надо подумать, скорее всего, таблица не пригодится
    link_id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.ForeignKey('users.user_id'),default=None)
    child_id = db.Column(db.ForeignKey('users.user_id'), default=None)

    def __repr__(self):
        return '<Parents {}>'.format(self.link_id)


class Users(UserMixin, db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    user_ = db.Column(db.String(64))
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(120), index=True, unique=True)
    role = db.Column(db.Integer, default=3) #0-default/1-user/2-admin/3-student/4-teacher/5-parent
    group_id = db.Column(db.ForeignKey('groups.group_id'), default=1)
    reg_time = db.Column(db.DateTime, index=True, default=datetime.now)
    last_visit_time = db.Column(db.DateTime, default=datetime.now)
    parent_email = db.Column(db.String(120), index=True)

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
    test_hidden = db.Column(db.Boolean, default=True)
    test_starts_number = db.Column(db.Integer, default=0)
    test_avg_result = db.Column(db.Float, default=0)
    def __repr__(self):
        return '<Tests {}>'.format(self.test_name)


class Test_started(db.Model):
    try_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey('users.user_id'))
    test_id = db.Column(db.ForeignKey('tests.test_id'))
    time_start = db.Column(db.DateTime, index=True, default=datetime.now)
    time_left = db.Column(db.Integer, default=235*60)
    time_end = db.Column(db.DateTime, index=True)
    ended = db.Column(db.Boolean, index=True, default=False)
    test_name = db.Column(db.String(64))
    #не смог удалить это поле в SQLite
    path = db.Column(db.String(64))
    for i in range(1, 28):
        locals()['task_'+str(i)] = db.Column(db.String(64))
    primary_mark = db.Column(db.Integer, default=0)
    final_mark = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<Tests_started {}>'.format(self.test_name)

class Videos(db.Model):
    v_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey('users.user_id'), default=1)
    v_link = db.Column(db.String(64)) #Ссылка на ролик
    v_name = db.Column(db.String(64))
    v_text = db.Column(db.String(128)) #описание видео
    v_date = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return '<Videos {}>'.format(self.v_name)

@login.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))
