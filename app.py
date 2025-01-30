from flask import Flask, jsonify, request
from database import db
from models.__init__ import Client, Product, Location, Order, OrderDetail
from services.filterData import filterData
from services.saveData import saveDataDb

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/gestion_pedidos'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
db.init_app(app)


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
   return saveDataDb(filterData(request))
  #return filterData(request)

'''@app.route('/')
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
'''


with app.app_context():
    db.create_all()