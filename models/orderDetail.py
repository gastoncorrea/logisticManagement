from app import db, ForeignKey

class OrderDetail(db.Model):

    __tablename__ = 'detalle_pedido'

    id_detalle_pedido = db.column(db.Integer, primary_key=True, autoincrement = True)
    cantidad = db.Column(db.Integer, nullable=False)
    id_producto = db.Column(db.Integer, ForeignKey("Producto_id_producto"))
    id_pedido = db.Column(db.Integer, ForeignKey("Pedido_id_pedido"))