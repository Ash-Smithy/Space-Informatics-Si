from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

#for the user notes
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True,), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

#for the user data
class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique = True)
    password = db.Column(db.String(150))
    name = db.Column(db.String(150))
    notes = db.relationship('Note')
    user_data = db.relationship('Conversations', backref='user')
    bot_data = db.relationship('Bot', backref='user')
 
#for user inputs while interacting with bot
class Conversations(db.Model):
    __tablename__ = 'conversations'
    id = db.Column(db.Integer,primary_key=True)
    user_inp = db.Column(db.String(200))
    u_id = db.Column(db.Integer, db.ForeignKey('user.id'))

#for the bot responses
class Bot(db.Model):
    __tablename__ = 'bot'
    id = db.Column(db.Integer,primary_key=True)
    user_input = db.Column(db.String(200), db.ForeignKey('conversations.user_inp'))
    bot_res = db.Column(db.String(200))    
    u_id = db.Column(db.Integer, db.ForeignKey('user.id'))
