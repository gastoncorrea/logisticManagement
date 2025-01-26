from app import db, ForeignKey, relationship

class Order(db.Model):
    __tablename__ = 'pedido'

    id_pedido = db.Column(db.Integer, primary_key = True)
    nro_pedido = db.Column(db.String(45), nullable = False) 
    fecha = db.Column(db.Date(), nullable = False) 
    id_cliente = db.Column(db.Integer(), ForeignKey("Cliente_id_cliente"))
    Ubicacion_id_ubicacion = db.Column(db.Integer(), ForeignKey("Ubicacion_id_cliente"))

    cliente = relationship('Cliente')
    ubicacion = relationship('Ubicacion')
    