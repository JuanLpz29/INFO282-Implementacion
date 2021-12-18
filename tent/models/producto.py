from numpy.core.fromnumeric import prod
from tent.models import ma, db
from numpy import isnan, nan
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from sqlalchemy.orm import relationship
from tent.models.productocompra import ProductoCompra
from tent.models.productoventa import ProductoVenta
from tent.models.compra import Compra
from tent.models.venta import Venta
# from tent.models.producto_compra import ProductoCompra
# from tent.models import ProductoCompra


class Producto(db.Model):
    __tablename__ = 'Producto'  # No sé si es necesario, pero creo que si
    idProducto = db.Column(db.Integer, primary_key=True, nullable=True)
    nombre = db.Column(db.String(50))
    descripcion = db.Column(db.String(50))
    stock = db.Column(db.Integer)
    categoria = db.Column(db.String(50), nullable=True)
    formato = db.Column(db.String(50), nullable=True)
    codigoBarra = db.Column(db.String(16))
    # foto
    cantidadRiesgo = db.Column(db.Integer, nullable=True)
    precioVenta = db.Column(db.Integer, nullable=True)
    precioUnitario = db.Column(db.Integer, nullable=True)
    valorItem = db.Column(db.Integer)
    ventas = relationship("ProductoVenta", back_populates="producto")
    compras = relationship("ProductoCompra", back_populates="producto")

    # comprasProducto = db.relationship(
    # "Compra", secondary=association_table, back_populates="productosCompra")

    # Campos minimos para hacer POST
    def __init__(self, nombre, stock, precioVenta, barcode, _dict=None):
        self.nombre = nombre
        self.stock = stock
        if precioVenta is not None:
            self.valorItem = int(precioVenta)
        else:
            self.precioVenta = round(
                int(_dict.get('precioUnitario') * 1.3) / 10) * 10
            self.valorItem = self.precioVenta
        if barcode is not None:
            if isinstance(barcode, str) or not isnan(barcode):
                self.codigoBarra = str(barcode)
        for key, value in _dict.items():
            setattr(self, key, value)

    @classmethod
    def from_dict(cls, prod_dict):
        return cls(
            prod_dict['nombre'],
            int(prod_dict['stock']),
            prod_dict.get('precioVenta'),
            barcode=prod_dict.get("codigoBarra"),
            _dict=prod_dict
        )


class ProductSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Producto
