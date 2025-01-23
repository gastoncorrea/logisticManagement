from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from datetime import datetime
import csv
import io

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/pedidos'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True


db = SQLAlchemy(app)

class Pedido(db.Model):
    __tablename__ = 'pedidos'

    id = db.Column(db.Integer, primary_key=True)
    nro_pedido = db.Column(db.String(10), nullable = False)
    nombre_cliente = db.Column(db.String(50))
    email = db.Column(db.String(50),nullable = False)
    fecha = db.Column(db.Date, nullable = False)
    producto = db.Column(db.String(100),nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    telefono = db.Column(db.Integer)
    ciudad = db.Column(db.String(50))
    direccion = db.Column(db.String(50))
    direccion2 = db.Column(db.String(50))
    cp = db.Column(db.String(20))

'''@app.route('/')
def index():
    try:
        # prueba de guardar un registro en base de datos
        nuevo_pedido = Pedido(

            nro_pedido = "#2479",
            nombre_cliente = "Edmundo Correa",
            email = "edmundo@gmail.com",
            fecha = datetime.strptime("2025-01-12","%Y-%m-%d").date(),
            producto = "parabrisas",
            cantidad = 1,
            telefono = 344521,
            ciudad = "CABA",
            direccion = "San Martin 54",
            direccion2 = "",
            cp = 4000
        )
        db.session.add(nuevo_pedido)
        db.session.commit()
        print("Pedido guardado con exito: Id ",nuevo_pedido.id)
        return "Registro guardado"
    except Exception as e:
        db.session.rollback()
        return f"Error en la conexión: {e}"
'''

@app.route("/upload", methods=["POST"])
def uplodad_file():
    if 'file' not in request.files:
        return jsonify({"error":"No file part"}),400
    file = request.files['file']
    if file.filename == "":
        return jsonify({"error":"No selected file"})

    try:
        #Leo archivo csv
        file_contents = file.read().decode('utf-8')
        csv_reader = csv.DictReader(io.StringIO(file_contents)) 
        #proceso cada fila y la guardo
        for row in csv_reader:
            fecha = datetime.strptime(row['Fecha'], "%d/%m/%Y").strftime("%Y-%m-%d")

             # Verificar si el campo 'Numero' está vacío antes de convertirlo a entero
            if row['Telefono']:
                telefono = int(row['Telefono'])
            else:
                telefono = None  # O cualquier valor por defecto que desees


            nuevo_pedido = Pedido(
                nro_pedido = row['nro_pedido'],
                nombre_cliente = row['Nombre'],
                email = row['Email'],
                fecha = fecha,
                producto = row['Producto'],
                cantidad = int(row['Cantidad']),
                telefono = telefono,
                ciudad = row['Ciudad'],
                direccion = row['Direccion1'],
                direccion2 = row['Direccion2'],
                cp = row['Codido postal']
            )
            db.session.add(nuevo_pedido)

        #Guardo datos en base de datos
        db.session.commit()

        return jsonify({"message":"Pedidos cargados con exito"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error":str(e)}), 500

@app.route('/')
def recuper_pedidos():
    mis_datos = Pedido.query.all()
    resultados = []
    for registro in mis_datos:
        resultados.append({
            'id' : registro.id,
            'nro_pedido' : registro.nro_pedido,
            'nombre_cliente' : registro.nombre_cliente,
            'email' : registro.email,
            'fecha' : registro.fecha,
            'producto' : registro.producto,
            'cantidad' : registro.cantidad,
            'telefono' : registro.telefono,
            'ciudad' : registro.ciudad,
            'direccion' : registro.direccion,
            'direccion2' : registro.direccion2,
            'cp' : registro.cp
            }
        )
    return jsonify(resultados)


with app.app_context():
    db.create_all()