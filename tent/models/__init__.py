from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
# from sqlalchemy.orm import relationship
from sqlalchemy import Table, Column, Integer, ForeignKey

db = SQLAlchemy()
ma = Marshmallow()


productos_compra = Table('ProductosCompra', db.Model.metadata,
                         Column('idProducto', ForeignKey(
                             'Producto.idProducto')),
                         Column('idCompra', ForeignKey(
                             'Compra.idCompra'))
                         )
