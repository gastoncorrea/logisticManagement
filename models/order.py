from database import db
from sqlalchemy import  ForeignKey
from sqlalchemy.orm import  relationship


class Order(db.Model):
    __tablename__ = 'pedido'

    id_pedido = db.Column(db.Integer, primary_key = True, autoincrement = True)
    nro_pedido = db.Column(db.String(45), nullable = False, unique = True) 
    fecha = db.Column(db.Date(), nullable = False) 
    id_cliente = db.Column(db.Integer(), ForeignKey("Cliente_id_cliente"),nullable=False)
    id_ubicacion = db.Column(db.Integer(), ForeignKey("Ubicacion_id_cliente"),nullable=False)

    cliente = relationship('Cliente')
    ubicacion = relationship('Ubicacion')
    