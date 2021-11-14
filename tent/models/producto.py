from tent.models import ma
from tent.models import db
from numpy import isnan, nan
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field


class Producto(db.Model):
    __tablename__ = 'Producto'  # No sé si es necesario, pero creo que si
    idProducto = db.Column(db.Integer, primary_key=True, nullable=True)
    nombre = db.Column(db.String(50))
    descripcion = db.Column(db.String(50))
    stock = db.Column(db.Integer)
    categoria = db.Column(db.String(50), nullable=True)
    formato = db.Column(db.String(50), nullable=True)
    codigoBarra = db.Column(db.Integer)
    # foto
    cantidadRiesgo = db.Column(db.Integer, nullable=True)
    precioCompra = db.Column(db.Integer, nullable=True)
    precioVenta = db.Column(db.Integer, nullable=True)
    precioUnitario = db.Column(db.Integer, nullable=True)
    valorItem = db.Column(db.Integer)

    # Campos minimos para hacer POST
    def __init__(self, nombre, descripcion, stock, precioUnitario, barcode=nan):
        self.nombre = nombre
        self.descripcion = descripcion
        self.stock = stock
        self.precioUnitario = precioUnitario
        self.valorItem = precioUnitario
        if isinstance(barcode, str) or not isnan(barcode):
            self.codigoBarra = barcode

    @classmethod
    def from_dict(cls, prod_dict):
        return cls(prod_dict['nombre'],
                   prod_dict['descripcion'],
                   int(prod_dict['stock']),
                   prod_dict['precioUnitario'],
                   prod_dict["codigoBarra"])


class ProductSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Producto
