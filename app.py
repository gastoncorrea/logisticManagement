from flask import Flask, jsonify, request
from flask_cors import CORS
from database import db
from models.__init__ import Client, Product, Location, Order, OrderDetail
from services.filterData import filterData
from services.saveData import saveDataDb


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/gestion_pedidos'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
db.init_app(app)
CORS(app)


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
                'fecha' : registro.fecha.strftime('%Y-%m-%d'),
                'nombre_cliente' : registro.cliente.nombre,
                'email':registro.cliente.email,
                'telefono':registro.cliente.telefono,
                'localidad' : registro.ubicacion.localidad,
                'direccion': registro.ubicacion.direccion,
                'direccion2': registro.ubicacion.direccion2,
                'cp': registro.ubicacion.codigo_postal
                }
            )
    return jsonify(resultados)

@app.route('/<int:id>')
def recuperar_detalle_pedidos(id):
    detalle_pedido = OrderDetail.query.filter_by(Pedido_id_pedido=id).all()
    detalle = [{'id_detalle_pedido': orderDetail.id_Detalle_Pedido, 'producto': orderDetail.producto.nombre_producto, 'cantidad': orderDetail.cantidad} for orderDetail in detalle_pedido]
    return jsonify(detalle)
with app.app_context():
    db.create_all()