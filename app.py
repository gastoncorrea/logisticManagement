from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_mail import Mail
from database import db
import os
from dotenv import load_dotenv
from models.__init__ import Client, Shipping, Rider, Order, OrderDetail,Track
from services.filterData import filterData
from services.saveData import saveDataDb
from services.sendMail import mail, send_mail_delivered,send_mail_not_delivered
from services.saveShipping import saveShippingData
from datetime import datetime



app = Flask(__name__)

load_dotenv(override=True)  # Carga las variables del .env

from pathlib import Path
print("📁 Working directory:", Path.cwd())
print(".env exists:", Path(".env").exists())

MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")
MAIL_SERVER = os.getenv("MAIL_SERVER")
DATABASE_URL = os.getenv("DATABASE_URL")

print("📦 MAIL_SERVER:", os.getenv("MAIL_SERVER"))
print("📦 MAIL_USERNAME:", os.getenv("MAIL_USERNAME"))
print("📦 MAIL_PASSWORD:", "SET" if os.getenv("MAIL_PASSWORD") else "NOT SET")
print("📦 DATABASE_URL:", os.getenv("DATABASE_URL"))



app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
# Configuración del servidor SMTP
app.config["MAIL_SERVER"] = MAIL_SERVER
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = MAIL_USERNAME
app.config["MAIL_PASSWORD"] = MAIL_PASSWORD
app.config["MAIL_DEFAULT_SENDER"] = MAIL_DEFAULT_SENDER
db.init_app(app)

CORS(app, resources= {
    r"/upload": {"origins": "https://skyflexshipping.netlify.app"}
})

print("DEBUG MAIL CONFIG:")
print("MAIL_SERVER:", app.config["MAIL_SERVER"])
print("MAIL_USERNAME:", app.config["MAIL_USERNAME"])
print("MAIL_PASSWORD:", "SET" if app.config["MAIL_PASSWORD"] else "NOT SET")

mail.init_app(app)



@app.route("/upload", methods=["POST"])
def uplodad_file():
   return saveDataDb(filterData(request))
  #return filterData(request)

@app.route('/pedidos/<estado>', methods=['GET'])
def recuper_pedidos(estado):
    mis_datos = Track.query.all()
    
    # Inicializamos las listas para cada estado
    no_entregados = []
    entregados = []
    en_camino = []
    en_proceso = []

    # Función para verificar si un pedido ya está en alguna lista
    def pedido_existe(id_pedido):
        return any(p['id_pedido'] == id_pedido for p in no_entregados + entregados + en_camino + en_proceso)

    for registro in mis_datos[::-1]:
        pedido = registro.pedido
        estado_registro = registro.estado.lower()

        # Si el pedido ya está en alguna lista, lo ignoramos
        if pedido_existe(pedido.id_pedido):
            continue

        pedido_data = {
            'id_pedido': pedido.id_pedido,
            'nro_pedido': pedido.nro_pedido,
            'fecha': pedido.fecha.strftime('%Y-%m-%d'),
            'nombre_cliente': pedido.cliente.nombre,
            'email': pedido.cliente.email,
            'provincia': pedido.ubicacion.provincia,
            'direccion': pedido.ubicacion.direccion,
            'cp': pedido.ubicacion.codigo_postal,
            'estado': registro.estado
        }

        if estado_registro == "no entregado":
            not_delivered_data = {
                "id_pedido": pedido.id_pedido,
                "nro_pedido": pedido.nro_pedido,
                "fecha_devolucion": registro.fecha,
                "rider_nombre": registro.id_rider,
                "descripcion_entrega": registro.descripcion, 
                "estado": estado_registro
            }
            no_entregados.append(not_delivered_data)
        elif estado_registro == "entregado":
            delivered_data = {
                "id_pedido": pedido.id_pedido,
                "nro_pedido": pedido.nro_pedido,
                "fecha_entrega": registro.fecha,
                "recibe_dni": registro.entrega_dni,
                "recibe_nombre": registro.entrega_nombre,
                "rider_nombre": registro.riders.email,
                "descripcion_entrega": registro.descripcion,
                "estado": estado_registro
            }
            entregados.append(delivered_data)
        elif estado_registro == "en camino":
            lista_envios = Shipping.query.filter_by(id_pedido=pedido.id_pedido).first()
            pedido = lista_envios.pedido
            datos_envio = {
                "id_pedido": pedido.id_pedido,
                "nro_pedido": pedido.nro_pedido,
                "fecha_envio": lista_envios.fecha,
                "rider": lista_envios.rider.email,
                "direccion": pedido.ubicacion.direccion,
                "codigo_postal": pedido.ubicacion.codigo_postal,
                "estado": registro.estado
            }
            en_camino.append(datos_envio)
            mis_datos.remove(registro)
        elif estado_registro == "en proceso":
            en_proceso.append(pedido_data)
            mis_datos.remove(registro)
            
    no_entregados = sorted(no_entregados, key=lambda x: x['id_pedido'])
    entregados = sorted(entregados, key=lambda x: x['id_pedido'])
    en_camino = sorted(en_camino, key=lambda x: x['id_pedido'])
    en_proceso = sorted(en_proceso, key=lambda x: x['id_pedido'])

    listas = {
        "in-progress": sorted(en_proceso, key=lambda x: x['id_pedido']),
        "sent": sorted(en_camino, key=lambda x: x['id_pedido']),
        "delivered": sorted(entregados, key=lambda x: x['id_pedido']),
        "not-delivered": sorted(no_entregados, key=lambda x: x['id_pedido'])
        }

    # Retorna la lista correspondiente o un error si el estado no es válido
    if estado in listas:
        return jsonify(listas[estado])
    else:
        return jsonify({"error": "Estado no válido"}), 400

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

