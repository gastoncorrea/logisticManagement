from database import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import  relationship

class OrderDetail(db.Model):

    __tablename__ = 'detalle_pedido'

    id_Detalle_Pedido = db.Column(db.Integer, primary_key=True, autoincrement = True)
    cantidad = db.Column(db.Integer, nullable=False)
    Producto_id_producto = db.Column(db.Integer, ForeignKey("producto.id_producto"))
    Pedido_id_pedido = db.Column(db.Integer, ForeignKey("pedido.id_pedido"))

    producto = relationship("Product", back_populates="detalles")