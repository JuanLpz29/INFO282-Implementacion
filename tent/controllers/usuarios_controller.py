from flask import redirect, url_for, request, jsonify
from sqlalchemy.sql.expression import text, or_
from tent import db
from tent.models.usuario import ADMIN, Usuario, UsuarioSchema
from flask_restful import Resource, reqparse, abort
from tent.controllers import pagination_arg_parser


usuario_schema = UsuarioSchema()
usuarios_schema = UsuarioSchema(many=True)


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


def abort_if_not_authorized(usuario: Usuario, idUsuario=None) -> None:
    if usuario.rol != ADMIN and (idUsuario is not None and usuario.idUsuario != idUsuario):
        abort(
            401, message=f"El usuario {usuario.nombre} no esta autorizado para realizar esta operacion")


class UserManager(Resource):
    # def abort_if_no_usuario(self, idUsuario):
    #     usuario = Usuario.query.get(idUsuario)
    #     if usuario is None:
    #         abort(404, message=f"No existe el usuario con id {idUsuario}")
    #     return usuario

    def get(self, idUsuario):
        usuario = abort_if_no_usuario('idUsuario', idUsuario)
        return usuario_schema.jsonify(usuario)

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

        _order_by = f"{args['sortby']} {args['order']}".strip()
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
