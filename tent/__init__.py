from flask import Flask, Blueprint
import os
from flask_cors import CORS
from tent.models import db, ma
from flask_restful import Api


def create_app(config_filename=None):
    application = Flask(__name__, instance_relative_config=True)
    application.config.from_pyfile(config_filename)
    # initialize_extensions(application)
    # from tent.models import db, ma
    db.init_app(application)
    ma.init_app(application)

    api_bp = Blueprint('api', __name__)
    api = Api(api_bp)
    register_blueprints(application, api, api_bp)
    return application


# def initialize_extensions(application):
#     # probablemente imports innecesarios
#     from tent.models.producto import Producto, ProductSchema
#     from tent.models.compra import Compra, CompraSchema
#     from tent.models.proveedor import Proveedor, ProveedorSchema


def register_blueprints(application, api, api_bp):
    from tent.controllers import compras_bp, base_bp
    from tent.controllers.usuarios_controller import UserManager, UserListManager
    from tent.controllers.ventas_controller import VentaManager, VentaListManager
    from tent.controllers.productos_controller import ProductoManager, ProductoListManager

    api.add_resource(UserManager, '/usuarios/<int:idUsuario>',
                     '/usuarios/<int:idUsuario>/')
    api.add_resource(UserListManager, '/usuarios/')
    api.add_resource(VentaManager, '/ventas/<int:idVenta>',
                     '/ventas/<int:idVenta>/')
    api.add_resource(VentaListManager, '/ventas/')
    api.add_resource(ProductoManager,
                     '/productos/<int:idProducto>', '/productos/<int:idProducto>/')
    api.add_resource(ProductoListManager, '/productos/')
    CORS(compras_bp)
    CORS(base_bp)
    CORS(api_bp)
    application.register_blueprint(compras_bp)
    application.register_blueprint(base_bp)
    application.register_blueprint(api_bp)


_env = os.environ.get('FLASK_ENV')
if _env is None:
    _env = 'development'
# config_filename = os.path.abspath(os.path.dirname(
#     __file__)) + f"/../instance/{_env}.cfg"
config_filename = '../instance/production.cfg'
tent = Flask(__name__)
tent.config.from_pyfile(config_filename)
# tent.config.from_pyfile(config_filename)
db.init_app(tent)
ma.init_app(tent)
api = Api(tent)
