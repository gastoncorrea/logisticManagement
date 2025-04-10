from database import db
from sqlalchemy import  ForeignKey
from sqlalchemy.orm import  relationship

class Shipping(db.Model):
    __tablename__ = "envios"
    
    id_envio = db.Column(db.Integer, primary_key = True, autoincrement = True)
    fecha = db.Column(db.Date(), nullable = False)
    desde = db.Column(db.String(50))
    hasta = db.Column(db.String(50))    
    id_pedido = db.Column(db.Integer, ForeignKey("pedido.id_pedido"))
    id_rider = db.Column(db.Integer, ForeignKey("riders.id_rider"))
    
    pedido = relationship("Order")
    rider = relationship("Rider")