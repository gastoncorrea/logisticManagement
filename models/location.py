from database import db
from sqlalchemy.orm import  relationship

class Location(db.Model):
    __tablename__ = 'ubicacion'

    id_ubicacion = db.Column(db.Integer, primary_key=True,autoincrement = True)
    localidad = db.Column(db.String(100),nullable=False)
    direccion = db.Column(db.String(100),nullable=False)
    direccion2 = db.Column(db.String(100),nullable=True)
    codigo_postal = db.Column(db.String(15),nullable=False)

    #pedido = relationship('Order', back_populates='ubicacion')