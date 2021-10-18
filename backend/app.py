from flask import Flask, jsonify, request #Flask para usar flask, jsonify para transformar a json objetos, request para los POST, PUT, GET
from flask_sqlalchemy import SQLAlchemy # Hace la conexión con la bd
from flask_marshmallow import Marshmallow #No cacho bien que hace pero es para poder mandar los cambios a la bd

app = Flask(__name__)

#Configuración inicial de la bd disponible en la doc de sqlalchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:rvega2015@35.223.76.162/taller'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

#Clase que hace la relacion entre la TABLA PRODUCTO de la db con Flask, no tienen que estar definidos todos los campos
class Producto(db.Model):
    __tablename__ = 'Producto' # No sé si es necesario, pero creo que si
    idProducto = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), )
    descripcion = db.Column(db.String(50))
    stock = db.Column(db.Integer)
    categoria = db.Column(db.String(50))
    formato = db.Column(db.String(50))
    codigoBarra = db.Column(db.Integer)
    #foto
    cantidadRiesgo = db.Column(db.Integer)
    precioCompra = db.Column(db.Integer)
    precioVenta = db.Column(db.Integer)
    precioUnitario = db.Column(db.Integer)
    valorItem = db.Column(db.Integer)

    #Campos minimos para hacer POST
    def __init__(self, nombre, stock, precioUnitario, valorItem):
        self.nombre = nombre
        self.stock = stock
        self.precioUnitario = precioUnitario
        self.valorItem = valorItem

#Define el esquema de la base de datos
class ProductSchema(ma.Schema):
    class Meta:
        fields = ('idProducto', 'nombre', 'descripcion', 'stock', 'categoria', 'formato', 'codigoBarra', 'foto', 'cantidadRiesgo','precioCompra', 'precioVenta' ,'precioUnitario', 'valorItem')



#Se inicializan
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)


# Retornamos todos los productos de la base de datos
@app.route('/productos', methods=['GET'])
def get_all_productos():
  all_productos = Producto.query.all()
  result = products_schema.dump(all_productos)
  return jsonify(result)


#Retornamos solo un producto de la base de datos
@app.route("/productos/<idProducto>/", methods = ['GET'])
def get_producto(idProducto):
    producto = Producto.query.get(idProducto)
    return product_schema.jsonify(producto)


#Posteamos en la bd un nuevo producto
#Lo hice simulando la info inicial de la factura
@app.route("/post-factura", methods = ['POST'])
def post_info_factura():
    nombre = request.json['nombre']
    stock = request.json['stock']
    precioUnitario = request.json['precioUnitario']
    valorItem = request.json['valorItem']

    new_product= Producto(nombre, stock, precioUnitario, valorItem)

    db.session.add(new_product)
    db.session.commit()
    
    return product_schema.jsonify(new_product)

# Actualizamos la info de un producto SOLO FUNCIONA CON debug=False, no sé por qué xd
@app.route("/productos/<idProducto>/", methods = ['PUT'])
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

    ##

    db.session.commit()

    return product_schema.jsonify(producto)

# DELETE, quizás no deberiamos borrar (Eso dijo Mirko asi que no sé que pasa)
@app.route("/productos/<idProducto>/", methods = ['DELETE'])
def delete_producto(idProducto):
    producto = Producto.query.get(idProducto)
    db.session.delete(producto)
    db.session.commit()
    return product_schema.jsonify(producto)



## DOCUMENTO


@app.route("/documento", methods = ['POST'])
def post_documento():
    req = request.get_json()
    print(req)
    return


if __name__ == "__main__": 
    app.run(debug=False)
