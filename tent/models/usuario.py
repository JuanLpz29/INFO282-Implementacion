from tent.models import ma
from tent.models import db
from sqlalchemy.orm import relationship


class UsuarioSchema(ma.Schema):
    class Meta:
        fields = ('idUsuario', 'nombre', 'rol', 'contraseña')


class Usuario(db.Model):
    __tablename__ = 'Usuario'
    idUsuario = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    rol = db.Column(db.String(15))
    contraseña = db.Column(db.String(15))
    # un usuario tiene N VENTAS
    ventas = relationship("Venta", back_populates="usuario")

    # Campos minimos para hacer POST
    def __init__(self, nombre, rol, contraseña):
        self.nombre = nombre
        self.rol = rol
        self.contraseña = contraseña

    def get_id(self):
        return self.idUsuario

    @classmethod
    def from_dict(cls, datos):
        return cls(datos['nombre'],
                   datos['rol'],
                   datos['contraseña'],)  # etc