@app.route('/riders/get')
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
            'vehiculo': rider.vehiculo
        })
    return jsonify(riders)   
        
@app.route('/shipping', methods=['POST'])
def create_shipping():
    print(request)
    # Obtener los datos enviados desde el frontend
    data = request.get_json()

    return saveShippingData(data)

@app.route('/shipping/data/<int:id>')
def detalle_envio(id):
    envio = Shipping.query.filter_by(id_pedido = id).first()
    envio_encontrado = {
        "id_envio": envio.id_envio,
        "fecha_envio": envio.fecha,
        "rider": envio.rider.email,
        "provincia": envio.pedido.ubicacion.provincia,
        "direccion": envio.pedido.ubicacion.direccion,
        "codigo_postal": envio.pedido.ubicacion.codigo_postal,
    }
    return jsonify(envio_encontrado)

@app.route('/shipping/find/<int:id>')
def find_shipping(id):
    shipping = Shipping.query.filter_by(id_envio = id).first()
    if not shipping:
        return jsonify({'error':'No existe el registro'})
    one_shipping = {
        "id_rider": shipping.rider.id_rider,
        "rider": shipping.rider.email,
        "nro_pedido": shipping.pedido.nro_pedido
    }
    
    return jsonify(one_shipping)

@app.route('/riders/save', methods=['POST'])
def create_rider():
    rider = request.get_json()
    
    save_rider = Rider(
        nombre = rider['nombre'],
        apellido = rider['apellido'],
        email = rider['email'],
        dni = rider['dni'],
        vehiculo = rider['vehiculo'],
        cedula_verde = rider['cedula']
    )
    db.session.add(save_rider)
    db.session.commit()
    
    return jsonify({'message': 'Rider creado exitosamente', 'id_rider': save_rider.id_rider}), 201

@app.route('/riders/shipping/<int:id>')
def pedido_enviado_por_rider(id):
    orders = Shipping.query.filter_by(id_rider=id).all()
    print("Id pedido",id)
    print("Lista de envios:", orders)
    orders_finded = []
    
    for order in orders:
        orders_finded.append({
            'nro_pedido': order.pedido.nro_pedido,
            'provincia': order.pedido.ubicacion.provincia,
            'codigo_postal': order.pedido.ubicacion.codigo_postal
        })
        
    return jsonify(orders_finded)

@app.route('/delivered/save', methods=['POST'])
def crear_entrega_pedido():
    datos_entrega = request.get_json()
    print(datos_entrega)
    if not datos_entrega['entrega_dni'] or not datos_entrega['entrega_nombre'] or not datos_entrega['entrega_rider']:
        return jsonify({'error':'Campos requeridos faltantes'}), 400
    
    order = Order.query.filter_by(nro_pedido = datos_entrega['nro_pedido']).first()
    if not order:
        return jsonify({'error':'Pedido no encontrado'}), 404
    
    rider = Rider.query.filter_by(id_rider = datos_entrega['entrega_rider']).first()
    if not rider:
        return jsonify({'error':'Rider no encontrado'}),404
    
    guardar_entrega = Track(
        fecha = datetime.now(),
        estado = "Entregado",
        entrega_dni = datos_entrega['entrega_dni'],
        entrega_nombre = datos_entrega['entrega_nombre'],
        descripcion = datos_entrega['descripcion'],
        id_rider = rider.id_rider,
        Pedido_id_pedido = order.id_pedido
    )
    db.session.add(guardar_entrega)
    envio = send_mail_delivered(order, guardar_entrega)
    db.session.commit()
    
    return jsonify({'message':'Entrega creada con exito', 'email': envio}), 201

@app.route('/delivered/not/save', methods=['POST'])
def crear_devolucion_pedido():
    datos_entrega = request.get_json()
    print(datos_entrega)
    if not datos_entrega['descripcion'] or not datos_entrega['entrega_rider'] or not datos_entrega['nro_pedido']:
        return jsonify({'error':'Campos requeridos faltantes'}), 400
    
    order = Order.query.filter_by(nro_pedido = datos_entrega['nro_pedido']).first()
    if not order:
        return jsonify({'error':'Pedido no encontrado'}), 404
    
    rider = Rider.query.filter_by(id_rider = datos_entrega['entrega_rider']).first()
    if not rider:
        return jsonify({'error':'Rider no encontrado'}),404
    
    guardar_entrega = Track(
        fecha = datetime.now(),
        estado = "No entregado",
        descripcion = datos_entrega['descripcion'],
        id_rider = rider.id_rider,
        Pedido_id_pedido = order.id_pedido
    )
    db.session.add(guardar_entrega)
    envio = send_mail_not_delivered(order, guardar_entrega)
    db.session.commit()
    
    return jsonify({'message':'Devolucion creada con exito', 'email': envio}), 201
    

with app.app_context():
    db.create_all()