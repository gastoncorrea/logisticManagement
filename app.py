from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_mail import Mail
from database import db
import os
from dotenv import load_dotenv
from models.__init__ import Client, Shipping, Rider, Order, OrderDetail,Track
from services.filterData import filterData
from services.saveData import saveDataDb
from services.sendMail import mail
from datetime import datetime



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

mail.init_app(app)



@app.route("/upload", methods=["POST"])
def uplodad_file():
   return saveDataDb(filterData(request))
  #return filterData(request)

@app.route('/')
def recuper_pedidos():
    mis_datos = Track.query.all()
    
    # Inicializamos las listas para cada estado
    no_entregados = []
    entregados = []
    en_camino = []
    en_proceso = []
    
    for registro in mis_datos[::-1]:
        pedido = registro.pedido
        estado = registro.estado.lower() 
        
        if estado == "no entregado":
                no_entregados.append({
                'id_pedido': pedido.id_pedido,
                'nro_pedido': pedido.nro_pedido,
                'fecha': pedido.fecha.strftime('%Y-%m-%d'),
                'nombre_cliente': pedido.cliente.nombre,
                'email': pedido.cliente.email,
                'provincia': pedido.ubicacion.provincia,
                'direccion': pedido.ubicacion.direccion,
                'cp': pedido.ubicacion.codigo_postal,
                'estado': registro.estado
                })
                mis_datos.remove(registro)
        elif estado == "entregado":
                entregados.append({
                'id_pedido': pedido.id_pedido,
                'nro_pedido': pedido.nro_pedido,
                'fecha': pedido.fecha.strftime('%Y-%m-%d'),
                'nombre_cliente': pedido.cliente.nombre,
                'email': pedido.cliente.email,
                'provincia': pedido.ubicacion.provincia,
                'direccion': pedido.ubicacion.direccion,
                'cp': pedido.ubicacion.codigo_postal,
                'estado': registro.estado
                })
                mis_datos.remove(registro)
        elif estado == "en camino":
                en_camino.append({
                'id_pedido': pedido.id_pedido,
                'nro_pedido': pedido.nro_pedido,
                'fecha': pedido.fecha.strftime('%Y-%m-%d'),
                'nombre_cliente': pedido.cliente.nombre,
                'email': pedido.cliente.email,
                'provincia': pedido.ubicacion.provincia,
                'direccion': pedido.ubicacion.direccion,
                'cp': pedido.ubicacion.codigo_postal,
                'estado': registro.estado
                })
                mis_datos.remove(registro)
        elif estado == "en proceso":
            en_proceso.append({
                'id_pedido': pedido.id_pedido,
                'nro_pedido': pedido.nro_pedido,
                'fecha': pedido.fecha.strftime('%Y-%m-%d'),
                'nombre_cliente': pedido.cliente.nombre,
                'email': pedido.cliente.email,
                'provincia': pedido.ubicacion.provincia,
                'direccion': pedido.ubicacion.direccion,
                'cp': pedido.ubicacion.codigo_postal,
                'estado': registro.estado
                })
            mis_datos.remove(registro)
        # Crear el diccionario final con las listas clasificadas
    resultados = {
        "no_entregados": no_entregados,
        "entregados": entregados,
        "en_camino": en_camino,
        "en_proceso": en_proceso
    }
    print(resultados)
    # Devolver los resultados en formato JSON
    return jsonify(resultados)

@app.route('/detail/<int:id>')
def recuperar_detalle_pedidos(id):
    detalle_pedido = OrderDetail.query.filter_by(Pedido_id_pedido=id).all()
    detalle = [{'id_detalle_pedido': orderDetail.id_Detalle_Pedido, 'producto': orderDetail.producto.nombre_producto, 'cantidad': orderDetail.cantidad} for orderDetail in detalle_pedido]
    return jsonify(detalle)

@app.route('/order/<int:id>')
def recuperar_un_pedido(id):
    pedido = Order.query.filter_by(id_pedido=id).first()
    enviar_pedido = {
        'id_pedido': pedido.id_pedido,
        'nro_pedido': pedido.nro_pedido
    }
    return jsonify(enviar_pedido)

@app.route('/riders')
def recuperar_riders():
    find_riders = Rider.query.all()
    riders = []
    for rider in find_riders:
        riders.append({
            'id_rider': rider.id_rider,
            'nombre': rider.nombre,
            'apellido': rider.apellido,
            'email': rider.email,
            'dni': rider.dni,
        })
    return jsonify(riders)   
        
@app.route('/shipping', methods=['POST'])
def create_shipping():
    print(request)
    # Obtener los datos enviados desde el frontend
    data = request.get_json()

    # Validar si los campos requeridos están presentes
    if not data.get('fecha') or not data.get('nro_pedido') or not data.get('id_rider'):
        return jsonify({'error': 'Campos requeridos faltantes'}), 400   
     # Buscar el pedido correspondiente por 'nro_pedido'
    order = Order.query.filter_by(nro_pedido=data['nro_pedido']).first()
    if not order:
        return jsonify({'error': 'Pedido no encontrado'}), 404 
    rider = Rider.query.filter_by(id_rider=data['id_rider']).first()
    if not rider:
        return jsonify({'error': 'Rider no encontrado'}), 404
    # Crear un nuevo envío
    shipping = Shipping(
        fecha=data['fecha'],
        id_pedido=order.id_pedido,
        id_rider=rider.id_rider,
        desde=data.get('desde', ''),  # Puedes ajustar según sea necesario
        hasta=data.get('hasta', 'cualquier lado')   # Puedes ajustar según sea necesario
    )
    track = Track(
        fecha = datetime.now(),
        estado = "En camino",
        Pedido_id_pedido = order.id_pedido
    )
    # Agregar a la base de datos y hacer commit
    db.session.add(shipping)
    db.session.add(track)
    db.session.commit()
     # Responder con un mensaje de éxito
    return jsonify({'message': 'Envío creado exitosamente', 'id_envio': shipping.id_envio}), 201
    
with app.app_context():
    db.create_all()