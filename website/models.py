#qui creiamo il modello di database => from . significa "da questo package"

from . import db 
from flask_login import UserMixin #flask login
from sqlalchemy.sql import func


class Note(db.Model):
    '''default, quando si aggiunge un oggetto il software è abbastanza
    intelligente da aggiungere un ID e sono sempre unici.'''
    
    id = db.Column(db.Integer, primary_key= True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())#quando creiamo una nota aggiungerà automaticamente la data con func.now()
    #tutte le note appartengono ad un user, come associare:
    '''Abbiamo bisogno di:
    - FOREIGN KEY: informazioni differenti devono essere associate a user differenti
        ogni user ha diverse note.
        La foreign key è una key che fa riferimento ad una key di una diversa colonna.
        è una colonna nel database che fa riferimento ad un'altra colonna.'''
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) 
    '''Passiamo l'id valido di un user esistente in questo campo
    ONE TO MANY RELATIONSHIP => un oggetto che ha molte notes. '''

class User(db.Model, UserMixin):
    '''layout per gli object da salvare nel database
    
    Quando si crea un oggetto abbiamo bisogno di:
    -PRIMARY KEY: modo unico di identificare l'oggetto. Tipicamente un INT.
    
    Bisogna specificare la lunghezza della stringa (150)
    '''

    id = db.Column(db.Integer, primary_key=True)
    email= db.Column(db.String(150),unique=True) #nessun user può avere la stessa mail.
    password = db.Column(db.String(20))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')
    