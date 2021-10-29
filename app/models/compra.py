from app import ma
from app import db
from dateutil.parser import parse
from sqlalchemy.orm import relationship


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

    # Campos minimos para hacer POST
    def __init__(self, total, neto, fecha, tipo, folio):
        self.montoTotal = total
        self.montoNeto = neto
        self.fecha = fecha
        self.tipoDocumento = tipo
        self.folio = folio

    # inicializar con los campos que estimen conveniente
    @classmethod
    def from_df(cls, df_datos, df_productos):
        ddf = df_datos.iloc[0].to_dict()
        return cls(ddf['montoTotal'],
                   ddf['montoNeto'],
                   parse(ddf['fecha']),
                   ddf['tipoDoc'],
                   ddf['folio'],)  # etc
