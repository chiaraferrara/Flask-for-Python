from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from sqlite3 import dbapi2 as sqlite
import os
from flask_login import LoginManager

db = SQLAlchemy() #oggetto che useremo quando creeremo un nuovo user.
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '800A800BSUCA'
    BASE_DIR = os.path.abspath(os.path.dirname(__file__)) # Ottiene il percorso assoluto della directory del file corrente
    DB_PATH = os.path.join(BASE_DIR, DB_NAME) # Combina il percorso della directory con il nome del file del database
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}' # Configura il percorso completo del database

    #il mio sqlalchemy database è a quella locazione.

    #inizializziamo il database: prende il database e gli assegna l'app.
    db.init_app(app)
  

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    #creazione del database, ogni volta controlla se il database è creato
    from .models import User, Note
    #dobbiamo essere sicuri che legga questo file.
    with app.app_context(): #assicura che il codice all'interno del blocco venga eseguito con un contesto dell'applicazione correttamente configurato
        create_database(app)

    login_manager = LoginManager()
    '''dove ci reindirizza flask se non siamo loggati?'''
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id)) #cerca la primary key, stiamo cercando un user
    
    return app  #flask application che inizializza un secret key.

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all()
        print('Created Database!')