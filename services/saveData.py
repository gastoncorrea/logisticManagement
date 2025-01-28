from database import db
from models.client import Client
from flask import jsonify

def saveDataDb(filteredData):
    #tengo que guardar los datos en la base de datos si es que no existen, si ya existen solo debo tomar sus id y ponerlo en el detalle de pedido o pedido
    #si no existe guardar cliente, sino tomar el id
    todos_clientes = Client.query.all()
    if todos_clientes:

        for data in filteredData:
            for clienteDb in todos_clientes:
                if data['Email'] == clienteDb['email']:
                 id_cliente = clienteDb['id_cliente']
                 return id_cliente 
    else:        
        return f"no hay clientes cargados aun"
