
from database import db

class Client(db.Model):
    __tablename__ = 'cliente'

    id_cliente = db.Column(db.Integer, primary_key = True, autoincrement = True)
    nombre = db.Column(db.String(100), nullable = False) 
    email = db.Column(db.String(100), nullable = False, unique = True) 
    telefono = db.Column(db.String(13), nullable = False)
