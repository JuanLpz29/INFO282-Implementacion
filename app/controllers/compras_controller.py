from flask import render_template, redirect, url_for, request, abort, jsonify
from app.models.compra import Compra, CompraSchema
from app.models.producto import ProductSchema
from app.controllers.DTE import DTE
from app import db
from werkzeug.utils import secure_filename
from os.path import join
from pathlib import Path
from flask import current_app
# from DTE import DTE


compra_schema = CompraSchema()
compras_schema = CompraSchema(many=True)

# NO SE SI HAY UNA FORMA MEJOR PARA MANEJAR LOS PRODUCTOS
# DENTOR DE LA COMPRA... OTRA TABLA POR LA RELACION ESA?


def _allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ['xml']


def upload_documento():
    if request.method == 'POST':
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
            # cmp = Compra(xml_compras)
            print(cmp.get_df_productos())
            resp1 = jsonify(info=cmp.get_df_datos().to_json(orient="index"),
                            productos=cmp.get_df_productos().to_json(orient="table"))
        return resp1
    return
