from flask import jsonify
import pandas as pd
import csv
import io


def filterData(request):
    if 'file' not in request.files:
        return jsonify({"error":"No file part"}),400
    file = request.files['file']
    if file.filename == "":
        return jsonify({"error":"No selected file"})

        #Leo archivo csv
    '''file_contents = file.read().decode('utf-8')
    csv_reader = csv.DictReader(io.StringIO(file_contents)) 

    # Para probar, devolver los datos leídos
    data = [row for row in csv_reader]
    return jsonify(data)'''

    file_contents = file.read().decode('utf-8')
    datos = pd.read_csv(io.StringIO(file_contents))
    pd.set_option('display.float_format', '{:.0f}'.format)
    datos['Created at'] = pd.to_datetime(datos['Created at'])
    datos['Created at'] = datos['Created at'].dt.strftime('%Y-%m-%d')
    columnas_seleccionadas = ['Name','Billing Name','Email','Created at','Lineitem name','Lineitem quantity','Billing Phone','Billing City','Billing Address1', 'Billing Address2','Billing Zip']
    datos_seleccionados = datos[columnas_seleccionadas]
    datos_seleccionados = datos_seleccionados.rename(columns={'Name':'Nro pedido','Billing Name': 'Nombre','Created at': 'Fecha','Lineitem name': 'Producto','Lineitem quantity': 'Cantidad','Billing Phone': 'Telefono','Billing City': 'Ciudad','Billing Address1': 'Direccion1', 'Billing Address2': 'Direccion2','Billing Zip': 'Codido postal'})

    data = datos_seleccionados.to_dict(orient='records')
    return jsonify(data)