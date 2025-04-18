from flask import jsonify
from database import db
from models.__init__ import Rider, Shipping, Location, Order, OrderDetail, Track 
from datetime import datetime
from services.sendMail import send_mail_shipping
 
def saveShippingData(data):
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
    envio = send_mail_shipping(order)
     # Responder con un mensaje de éxito
    return jsonify({'message': 'Envío creado exitosamente', 'id_envio': shipping.id_envio, 'email': envio}), 201