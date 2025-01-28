from database import db
from models.client import Client
from models.product import Product
from flask import jsonify

def saveDataDb(filteredData):
    #tengo que guardar los datos en la base de datos si es que no existen, si ya existen solo debo tomar sus id y ponerlo en el detalle de pedido o pedido
    #si no existe guardar cliente, sino tomar el id
    todos_clientes = Client.query.all()
    todos_productos = Product.query.all()
    id_cliente = None
    for data in filteredData:
        if todos_clientes:
            for clienteDb in todos_clientes:
                if data['Email'] == clienteDb['email']:
                    #guardar id_cliente
                    id_cliente = clienteDb['email']
                    break
                else:
                    #guardar en la base de datos
                    nuevoCliente = Client(
                        nombre = data['Nombre'],
                        email = data['Email'],
                        telefono = data['Telefono']
                    )

                    db.session.add(nuevoCliente)
                    db.session.commit()
                     #buscar id de client con los datos que tengo
       
