'''HTTP request: cliccando submit nei vari form dirà "method not allowed", 
in base al tipo di richiesta servirà un metodo differente...

post request: cambiamento nello stato del database. sign up : 
mandiamo una post request con tutte le informazioni'''

from flask import Blueprint, render_template, request, flash, redirect,  url_for
from .models import User

'''import for password, converts password to something more secure, a hash.'''
from werkzeug.security import generate_password_hash, check_password_hash

from . import db

'''Se hai fatto l'accesso, ti serve solo vedere home e logout sopra, non ti serve più sign in e login...'''
from flask_login import login_user, login_required, logout_user, current_user
auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        '''filtra tutti gli user che hanno quella mail'''

        user = User.query.filter_by(email=email).first()

        if user:
            '''qualsiasi user che abbiamo trovato con e password che abbiamo ottenuto dal form'''
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category = 'success')
                login_user(user, remember=True) #ricorderà la sessione
                return redirect(url_for("views.home"))
            else:
                flash('La password è incorretta!', category = 'error')
        else:
            flash("L'user non esiste", category = 'error')
    data = request.form
    print(data)
    return render_template("login.html", user = current_user)

@auth.route('/logout')
@login_required #fa in modo che non si può accedere a ciò se non si è loggati prima. A che serve il logout se non hai ancora fatto il login?
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

@auth.route('/signup', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        
        if user:
            flash("C'è già un utente con questa email.", category='error')
        elif len(email)<4:
            '''message flash => Funzionalità di Flask'''
            flash('E-mail deve essere più lunga di 3 caratteri.', category='error')
        elif len(first_name)<2:
            flash('Il nome deve essere più lungo di 1 carattere.', category='error')
        
        elif password1 != password2:
            flash('Le password non combaciano.', category='error')
        
        elif len(password1) < 7:
            flash('La password deve essere almeno 7 caratteri.', category='error')
        
        else:
            new_user = User(email=email, first_name=first_name, password= generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True) #ricorderà la sessione COME IN LOGIN
            flash('Account creato con successo!', category='success')
            '''redirect'''
            return redirect(url_for("views.home"))
    return render_template("signup.html", user = current_user)