from database import db, ForeignKey

class Product(db.Model):

    __tablename__ = 'producto'

    id_producto = db.column(db.Integer, primary_key=True)
    nombre_producto = db.Column(db.String(100), nullable=False)