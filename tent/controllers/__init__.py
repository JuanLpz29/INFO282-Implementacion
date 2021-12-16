from flask import Blueprint, current_app
from flask_restful import reqparse

from tent.controllers.productos_controller import index as products_index
from tent.controllers.productos_controller import show as products_show
from tent.controllers.productos_controller import store as products_store
from tent.controllers.productos_controller import reservar_producto as products_reserva

from tent.controllers.compras_controller import upload_documento as compras_store
from tent.controllers.compras_controller import upload_json as compras_store_json
from tent.controllers.compras_controller import index as compras_index
from tent.controllers.compras_controller import show as compras_show
from tent.controllers.compras_controller import details as compras_details

from tent.controllers.base_controller import hello

productos_bp = Blueprint('productos', 'api', url_prefix='/productos')
compras_bp = Blueprint('compras', 'api', url_prefix='/compras')
base_bp = Blueprint('', 'api', url_prefix='')

productos_url_rules = [('/', products_index, ['GET']),
                       ('/reservar/', products_reserva, ['GET']),
                       ('/<int:idProducto>/', products_show, ['GET']),
                       ('/nuevo/', products_store, ['POST'])
                       ]

compras_url_rules = [('/', compras_index, ['GET']),
                     ('/documento', compras_store, ['POST']),
                     ('/upload', compras_store_json, ['POST']),
                     ('/<int:idCompra>/', compras_show, ['GET']),
                     ('/details/<int:idCompra>/', compras_details, ['GET']),
                     ]


base_url_rules = [('/', hello, ['GET'])]

for (rule, func, methods) in productos_url_rules:
    productos_bp.add_url_rule(rule, view_func=func, methods=methods)

for (rule, func, methods) in compras_url_rules:
    compras_bp.add_url_rule(rule, view_func=func, methods=methods)

for (rule, func, methods) in base_url_rules:
    base_bp.add_url_rule(rule, view_func=func, methods=methods)


pagination_arg_parser = reqparse.RequestParser()
pagination_arg_parser.add_argument('page', default=1, type=int,
                                   help='Page cannot be converted')
pagination_arg_parser.add_argument("perpage", default=10, type=int,
                                   help='perpage cannot be converted')
pagination_arg_parser.add_argument("filter", default="", type=str,)
pagination_arg_parser.add_argument("sortby", default="", type=str,)
pagination_arg_parser.add_argument("order", default="", type=str,
                                   choices=["asc", "desc", ""],)
