from tent.models import ma
from tent.models import db
from sqlalchemy.orm import relationship

ADMIN = "Admin"
VENDEDOR = "Vendedor"


class UsuarioSchema(ma.Schema):
    class Meta:
        fields = ('idUsuario', 'nombre', 'rol', 'contraseña')


class Usuario(db.Model):
    __tablename__ = 'Usuario'
    idUsuario = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    rol = db.Column(db.String(15))
    contraseña = db.Column(db.String(15))
    ventas = relationship("Venta", back_populates="usuario")
    _is_authenticated = True
    _is_active = True

    def __init__(self, nombre, rol, contraseña):
        self.nombre = nombre
        self.rol = rol
        self.contraseña = contraseña

    def get_id(self):
        return self.idUsuario

    @property
    def is_authenticated(self):
        return self._is_authenticated

    @is_authenticated.setter
    def is_authenticated(self, value):
        self._is_authenticated = value

    @property
    def is_active(self):
        return self._is_active

    @is_active.setter
    def is_active(self, value):
        self._active = value

    @classmethod
    def from_dict(cls, datos):
        return cls(datos['nombre'],
                   datos['rol'],
                   datos['contraseña'],)  # etc
