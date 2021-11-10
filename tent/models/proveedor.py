from tent import ma
from tent import db
from sqlalchemy.orm import relationship


class ProveedorSchema(ma.Schema):
    class Meta:
        fields = ('idProveedor', 'razonSocial', 'rut', 'comuna')


class Proveedor(db.Model):
    __tablename__ = 'Proveedor'  # No sé si es necesario, pero creo que si
    # sakar el digito verificador y usar int
    idProveedor = db.Column(db.Integer, primary_key=True)
    rut = db.Column(db.String(15))
    razonSocial = db.Column(db.String(50))
    comuna = db.Column(db.String(50))
    # = relationship("Parent", back_populates="child")
    # un proveedor tiene N COMPRAS
    compras = relationship("Compra", back_populates="proveedor")

    # Campos minimos para hacer POST
    def __init__(self, rut, nombre, comuna):
        self.rut = rut
        self.razonSocial = nombre
        self.comuna = comuna

    def get_id(self):
        return self.idProveedor

    @classmethod
    def from_dict(cls, datos):
        return cls(datos['rut'],
                   datos['proveedor'],
                   datos['comuna'],)  # etc
