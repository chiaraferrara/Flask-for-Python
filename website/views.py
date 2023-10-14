#urls defined = blueprint

from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)

#define view

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note').strip()  # Rimuovi gli spazi vuoti iniziali e finali

        if len(note) < 1:
            flash('La nota è troppo corta', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Aggiunta con successo', category='success')

    return render_template("home.html", user=current_user)
#nel template possiamo controllare se l'utente è autenticato


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data) #prende il request.data (la string noteId)
    noteId = note['noteId'] #la carica come json object (dizionario)
    note = Note.query.get(noteId)
    if note: #se esiste
        if note.user.id == current_user.id: #se l'utente che è loggato, elimineremo la nota.
            db.session.delete(note)
            db.session.commit()
    
    return jsonify({})