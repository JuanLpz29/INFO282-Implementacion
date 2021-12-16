from tent.models import ma
from tent.models import db
from sqlalchemy.orm import relationship
from tent.models.usuario import Usuario
from sqlalchemy.sql import func

EN_CURSO = "En Curso"
CONFIRMADA = "Confirmada"
ANULADA = "Anulada"
PAGADA = "Pagada"
NO_FINALIZADA = "No Finalizada"


class VentaSchema(ma.Schema):
    class Meta:
        fields = ('idVenta',
                  'idUsuario', 'medioDePago', 'estado',
                  'fecha', 'montoNeto', 'iva', 'total')


class Venta(db.Model):
    __tablename__ = 'Venta'
    idVenta = db.Column(db.Integer, primary_key=True)
    total = db.Column(db.Integer)
    medioDePago = db.Column(db.String(15), nullable=True)
    estado = db.Column(db.String(15), nullable=True)
    fecha = db.Column(db.DateTime,
                      onupdate=func.now(), nullable=True)
    montoNeto = db.Column(db.Integer)
    iva = db.Column(db.Integer)
    idUsuario = db.Column(db.Integer, db.ForeignKey('Usuario.idUsuario'))
    usuario = relationship("Usuario", back_populates="ventas")
    productos = relationship("ProductoVenta", back_populates="venta")

    def __init__(self, idUsuario):
        self.idUsuario = idUsuario
        self.total = 0
        self.estado = EN_CURSO

    def get_id(self):
        return self.idVenta
