from database import db
from sqlalchemy import  ForeignKey
from sqlalchemy.orm import  relationship


class Track(db.Model):
    __tablename__ = 'seguimiento'
    
    id_seguimiento = db.Column(db.Integer(), primary_key = True, autoincrement = True)
    fecha = db.Column(db.Date(), nullable = False)
    estado = db.Column(db.String(20), nullable = False)
    descripcion = db.Column(db.String(100))
    Pedido_id_pedido = db.Column(db.Integer(), ForeignKey("pedido.id_pedido"))
    
    pedido = relationship('Order')