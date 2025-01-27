from database import db
from models.client import Client

def saveDataDb(filteredData):
    #tengo que guardar los datos en la base de datos si es que no existen, si ya existen solo debo tomar sus id y ponerlo en el detalle de pedido o pedido
    #si no existe guardar cliente, sino tomar el id
    todos_clientes = Client.query.all()
    for cliente in todos_clientes:
        filteredData['email'] == cliente['email']
        print(f"{filteredData['email']} es igual a:   {cliente['email']}")
        return filteredData['email'] == cliente['email']