from database import db

class Product(db.Model):

    __tablename__ = 'producto'

    id_producto = db.Column(db.Integer, primary_key=True, autoincrement = True)
    nombre_producto = db.Column(db.String(100), nullable=False)