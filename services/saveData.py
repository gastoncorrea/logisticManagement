from database import db
from models.client import Client
from models.product import Product
from models.location import Location
from models.order import Order
from models.orderDetail import OrderDetail
from flask import jsonify

def saveDataDb(filteredData):
    #tengo que guardar los datos en la base de datos si es que no existen, si ya existen solo debo tomar sus id y ponerlo en el detalle de pedido o pedido
    #si no existe guardar cliente, sino tomar el id
    for orders in filteredData:
        cliente,producto,ubicacion,order = verificar_existencia(orders)
        if not order:
            if not cliente:
                cliente = Client(
                    nombre=orders['Nombre'],
                    email=orders['Email'],
                    telefono=orders['Telefono']
                )
                db.session.add(cliente)
                db.session.commit()
            if not producto:
                producto = Product(
                    nombre_producto = orders['Producto']
                )
                db.session.add(producto)
                db.session.commit()
            if not ubicacion:
                ubicacion = Location(
                    localidad = orders['Ciudad'],
                    direccion = orders['Direccion1'],
                    direccion2 = orders['Direccion2'],
                    codigo_postal = orders['Codigo postal']
                )
                db.session.add(ubicacion)
                db.session.commit()
            order = Order(
                nro_pedido = orders['nro_pedido'],
                fecha = orders['Fecha'],
                id_cliente = cliente.id_cliente,
                id_ubicacion = ubicacion.id_ubicacion
            )
            db.session.add(order)
            db.session.commit()

            orderDetail = OrderDetail(
                cantidad = orders['Cantidad'],
                id_producto = producto.id_producto,
                id_pedido = order.id_pedido
            )
            db.session.add(orderDetail)
            db.session.commit()
        else:
            if not producto:
                producto = Product(
                    nombre_producto = orders['Producto']
                )
                db.session.add(producto)
                db.session.commit()

            orderDetail = OrderDetail(
                cantidad = orders['Cantidad'],
                id_producto = producto.id_producto,
                id_pedido = order.id_pedido
            )
            db.session.add(orderDetail)
            db.session.commit()
    return "Datos guardados correctamente"


       


def verificar_existencia(pedido):
    cliente = Client.query.filter_by(email=pedido['Email']).first()
    producto = Product.query.filter_by(nombre_producto=pedido['Producto'])
    ubicacion = Location.query.filter_by(localidad=pedido['Ciudad'],direccion=pedido['Direccion1'],codigo_postal=pedido['Codigo postal'])
    order = Order.query.filter_by(nro_pedido=pedido['nro_pedido'])
    return cliente,producto,ubicacion,order
