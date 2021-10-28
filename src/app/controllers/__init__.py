import os
from flask import Blueprint, current_app

from app.controllers.productos_controller import index as products_index
from app.controllers.productos_controller import show as products_show
from app.controllers.productos_controller import destroy as products_destroy
from app.controllers.productos_controller import store as products_store
from app.controllers.productos_controller import update as products_update


from app.controllers.compras_controller import upload_documento as compras_store

productos_bp = Blueprint('productos', 'api')
productos_bp.add_url_rule('/productos', view_func=products_index,
                          methods=['GET'])
compras_bp = Blueprint('compras', 'api')
compras_bp.add_url_rule('/documento', view_func=compras_store,
                        methods=['GET', 'POST'])
# products_bp.add_url_rule('/', view_func=products_store,
#                          methods=['GET'])

# products_bp.add_url_rule('/', view_func=products_show,
#                          methods=['GET'])
# products_bp.add_url_rule('/', view_func=products_update,
#                          methods=['GET'])
# products_bp.add_url_rule('/', view_func=products_destroy,
#                          methods=['GET'])
