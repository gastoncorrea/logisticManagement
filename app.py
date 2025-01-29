from flask import Flask, jsonify, request
from database import db
from models.__init__ import Client, Product, Location, Order, OrderDetail
from services.filterData import filterData
from services.saveData import saveDataDb

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/gestion_pedidos'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
db.init_app(app)


@app.route("/upload", methods=["POST"])
def uplodad_file():
   return saveDataDb(filterData(request))
  #return filterData(request)

@app.route('/')
def recuper_pedidos():
    mis_datos = Order.query.all()
    resultados = []
    for registro in mis_datos:
        resultados.append({
            'id_pedido' : registro.id_pedido,
            'nro_pedido' : registro.nro_pedido,
            'fecha' : registro.fecha,
            'id_cliente' : registro.Cliente_id_cliente,
            'id_ubicacion' : registro.Ubicacion_id_ubicacion,
            }
        )
    return jsonify(resultados)

@app.route('/<int:id>')
def recuperar_detalle_pedidos(id):
    detalle_pedido = OrderDetail.query.filter_by(Pedido_id_pedido=id).all()
    detalle = [{'id_detalle_pedido': orderDetail.id_Detalle_Pedido, 'id_producto': orderDetail.Producto_id_producto, 'cantidad': orderDetail.cantidad} for orderDetail in detalle_pedido]
    return jsonify(detalle)
with app.app_context():
    db.create_all()