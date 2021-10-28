from app import ma
from app import db


class CompraSchema(ma.Schema):
    class Meta:
        fields = ('idCompra', 'nombre', 'descripcion', 'stock', 'categoria', 'formato', 'codigoBarra',
                  'foto', 'cantidadRiesgo', 'precioCompra', 'precioVenta', 'precioUnitario', 'valorItem')

# dejar los campos que correspondan


class Compra(db.Model):
    __tablename__ = 'Compra'  # No sé si es necesario, pero creo que si
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

    # inicializar con los campos que estimen conveniente
    @classmethod
    def from_df(cls, df_datos, df_productos):
        ddf = df_datos.iloc[0].to_dict()
        cls(ddf['folio'], ddf['tipo_documento'], )  # etc
