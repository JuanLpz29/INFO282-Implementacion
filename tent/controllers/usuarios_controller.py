from flask import redirect, url_for, request, jsonify
from sqlalchemy.sql.expression import and_, text
from tent import db
from tent.models.usuario import ADMIN, Usuario, UsuarioSchema
from tent.models.venta import Venta, EN_CURSO
from flask_restful import Resource, reqparse, abort
from flask_login import login_user, current_user, login_required, logout_user
from tent.utils.parsers import pagination_arg_parser

usuario_schema = UsuarioSchema()
usuarios_schema = UsuarioSchema(many=True)


def query_venta_en_curso_usuario(idUsuario):
    venta = Venta.query.filter(and_(
        Venta.idUsuario == idUsuario,
        Venta.estado == EN_CURSO
    )).first()

    return venta


def query_user_by(_key: str, _value: str):
    query_funcs = {'idUsuario': Usuario.query.get,
                   'nombre': lambda x: Usuario.query.filter(
                       Usuario.nombre == x).first(),
                   'rol': lambda x: Usuario.query.filter(
                       Usuario.rol == x).items(), }
    f = query_funcs.get(_key)
    if f is not None:
        return f(_value)


def abort_if_no_usuario(_key: str, _value: str) -> Usuario:
    usuario = query_user_by(_key, _value)
    if usuario is None:
        abort(404, message=f"No existe el usuario con {_key} {_value}")
    return usuario


def abort_if_not_authorized(key: str, value, idUsuario=None) -> Usuario:
    usuario = query_user_by(key, value)
    if usuario is not None:
        if usuario.rol == ADMIN or (idUsuario is not None and usuario.idUsuario == idUsuario):
            return usuario
    abort(
        401, message=f"El usuario con {key} {value} no esta autorizado para realizar esta operacion")


def abort_if_bad_login(usuario: str, contrasena: str) -> None:
    user = query_user_by('nombre', usuario)
    if user is None or user.contraseña != contrasena:
        abort(401, message=f"Datos incorrectos")
    return user


class UserManager(Resource):
    def get(self, idUsuario):
        usuario = abort_if_no_usuario('idUsuario', idUsuario)
        user_info = usuario_schema.dump(usuario)
        venta = query_venta_en_curso_usuario(idUsuario)
        if venta is not None:
            user_info['idVentaActiva'] = venta.idVenta
        user_info.pop('contraseña')
        return user_info

    def put(self, idUsuario):
        todito = request.form['data']
        return {idUsuario: todito}


class UserListManager(Resource):
    def __init__(self) -> None:
        # super().__init__()
        self.post_parser = reqparse.RequestParser()
        for _arg in ['nombre', 'contraseña', 'rol']:
            self.post_parser.add_argument(_arg, type=str,
                                          location=['form', 'json'],
                                          required=True)

    def get(self):
        args = pagination_arg_parser.parse_args()

        _order_by = f"{args['sortby']} {args['order']}" if args['sortby'] else ""
        filtered_query = Usuario.query.order_by(text(_order_by))
        rowsNumber = filtered_query.count()
        all_users = filtered_query.paginate(
            page=args['page'], per_page=args['perpage'])
        result = usuarios_schema.dump(all_users.items)
        return jsonify(items=result,
                       rowsNumber=rowsNumber)

    def post(self):
        args = self.post_parser.parse_args()
        nombre = args['nombre']
        user = query_user_by('nombre', nombre)
        if user is None:
            # validar que el usuario no se repita
            new_user = Usuario.from_dict(args)
            db.session.add(new_user)
            db.session.commit()
            return f"usuario: {args['nombre']}"
        abort(409, message=f"Ya existe un usuario con nombre {nombre}")


class UserLoginManager(Resource):
    def __init__(self) -> None:
        # super().__init__()
        self.post_parser = reqparse.RequestParser()
        for _arg in ['nombre', 'contraseña']:
            self.post_parser.add_argument(_arg, type=str,
                                          location=['form', 'json'],
                                          required=True)

    def post(self):
        args = self.post_parser.parse_args()
        nombre = args['nombre']
        contrasena = args['contraseña']
        user = abort_if_bad_login(nombre, contrasena)
        login_user(user, remember=True)
        user_info = usuario_schema.dump(user)
        user_info.pop('contraseña')
        user_info['message'] = 'logeao de pana'
        return user_info

    def get(self):
        return "Login required"


class UserLogout(Resource):

    @login_required
    def get(self):
        logout_user()
        return "xao"

    @login_required
    def post(self):
        logout_user()
        return "xao"
