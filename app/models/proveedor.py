from app import ma
from app import db
from sqlalchemy.orm import relationship


class ProveedorSchema(ma.Schema):
    class Meta:
        fields = ('idProveedor', 'razonSocial', 'rut', 'comuna')


class Proveedor(db.Model):
    __tablename__ = 'Proveedor'  # No sé si es necesario, pero creo que si
    # sakar el digito verificador y usar int
    rut = db.Column(db.String(15), primary_key=True)
    razonSocial = db.Column(db.String(50))
    comuna = db.Column(db.String(50))
    # = relationship("Parent", back_populates="child")

    # Campos minimos para hacer POST
    def __init__(self, rut, nombre, comuna):
        self.rut = rut
        self.razonSocial = nombre
        self.comuna = comuna

    @classmethod
    def from_df(cls, df):
        df = df.iloc[0].to_dict()
        return cls(df['rut'],
                   df['proveedor'],
                   df['comuna'],)  # etc
