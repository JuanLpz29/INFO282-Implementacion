from tent.models import ma
from tent.models import db
from sqlalchemy.orm import relationship
from tent.models.usuario import Usuario

# tal vez sea mejor con herencia
# o simplemente tener un atributo
# el query por id deberia ser O(log n)
# class VentaTemporalSchema(ma.Schema):
#     class Meta:
#         fields = ('idVenta', 'idUsuario', 'total')


class VentaSchema(ma.Schema):
    class Meta:
        fields = ('idVenta', 'idUsuario', 'medioDePago', 'estado'
                  'fecha', 'total')


class Venta(db.Model):
    __tablename__ = 'Venta'
    idVenta = db.Column(db.Integer, primary_key=True)
    total = db.Column(db.Integer)

    # efectivo, debito, credito, tia me fia un super8
    medioDePago = db.Column(db.String(15), nullable=True)

    # en curso, confirmada, cancelada, pagada
    estado = db.Column(db.String(15))

    fecha = db.Column(db.DateTime, nullable=True)
    idUsuario = db.Column(db.Integer, db.ForeignKey('Usuario.idUsuario'))
    usuario = relationship("Usuario", back_populates="ventas")
    productos = relationship("ProductoVenta", back_populates="venta")

    def __init__(self, idUsuario):
        self.idUsuario = idUsuario
        # self.estado = "en curso"
        self.total = 0
        # self.productos = []

    def get_id(self):
        return self.idVenta
