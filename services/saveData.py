from database import db
from models.__init__ import Client, Product, Location, Order, OrderDetail, Track
from datetime import datetime

def saveDataDb(filteredData):
    #tengo que guardar los datos en la base de datos si es que no existen, si ya existen solo debo tomar sus id y ponerlo en el detalle de pedido o pedido
    #si no existe guardar cliente, sino tomar el id
    registros_guardados = 0
    registros_duplicados = 0
    ver_duplicados = []
    contador = 0
    for orders in filteredData:
        cliente = None
        producto = None
        ubicacion = None
        order = None
        contador += 1
        cliente,producto,ubicacion,order = verificar_existencia(orders)
        print(f"*****REGISTRO NRO******: {contador}")
        if not order:
            if not cliente:
                cliente = Client(
                    nombre=orders['Nombre'],
                    #email=orders['Email'],
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
                    provincia = orders['Ciudad'],
                    direccion = orders['Direccion1'],
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
            
            track = Track(
                fecha = datetime.now(),
                estado = "En proceso",
                Pedido_id_pedido = order.id_pedido
            )
            db.session.add(track)
            db.session.commit()
            
            registros_guardados+=1
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
                registros_guardados+=1
            else:
                #Agregar logica para ver si el id_producto esta relacionado con un pedido existente
                orderDetail = OrderDetail.query.filter_by(Pedido_id_pedido=order.id_pedido,Producto_id_producto = producto.id_producto).first()
                if not orderDetail:
                    orderDetail = OrderDetail(
                    cantidad = orders['Cantidad'],
                    Producto_id_producto = producto.id_producto,
                    Pedido_id_pedido = order.id_pedido
                    )
                    db.session.add(orderDetail)
                    db.session.commit()
                    registros_guardados+=1
                else:
                    ver_duplicados.append(orders)
                    registros_duplicados+=1
                    print(f"prducto repetido: {producto} se compara con este del excel: {orders['Producto']}")
                
    return f"Datos guardados correctamente: {registros_guardados}--- Registros duplicados: {registros_duplicados} ---Ver{ver_duplicados}"


       


def verificar_existencia(pedido):

    print(f"este es el valor del registro: ***{pedido}***")
    ubicacion = Location.query.filter_by(provincia=pedido['Ciudad'],direccion=pedido['Direccion1'],codigo_postal=pedido['Codigo postal']).first()
    print(f"estos son los datos *encontrados* en ubicacion: {ubicacion} y estos *vienen* en el excel: {pedido['Ciudad']}")
    cliente = Client.query.filter_by(nombre=pedido['Nombre']).first()
    print(f"*Cliente encontrado*: {cliente} y estos vienen en el excel en cliente: {pedido['Nombre']}")
    producto = Product.query.filter_by(nombre_producto=pedido['Producto']).first()
    print(f"*Producto encontrado en la base de Datos*: {producto} y estos el producto que llega en el excel: {pedido['Producto']}")
    order = Order.query.filter_by(nro_pedido=pedido['Nro pedido']).first()
    print(f"pedido encontrado en la base de datos: {order} y pedido que llega en el excel: {pedido['Nro pedido']}")
    return cliente,producto,ubicacion,order
