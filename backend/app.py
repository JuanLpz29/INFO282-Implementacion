# Flask para usar flask, jsonify para transformar a json objetos, request para los POST, PUT, GET
from flask import Flask, jsonify, request, render_template, make_response, Response
from flask.json import loads
from flask_sqlalchemy import SQLAlchemy  # Hace la conexión con la bd
# No cacho bien que hace pero es para poder mandar los cambios a la bd
from flask_marshmallow import Marshmallow
import os
from flask import flash, redirect, url_for
from werkzeug.utils import secure_filename
import json
from xml_to_pdf_functions import sii_doc_XMLtoPDF, datos_xml_to_df
from my_funcs import TPDV, preprocess_xml, get_final_df
from pathlib import Path
from os.path import join

UPLOAD_FOLDER = './uploads/'
# ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


app = Flask(__name__)
app.secret_key = "super secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Configuración inicial de la bd disponible en la doc de sqlalchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:rvega2015@35.223.76.162/taller'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)


class Producto(db.Model):
    __tablename__ = 'Producto'  # No sé si es necesario, pero creo que si
    idProducto = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), )
    descripcion = db.Column(db.String(50))
    stock = db.Column(db.Integer)
    categoria = db.Column(db.String(50))
    formato = db.Column(db.String(50))
    codigoBarra = db.Column(db.Integer)
    # foto
    cantidadRiesgo = db.Column(db.Integer)
    precioCompra = db.Column(db.Integer)
    precioVenta = db.Column(db.Integer)
    precioUnitario = db.Column(db.Integer)
    valorItem = db.Column(db.Integer)

    # Campos minimos para hacer POST
    def __init__(self, nombre, descripcion, stock, precioUnitario, valorItem):
        self.nombre = nombre
        self.descripcion = descripcion
        self.stock = stock
        self.precioUnitario = precioUnitario
        self.valorItem = valorItem

    @classmethod
    def from_df(cls, df_row):
        try:
            price = int(df_row['Valor Item'].replace('.', ''))
        except AttributeError:
            price = 0
        return cls(df_row['nombre'],
                   df_row['descripcion'],
                   int(df_row['qty']),
                   price,
                   price)

    def print_info(self):
        print(f"{self.nombre:<43} {self.cantidad:<15} {self.precioUnitario:}")


class ProductSchema(ma.Schema):
    class Meta:
        fields = ('idProducto', 'nombre', 'descripcion', 'stock', 'categoria', 'formato', 'codigoBarra',
                  'foto', 'cantidadRiesgo', 'precioCompra', 'precioVenta', 'precioUnitario', 'valorItem')


# Se inicializan
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)


class Compra:
    def __init__(self, xml_file):
        self.get_info_compra(xml_file)
        self.toJSON()
        self.get_info_productos(xml_file)

    def get_info_compra(self, xml_file):
        df_datos = datos_xml_to_df(xml_file)
        dict_datos = df_datos.iloc[0].to_dict()
        # forma corta, no se ve que se esta agregando
        for key, value in dict_datos.items():
            setattr(self, key, value)
        """
        self.id = dict_datos['folio']
        self.tipo_documento = dict_datos['tipoDoc']
        self.monto_neto = int(dict_datos['montoNeto'])
        self.monto_iva = int(dict_datos['montoIVA'])
        self.monto_total = int(dict_datos['montoTotal'])
        self.proveedor = dict_datos['proveedor']
        self.fecha = dict_datos['fecha']
        """

    def get_info_productos(self, xml_file):
        df_productos = sii_doc_XMLtoPDF(xml_file)
        df_productos = get_final_df(df_productos)
        print(df_productos)
        self.productos = []
        for i in range(len(df_productos)):
            self.productos.append(Producto.from_df(df_productos.iloc[i]))
            # self.products[i].print_info()

    def print_info_compra(self):
        for key, value in self.__dict__.items():
            if key != 'productos':
                print(f"{key:>20} : {value}")
        self.print_productos()

    def print_productos(self):
        print("\n", "*"*30, "DETALLE", "*"*30, '\n')
        print(f"{'nobmre':<40} cantidad   presio compra")
        for prod in self.productos:
            prod.print_info()
        print("\n", "*"*69, '\n')

    def toJSON(self):
        self.json_compra = json.dumps(self, default=lambda o: o.__dict__,
                                      sort_keys=True, indent=4)


# Retornamos todos los productos de la base de datos
@app.route('/productos', methods=['GET'])
def get_all_productos():
    all_productos = Producto.query.all()
    result = products_schema.dump(all_productos)
    return jsonify(result)


# Retornamos solo un producto de la base de datos
@app.route("/productos/<idProducto>/", methods=['GET'])
def get_producto(idProducto):
    producto = Producto.query.get(idProducto)
    return product_schema.jsonify(producto)


# Posteamos en la bd un nuevo producto
# Lo hice simulando la info inicial de la factura
@app.route("/post-factura", methods=['POST'])
def post_info_factura():
    nombre = request.json['nombre']
    stock = request.json['stock']
    precioUnitario = request.json['precioUnitario']
    valorItem = request.json['valorItem']

    new_product = Producto(nombre, stock, precioUnitario, valorItem)

    db.session.add(new_product)
    db.session.commit()

    return product_schema.jsonify(new_product)


# Actualizamos la info de un producto SOLO FUNCIONA CON debug=False, no sé por qué xd

@app.route("/productos/<idProducto>/", methods=['PUT'])
def put_info_adicional_factura(idProducto):

    producto = Producto.query.get(idProducto)

    descripcion = request.json['descripcion']
    categoria = request.json['categoria']
    formato = request.json['formato']
    codigoBarra = request.json['codigoBarra']
    cantidadRiesgo = request.json['cantidadRiesgo']
    precioVenta = request.json['precioVenta']

    producto.descripcion = descripcion
    producto.categoria = categoria
    producto.formato = formato
    producto.codigoBarra = codigoBarra
    producto.cantidadRiesgo = cantidadRiesgo
    producto.precioVenta = precioVenta

    db.session.commit()

    return product_schema.jsonify(producto)

# DELETE, quizás no deberiamos borrar (Eso dijo Mirko asi que no sé que pasa)


@app.route("/productos/<idProducto>/", methods=['DELETE'])
def delete_producto(idProducto):
    producto = Producto.query.get(idProducto)
    db.session.delete(producto)
    db.session.commit()
    return product_schema.jsonify(producto)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ['xml']


@app.route('/documento', methods=['GET', 'POST'])
def upload_file():
    print(request)
    print('*'*60)
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            print("NINGUN ARCHIVO SELECCIONADO")
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            xml_compras = Path(UPLOAD_FOLDER + file.filename).read_text()
            # si es un archivo ya preprocesado se cae con esto
            # xml_compras = preprocess_xml(xml_str, n_compras=1)
            cmp = Compra(xml_compras)
            resp1 = jsonify(info=cmp.json_compra,
                            productos=products_schema.dumps(cmp.productos))
        return resp1
    return


if __name__ == "__main__":
    app.run(debug=True)
