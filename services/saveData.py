from database import db
from models.__init__ import Client, Product, Location, Order, OrderDetail
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
                nro_pedido = orders['Nro pedido'],
                fecha = orders['Fecha'],
                Cliente_id_cliente = cliente.id_cliente,
                Ubicacion_id_ubicacion = ubicacion.id_ubicacion
            )
            db.session.add(order)
            db.session.commit()

            orderDetail = OrderDetail(
                cantidad = orders['Cantidad'],
                Producto_id_producto = producto.id_producto,
                Pedido_id_pedido = order.id_pedido
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
                Producto_id_producto = producto.id_producto,
                Pedido_id_pedido = order.id_pedido
            )
            db.session.add(orderDetail)
            db.session.commit()
    return "Datos guardados correctamente"


       


def verificar_existencia(pedido):
    ubicacion = None
    print(f"ciudad:{pedido.get('Ciudad')} , direccion:{pedido.get('Direccion1')}")
    if pedido.get('Ciudad') and pedido.get('Direccion1') and pedido.get('Codigo postal'):
        ubicacion = Location.query.filter_by(localidad=pedido['Ciudad'],direccion=pedido['Direccion1'],codigo_postal=pedido['Codigo postal']).first()
    cliente = Client.query.filter_by(email=pedido['Email']).first()
    producto = Product.query.filter_by(nombre_producto=pedido['Producto']).first()
    order = Order.query.filter_by(nro_pedido=pedido['Nro pedido']).first()
    return cliente,producto,ubicacion,order
