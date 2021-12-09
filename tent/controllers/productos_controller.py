import re
from flask import redirect, url_for, request, jsonify
from sqlalchemy.sql.expression import text
from tent.models.producto import Producto, ProductSchema
# from tent.models.producto_compra import ProductoCompra
from tent import db
from sqlalchemy.dialects.mysql import insert
from sqlalchemy import func
import json

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)


# Retornamos todos los productos de la base de datos
def index():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    _filter = request.args.get('filter', '', type=str)
    sort_by = request.args.get('sortby', '', type=str)
    order = request.args.get('order', '', type=str)

    if sort_by:
        _order_by = f"{sort_by} {order}"
    else:
        _order_by = ""

    filtered_query = Producto.query.filter(func.lower(Producto.nombre).contains(
        _filter.lower())).order_by(text(_order_by))

    # necesaria para la paginacion
    rowsNumber = filtered_query.count()
    all_productos = filtered_query.paginate(page=page, per_page=per_page)
    result = products_schema.dump(all_productos.items)
    return jsonify(items=result,
                   rowsNumber=rowsNumber)


def productos_compra_json(lista_productos: list[dict]) -> list[Producto]:
    prods = []
    for prod in lista_productos:
        prods.append(Producto.from_dict(prod))
    return prods
    # result = products_schema.dump(prods)
    # return result


# ProductoRetornamos solo un producto de la base de datos
def show(idProducto):
    producto = Producto.query.get(idProducto)
    if producto is not None:
        return product_schema.dump(producto)
    return f"no se encontro producto con id {idProducto}"


def reservar_producto():
    barcode = request.args.get('barcode', None, type=str)
    cantidad = request.args.get('cantidad', 1, type=int)
    if barcode is not None:
        producto = Producto.query.filter(
            Producto.codigoBarra == barcode).first()
        if producto is not None:
            # manejar lo del stock negativo
            producto.stock = 1 if cantidad >= producto.stock else producto.stock - cantidad
            # "reservar" items
            db.session.commit()
            return product_schema.dump(producto)
        # que pasa si no se encuentra un producto con ese barcode?
        return f"no se encontro producto con codigo de barra {barcode}", 404
    else:
        return "Busqueda malarda", 400  # bad request


# manejar lo del stock negativo
# que pasa si no se encuentra un producto con ese barcode?
def actualizar_stock(producto=None, barcode='', cantidad=1):
    if producto is None:
        producto = Producto.query.filter(
            Producto.codigoBarra == barcode).first()
    if producto is not None:
        if producto.stock > cantidad:
            producto.stock = producto.stock - cantidad
        else:
            producto.stock = 0
        return producto
    return None


# def cancelar_compra():
#


def get_many(ids: list):
    prods = Producto.query.filter(Producto.idProducto
                                  .in_(ids)).all()
    return products_schema.dump(prods)


def add_or_update(prod_list, add_news=True):
    barcodes = [prod.codigoBarra for prod in prod_list]
    existing_prods = Producto.query.filter(Producto.codigoBarra
                                           .in_(barcodes)).all()
    i = 0
    n_existing = len(existing_prods)
    for prod in prod_list:
        # manejar cambios en el precio
        if i < n_existing and prod.codigoBarra == existing_prods[i].codigoBarra:
            existing_prods[i].stock += prod.stock
            i += 1
        else:
            if add_news:
                existing_prods.append(prod)
    return existing_prods


def destroy(idProducto):
    producto = Producto.query.get(idProducto)
    db.session.delete(producto)
    db.session.commit()
    return product_schema.jsonify(producto)


def store():
    body = request.data.decode()
    body_json = json.loads(body)
    new_product = Producto.from_dict(body_json)
    [prod] = add_or_update([new_product])
    # ver lo de INSERT ... ON DUPLICATE KEY UPDATE Statement
    db.session.add(prod)
    db.session.commit()
    return "OK MI REY"
    # return product_schema.dumps(new_product)


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
