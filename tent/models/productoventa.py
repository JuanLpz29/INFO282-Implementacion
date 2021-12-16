from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from tent.models import ma, db
# from tent.models.compra import Compra
# from tent.models.producto import Producto


class ProductoVenta(db.Model):
    __tablename__ = 'ProductoVenta'
    idProducto = Column(ForeignKey('Producto.idProducto'),
                        primary_key=True)
    idVenta = Column(ForeignKey('Venta.idVenta'),
                     primary_key=True)
    cantidad = Column(Integer)
    precio = Column(Integer)
    producto = relationship("Producto", back_populates="ventas")
    venta = relationship("Venta", back_populates="productos")
