from tent import ma
from tent import db
from dateutil.parser import parse
from sqlalchemy.orm import relationship
from pandas import DataFrame


class CompraSchema(ma.Schema):
    class Meta:
        fields = ('idCompra', 'idProveedor', 'montoTotal',
                  'montoNeto', 'fecha', 'tipoDocumento')

# dejar los campos que correspondan


class Compra(db.Model):
    __tablename__ = 'Compra'  # No sé si es necesario, pero creo que si
    idCompra = db.Column(db.Integer, primary_key=True)
    # idProveedor = relationship(
    #    "Proveedor", back_populates="compra", uselist=False)
    montoTotal = db.Column(db.Integer)
    montoNeto = db.Column(db.Integer)
    fecha = db.Column(db.Date)
    tipoDocumento = db.Column(db.String(20))
    folio = db.Column(db.Integer)
    # una compra tiene UN PROVEEDOR
    idProveedor = db.Column(db.Integer, db.ForeignKey('Proveedor.idProveedor'))
    proveedor = relationship("Proveedor", back_populates="compras")

    # Campos minimos para hacer POST
    def __init__(self, datos: dict, productos: DataFrame):
        self.montoTotal = datos['montoTotal']
        self.montoNeto = datos['montoNeto']
        self.fecha = datos['fecha']
        self.tipoDocumento = datos['tipoDoc']
        self.folio = datos['folio']

    def get_id(self):
        return self.idCompra
    # inicializar con los campos que estimen conveniente

    @classmethod
    def from_df(cls, df_datos, df_productos):
        ddf = df_datos.iloc[0].to_dict()
        return cls(ddf['montoTotal'],
                   ddf['montoNeto'],
                   parse(ddf['fecha']),
                   ddf['tipoDoc'],
                   ddf['folio'],)  # etc
