from tent.models import ma
from tent.models import db
from dateutil.parser import parse
from sqlalchemy.orm import relationship


class CompraSchema(ma.Schema):
    class Meta:
        fields = ('idCompra', 'idProveedor', 'montoTotal',
                  'montoNeto', 'fecha', 'tipoDocumento')


class Compra(db.Model):
    __tablename__ = 'Compra'  # No sé si es necesario, pero creo que si
    idCompra = db.Column(db.Integer, primary_key=True)
    montoTotal = db.Column(db.Integer)
    montoNeto = db.Column(db.Integer)
    fecha = db.Column(db.Date)
    tipoDocumento = db.Column(db.String(20))
    folio = db.Column(db.Integer)
    # una compra tiene UN PROVEEDOR
    idProveedor = db.Column(db.Integer, db.ForeignKey('Proveedor.idProveedor'))
    proveedor = relationship("Proveedor", back_populates="compras")

    # Campos minimos para hacer POST
    def __init__(self, montoTotal, montoNeto, fecha, tipoDocumento, folio):
        self.montoTotal = montoTotal
        self.montoNeto = montoNeto
        self.fecha = fecha
        self.tipoDocumento = tipoDocumento
        self.folio = folio

    def get_id(self):
        return self.idCompra
    # inicializar con los campos que estimen conveniente

    @classmethod
    def from_dict(cls, dict_datos):
        return cls(dict_datos['montoTotal'],
                   dict_datos['montoNeto'],
                   dict_datos['fecha'],
                   dict_datos['tipoDocumento'],
                   dict_datos['folio'],)  # etc

    @classmethod
    def from_df(cls, df_datos):
        ddf = df_datos.iloc[0].to_dict()
        return cls.from_dict(ddf)
