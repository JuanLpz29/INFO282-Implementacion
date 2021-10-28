from flask import render_template, redirect, url_for, request, abort, jsonify
from app.models.producto import Producto, ProductSchema
from app import db

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)
# Retornamos todos los productos de la base de datos


def index():
    all_productos = Producto.query.all()
    result = products_schema.dump(all_productos)
    return jsonify(result)


# Retornamos solo un producto de la base de datos
def show(idProducto):
    producto = Producto.query.get(idProducto)
    return product_schema.jsonify(producto)


def destroy(idProducto):
    producto = Producto.query.get(idProducto)
    db.session.delete(producto)
    db.session.commit()
    return product_schema.jsonify(producto)


def store():
    nombre = request.json['nombre']
    stock = request.json['stock']
    precioUnitario = request.json['precioUnitario']
    valorItem = request.json['valorItem']

    new_product = Producto(nombre, stock, precioUnitario, valorItem)

    db.session.add(new_product)
    db.session.commit()

    return product_schema.jsonify(new_product)


# Actualizamos la info de un producto SOLO FUNCIONA CON debug=False, no sé por qué xd
def update(idProducto):

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
