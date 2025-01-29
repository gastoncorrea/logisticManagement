from database import db
from sqlalchemy import  ForeignKey
from sqlalchemy.orm import  relationship


class Order(db.Model):
    __tablename__ = 'pedido'

    id_pedido = db.Column(db.Integer, primary_key = True, autoincrement = True)
    nro_pedido = db.Column(db.String(45), nullable = False, unique = True) 
    fecha = db.Column(db.Date(), nullable = False) 
    Cliente_id_cliente = db.Column(db.Integer(), ForeignKey("cliente.id_cliente"),nullable=False)
    Ubicacion_id_ubicacion = db.Column(db.Integer(), ForeignKey("ubicacion.id_ubicacion"),nullable=False)

    cliente = relationship('Client')
    ubicacion = relationship('Location')
    