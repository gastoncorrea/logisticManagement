from database import db
from sqlalchemy.orm import  relationship

class Product(db.Model):

    __tablename__ = 'producto'

    id_producto = db.Column(db.Integer, primary_key=True, autoincrement = True)
    nombre_producto = db.Column(db.String(200), nullable=False)

    detalles = relationship("OrderDetail", back_populates = "producto")