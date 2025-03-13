from flask import Flask, jsonify, request
from flask_cors import CORS
from database import db
import os
from dotenv import load_dotenv
from models.__init__ import Client, Product, Location, Order, OrderDetail,Track
from services.filterData import filterData
from services.saveData import saveDataDb


app = Flask(__name__)

load_dotenv()  # Carga las variables del .env

MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/gestion_pedidos'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
# Configuración del servidor SMTP
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = MAIL_USERNAME
app.config["MAIL_PASSWORD"] = MAIL_PASSWORD
app.config["MAIL_DEFAULT_SENDER"] = MAIL_DEFAULT_SENDER
db.init_app(app)
CORS(app)


@app.route("/upload", methods=["POST"])
def uplodad_file():
   return saveDataDb(filterData(request))
  #return filterData(request)

@app.route('/')
def recuper_pedidos():
    mis_datos = Track.query.all()
    resultados = []
    for registro in mis_datos:
        if registro.estado == "En proceso":
            resultados.append({
                'id_pedido' : registro.pedido.id_pedido,
                'nro_pedido' : registro.pedido.nro_pedido,
                'fecha' : registro.pedido.fecha.strftime('%Y-%m-%d'),
                'nombre_cliente' : registro.pedido.cliente.nombre,
                #'email':registro.cliente.email,
                'provincia' : registro.pedido.ubicacion.provincia,
                'direccion': registro.pedido.ubicacion.direccion,
                'cp': registro.pedido.ubicacion.codigo_postal,
                'estado': registro.estado
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