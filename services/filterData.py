from flask import jsonify
import pandas as pd
import numpy as np
import io


def filterData(request):
    if 'file' not in request.files:
        return jsonify({"error":"No file part"}),400
    file = request.files['file']
    if file.filename == "":
        return jsonify({"error":"No selected file"})

        #Leo archivo csv

    file_contents = file.read().decode('utf-8')
    datos = pd.read_csv(io.StringIO(file_contents))
    datos['FECHA'] = pd.to_datetime(datos['FECHA'], format='%d/%m/%Y', errors='coerce')
    datos = datos.dropna(subset=['FECHA'])
    datos['CANTIDAD'].replace([np.nan, np.inf, -np.inf], 0, inplace=True)
    datos['CANTIDAD'] = datos['CANTIDAD'].astype(int)
    columnas_seleccionadas = ['FECHA','NRO DE PEDIDO','NOMBRE','CANTIDAD','Producto','PROVINCIA','DIRECCION', 'CP','NUMERO']
    datos_seleccionados = datos[columnas_seleccionadas]
    datos_seleccionados = datos_seleccionados.rename(columns={
        'NRO DE PEDIDO': 'Nro pedido',
        'NOMBRE': 'Nombre',
        'FECHA': 'Fecha',
        'Producto': 'Producto',
        'CANTIDAD': 'Cantidad',
        'NUMERO': 'Telefono',
        'PROVINCIA': 'Ciudad',
        'DIRECCION': 'Direccion1',
        'CP': 'Codigo postal'
    })
    
    datos_seleccionados = datos_seleccionados.fillna("")
    data = datos_seleccionados.to_dict(orient='records')
    print("los datos son:", data[0])
    return data