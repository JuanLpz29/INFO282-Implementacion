import re
from flask import redirect, url_for, request, jsonify
from sqlalchemy.sql.expression import text
from tent.models.producto import Producto, ProductSchema
# from tent.models.producto_compra import ProductoCompra
from tent import db
from sqlalchemy.dialects.mysql import insert
from sqlalchemy import func
import json
from flask_restful import Resource, reqparse, abort
from tent.utils.parsers import pagination_arg_parser, prod_args_parser
# from tent.controllers import pagination_arg_parser
# from tent.controllers import prod_args_parser

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)


def query_producto_by(_key: str, _value: str) -> Producto:
    query_funcs = {

        'idProducto': Producto.query.get,
        'codigoBarra': lambda x: Producto.query.filter(
            Producto.codigoBarra == x).first(),
    }
    f = query_funcs.get(_key)
    if f is not None:
        return f(_value)


def query_many_productos_by(key: str, value: list) -> list[Producto]:
    query_funcs = {

        'all': lambda x: Producto.query.all(),

        'idProducto': lambda x: Producto.query.filter(Producto.idProducto
                                                      .in_(value)).all(),
        'codigoBarra': lambda x: Producto.query.filter(Producto.codigoBarra
                                                       .in_(value)).all(),
        'nombre': lambda x: Producto.query.filter((Producto.nombre).contains(x))
    }
    f = query_funcs.get(key)
    if f is not None:
        return f(value)


def abort_if_no_producto_found(key: str, value: any) -> Producto:
    producto = query_producto_by(key, value)
    if producto is None:
        abort(404, message=f"No se encontro producto con {key} {value}")
    return producto


def productos_from_json_list(lista_productos: list[dict]) -> list[Producto]:
    prods = []
    for prod in lista_productos:
        prods.append(Producto.from_dict(prod))
    return prods
    # result = products_schema.dump(prods)
    # return result


# manejar lo del stock negativo
# que pasa si no se encuentra un producto con ese barcode?
def actualizar_stock(producto=None, barcode='', cantidad=1) -> Producto:
    if producto is None:
        producto = Producto.query.filter(
            Producto.codigoBarra == barcode).first()
    if producto is not None:
        if producto.stock > cantidad:
            producto.stock = producto.stock - cantidad
        else:
            producto.stock = 1
        return producto
    return None

# asumir que le codigo de barra sera unique key?
# creo que todo funciona bajo el supuesto de que no
# hay mas de un producto registrado con el mismo codigo de barras


def add_or_update(prod_list: list[Producto], add_news=True) -> list[Producto]:
    barcodes = [prod.codigoBarra for prod in prod_list]
    existing_prods = query_many_productos_by('codigoBarra', barcodes)
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


class ProductoManager(Resource):
    def get(self, idProducto):
        prod = abort_if_no_producto_found('idProducto', idProducto)
        return product_schema.dump(prod)

    def put(self, idProducto):
        prod = abort_if_no_producto_found('idProducto', idProducto)
        args = prod_args_parser.parse_args()
        for key, value in args:
            setattr(prod, key, value)
        db.session.add(prod)
        db.session.commit()
        return product_schema.jsonify(prod)


class ProductoListManager(Resource):
    def get(self):
        args = pagination_arg_parser.parse_args()

        _order_by = f"{args['sortby']} {args['order']}" if args['sortby'] else ""
        filtered_query = query_many_productos_by(
            'nombre', args['filter']).order_by(text(_order_by))
        rowsNumber = filtered_query.count()
        all_prods = filtered_query.paginate(
            page=args['page'], per_page=args['perpage'])
        result = products_schema.dump(all_prods.items)
        return jsonify(items=result,
                       rowsNumber=rowsNumber)

    def post(self):
        args = prod_args_parser.parse_args()
        prod = query_producto_by('codigoBarra', args['codigoBarra'])
        if prod is None:
            prod = Producto.from_dict(args)
            db.session.add(prod)
            db.session.commit()
            added = True
        else:
            # si ya existe se debe actualizar con un put(idProducto)
            added = False
        return jsonify(producto=product_schema.dump(prod),
                       added=added)
