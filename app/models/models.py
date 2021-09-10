from datetime import datetime
from __init__ import db, login_manager
from flask_login import UserMixin
import pytz


UTC = pytz.utc
Srb = pytz.timezone('Europe/Belgrade')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(120), unique=True)
    company = db.Column(db.String(120))
    email = db.Column(db.String(120), nullable=False, unique=True)
    subject = db.Column(db.String(120))
    description = db.Column(db.String(240))
    date = db.Column(db.String(120))
    time = db.Column(db.String(120))

    def __repr__(self):
        return f"Contact('{self.name}', '{self.phone}', '{self.company}', '{self.email}', '{self.subject}', '{self.description}', '{self.date}', '{self.time}')"

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(20), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}','{self.email}', '{self.password}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now(Srb))
    comment = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

# db.drop_all()