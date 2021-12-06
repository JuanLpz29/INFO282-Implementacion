import os
from flask import Blueprint, current_app

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

from tent.controllers.ventas_controller import index as ventas_index
from tent.controllers.ventas_controller import show as ventas_show
from tent.controllers.ventas_controller import start as ventas_start
from tent.controllers.ventas_controller import details as ventas_details
from tent.controllers.ventas_controller import update as ventas_update
from tent.controllers.ventas_controller import cancel as ventas_cancel
from tent.controllers.ventas_controller import confirm as ventas_confirm


productos_bp = Blueprint('productos', 'api', url_prefix='/productos')
compras_bp = Blueprint('compras', 'api', url_prefix='/compras')
ventas_bp = Blueprint('ventas', 'api', url_prefix='/ventas')
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


ventas_url_rules = [('/', ventas_index, ['GET']),
                    ('/<int:idVenta>/', ventas_show, ['GET']),
                    ('/details/<int:idVenta>/', ventas_details, ['GET']),
                    ('/start/', ventas_start, ['GET']),
                    ('/update/', ventas_update, ['GET']),
                    ('/cancel/', ventas_cancel, ['GET']),
                    ('/confirm/', ventas_confirm, ['GET']),
                    ]

base_url_rules = [('/', hello, ['GET'])]

for (rule, func, methods) in productos_url_rules:
    productos_bp.add_url_rule(rule, view_func=func, methods=methods)

for (rule, func, methods) in compras_url_rules:
    compras_bp.add_url_rule(rule, view_func=func, methods=methods)

for (rule, func, methods) in ventas_url_rules:
    ventas_bp.add_url_rule(rule, view_func=func, methods=methods)

for (rule, func, methods) in base_url_rules:
    base_bp.add_url_rule(rule, view_func=func, methods=methods)
