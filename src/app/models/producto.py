from app import ma
from app import db


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
    def __init__(self, nombre, descripcion, stock, precioUnitario, valorItem):
        self.nombre = nombre
        self.descripcion = descripcion
        self.stock = stock
        self.precioUnitario = precioUnitario
        self.valorItem = valorItem

    @classmethod
    def from_df(cls, df_row):
        try:
            price = int(df_row['Valor Item'].replace('.', ''))
        except AttributeError:
            price = 0
        return cls(df_row['nombre'],
                   df_row['descripcion'],
                   int(df_row['qty']),
                   price,
                   price)

    def print_info(self):
        print(f"{self.nombre:<43} {self.cantidad:<15} {self.precioUnitario:}")
