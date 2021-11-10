from app import ma
from app import db
from numpy import isnan


class ProductSchema(ma.Schema):
    class Meta:
        fields = ('idProducto', 'nombre', 'descripcion', 'stock', 'categoria', 'formato', 'codigoBarra',
                  'foto', 'cantidadRiesgo', 'precioCompra', 'precioVenta', 'precioUnitario', 'valorItem')


class Producto(db.Model):
    __tablename__ = 'Producto'  # No sé si es necesario, pero creo que si
    idProducto = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), )
    descripcion = db.Column(db.String(50))
    stock = db.Column(db.Integer)
    categoria = db.Column(db.String(50))
    formato = db.Column(db.String(50))
    codigoBarra = db.Column(db.Integer)
    # foto
    cantidadRiesgo = db.Column(db.Integer)
    precioCompra = db.Column(db.Integer)
    precioVenta = db.Column(db.Integer)
    precioUnitario = db.Column(db.Integer)
    valorItem = db.Column(db.Integer)

    # Campos minimos para hacer POST
    def __init__(self, nombre, descripcion, stock, precioUnitario, valorItem, barcode):
        self.nombre = nombre
        self.descripcion = descripcion
        self.stock = stock
        self.precioUnitario = precioUnitario
        self.valorItem = valorItem
        if not isnan(barcode):
            print(barcode)
            self.codigoBarra = barcode

    @classmethod
    def from_dict(cls, prod_dict):
        try:
            price = int(prod_dict['Valor Item'].replace('.', ''))
        except AttributeError:
            price = 0
        return cls(prod_dict['nombre'],
                   prod_dict['descripcion'],
                   int(prod_dict['Stock']),
                   price,
                   price,
                   prod_dict['item_code'])
