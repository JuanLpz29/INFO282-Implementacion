from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from tent.models import ma, db
# from tent.models.compra import Compra
# from tent.models.producto import Producto


class ProductosCompra(db.Model):
    __tablename__ = 'ProductosCompra'
    idProducto = Column(ForeignKey('Producto.idProducto'),
                        primary_key=True)
    idCompra = Column(ForeignKey('Compra.idCompra'),
                      primary_key=True)
    cantidad = Column(Integer)
    producto = relationship("Producto", back_populates="compras")
    compra = relationship("Compra", back_populates="productos")
