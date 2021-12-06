from flask import Flask
import os
from flask_cors import CORS
from tent.models import db, ma


def create_app(config_filename=None):
    application = Flask(__name__, instance_relative_config=True)
    application.config.from_pyfile(config_filename)
    # initialize_extensions(application)
    # from tent.models import db, ma
    db.init_app(application)
    ma.init_app(application)
    register_blueprints(application)
    return application


# def initialize_extensions(application):
#     # probablemente imports innecesarios
#     from tent.models.producto import Producto, ProductSchema
#     from tent.models.compra import Compra, CompraSchema
#     from tent.models.proveedor import Proveedor, ProveedorSchema


def register_blueprints(application):
    from tent.controllers import productos_bp, compras_bp, base_bp, ventas_bp
    CORS(compras_bp)
    CORS(productos_bp)
    CORS(ventas_bp)
    CORS(base_bp)
    application.register_blueprint(productos_bp)
    application.register_blueprint(compras_bp)
    application.register_blueprint(ventas_bp)
    application.register_blueprint(base_bp)


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
