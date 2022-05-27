from app import db

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(64), index=True, unique=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(120), index=True, unique=True)
    role = db.Column(db.Integer, index=True, unique=True)
    group_id = db.Column(db.Integer, index=True, unique=True)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Groups(db.Model):
    group_id = db.Column(db.Integer, primary_key=True)
    gr_name = db.Column(db.String(64), index=True, unique=True)

    def __repr__(self):
        return '<Groups {}>'.format(self.username)