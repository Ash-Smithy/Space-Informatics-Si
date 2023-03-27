from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True,), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique = True)
    password = db.Column(db.String(150))
    name = db.Column(db.String(150))
    notes = db.relationship('Note')
    user_data = db.relationship('Conversations')
    bot_data = db.relationship('Bot')

class Conversations(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    user_inp = db.Column(db.String(200))
    u_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Bot(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    user_input = db.Column(db.String(200), db.ForeignKey('conversations.user_inp'))
    bot_res = db.Column(db.String(200))
    u_id = db.Column(db.Integer, db.ForeignKey('user.id'))
