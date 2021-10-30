import os
from flask import Blueprint, current_app

from app.controllers.productos_controller import index as products_index
from app.controllers.productos_controller import show as products_show
from app.controllers.productos_controller import destroy as products_destroy
from app.controllers.productos_controller import store as products_store
from app.controllers.productos_controller import update as products_update

from app.controllers.compras_controller import upload_documento as compras_store
from app.controllers.compras_controller import index as compras_index
from app.controllers.compras_controller import show as compras_show

productos_bp = Blueprint('productos', 'api', url_prefix='/productos')
compras_bp = Blueprint('compras', 'api', url_prefix='/compras')

productos_url_rules = [('/', products_index, ['GET']),
                       ('/<int:idProducto>/', products_show, ['GET']),
                       ]

compras_url_rules = [('/', compras_index, ['GET']),
                     ('/upload', compras_store, ['POST']),
                     ('/<int:idCompra>/', compras_show, ['GET']),
                     ]

for (rule, func, methods) in productos_url_rules:
    productos_bp.add_url_rule(rule, view_func=func, methods=methods)
for (rule, func, methods) in compras_url_rules:
    compras_bp.add_url_rule(rule, view_func=func, methods=methods)
