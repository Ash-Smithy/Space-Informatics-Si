#modules to import
from flask import Blueprint,render_template, request, flash
from flask_login import current_user
from . import db
from .models import Conversations, Bot
from .bot_run import result

#to register this file as a blueprint
bot_bp = Blueprint('bot',__name__)


#to access bot page and have conversations with the chatbot
@bot_bp.route('/bot',methods=['GET', 'POST'])
def bot():
    if request.method == 'POST':
        userInp = request.form.get('userInp')
        if len(userInp) < 1:
            flash("Message cannot be blank!", category= 'error')
            return render_template("cbot.html", user = current_user)
        else:
            user_ip = Conversations(user_inp=userInp, u_id=current_user.id) 
            db.session.add(user_ip)
            db.session.commit()
            rep = result(userInp)
            bot_rep = Bot(user_input=userInp, bot_res=rep, u_id=current_user.id)
            db.session.add(bot_rep)
            db.session.commit()
    return render_template("cbot.html", user = current_user)
