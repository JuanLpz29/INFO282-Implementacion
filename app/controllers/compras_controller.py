from flask import render_template, redirect, url_for, request, abort, jsonify, wrappers
from app.models.compra import Compra, CompraSchema
from app.models.producto import ProductSchema
from app.models.proveedor import Proveedor
from app.utils.DTE import DTE
from app import db
from werkzeug.utils import secure_filename
from os.path import join
from pathlib import Path
from flask import current_app
from pandas import DataFrame

from app.models.proveedor import Proveedor
# from DTE import DTE


compra_schema = CompraSchema()
compras_schema = CompraSchema(many=True)

# NO SE SI HAY UNA FORMA MEJOR PARA MANEJAR LOS PRODUCTOS
# DENTOR DE LA COMPRA... OTRA TABLA POR LA RELACION ESA?fal


def index():
    all_compras = Compra.query.paginate(page=1, per_page=30)
    result = compras_schema.dump(all_compras.items)
    return jsonify(result)


# Retornamos solo un producto de la base de datos
def show(idCompra):
    compra = Compra.query.get(idCompra)
    if compra is not None:
        return compra_schema.jsonify(compra)
    return f"no se encontro Compra con id {idCompra}"


def _allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ['xml']


def _store(datos_compra: dict, df_productos: DataFrame, datos_proveedor: dict):
    cmp = Compra.query.filter_by(folio=datos_compra['folio']).first()
    if cmp is not None:
        print('la compra ya se encuentra registrada en el sistema!!')
        return
    # como no existe creamos una nueva
    new_compra = Compra(datos_compra, df_productos)
    # si no existe un proveedor con ese rut, lo creamos
    pro = Proveedor.query.filter_by(rut=datos_proveedor['rut']).first()
    if pro is None:
        pro = Proveedor.from_dict(datos_proveedor)
        print(f'Se agregara el proveedor  "{pro.razonSocial}" al sistema')
    # una comprita pal master
    pro.compras.append(new_compra)
    db.session.add(pro)
    # al parecer no es necesaroi este ADD, con el append anterior basta
    # para que se cree la compra actual
    # db.session.add(new_compra)
    db.session.commit()


def upload_documento():
    # check if the post request has the file part
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        print("NINGUN ARCHIVO SELECCIONADO")
        return redirect(request.url)
    if file and _allowed_file(file.filename):
        filename = secure_filename(file.filename)
        uf = current_app.config['UPLOAD_FOLDER']
        file.save(join(uf, filename))
        xml_compras = Path(join(uf, file.filename)).read_text()
        cmp = DTE(xml_compras)
        # print(cmp.get_df_datos())
        # print(cmp.get_df_proveedor())
        _store(cmp.datos_dict, cmp.df_productos,
               cmp.proveedor_dict)  # guardar datos factura
        # unir los diccionariosgt
        info_doc = {**cmp.proveedor_dict, **cmp.datos_dict}
        response = jsonify(info=info_doc,
                           productos=cmp.df_productos.to_json(orient="table"))
    return response
