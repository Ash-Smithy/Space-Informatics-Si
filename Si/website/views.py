from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json 

#to make this file a blueprint
views = Blueprint('views', __name__)

#to navigate to home page if logged in
@views.route('/home',methods=['GET','POST'])
@login_required
def home():
    return render_template("index.html", user = current_user)

#to navigate to welcome page if not logged in
@views.route('/welcome')
@views.route('/')
def welcome(user = current_user):
    if user.is_authenticated:
        return render_template("index.html",user = current_user)
    else:
        return render_template("welcome.html", user = current_user)

#navigate to notes page
@views.route('/notes', methods=['GET', 'POST'])
@login_required
def notes():
    if request.method == 'POST': 
        note = request.form.get('note')#Gets the note from the HTML 

        if len(note) < 1:
            flash('Note is too short!', category='error') 
        else:
            new_note = Note(data=note, user_id=current_user.id)  #providing the schema for the note 
            db.session.add(new_note) #adding the note to the database 
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("notes.html", user=current_user)

#to delete a note
@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

