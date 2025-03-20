from database import db
from sqlalchemy import  ForeignKey
from sqlalchemy.orm import  relationship

class Rider(db.Model):
    __tablename__ = 'riders'
    
    id_rider = db.Column(db.Integer, primary_key=True, autoincrement = True)
    nombre = db.Column(db.String(50), nullable = False)
    apellido = db.Column(db.String(50), nullable = False)
    email = db.Column(db.String(50), nullable = False, unique = True)
    dni = db.Column(db.String(50), nullable = False, unique = True)
    vehiculo = db.Column(db.String(50), nullable = False)
    cedula_verde = db.Column(db.String(50))