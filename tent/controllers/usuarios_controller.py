from operator import ne
import re
from flask import redirect, url_for, request, jsonify
from sqlalchemy.sql.expression import text
# from tent.models.producto_compra import ProductoCompra
from tent import db
from sqlalchemy.dialects.mysql import insert
from sqlalchemy import func
import json
from tent.models.usuario import Usuario, UsuarioSchema

usuario_schema = UsuarioSchema()
usuario_schema = UsuarioSchema(many=True)


def index():
    all_users = Usuario.query.paginate(page=1, per_page=30)
    result = usuario_schema.dump(all_users.items)
    return jsonify(result)


# Retornamos solo un compra de la base de datos
def show(idUsuario):
    usuario = Usuario.query.get(idUsuario)
    if usuario is not None:
        return usuario_schema.jsonify(usuario)
    return f"no se encontro Compra con id {idUsuario}"


def store():
    body = request.data.decode()
    body_json = json.loads(body)
    new_user = Usuario.from_dict(body_json)
    # ver lo de INSERT ... ON DUPLICATE KEY UPDATE Statement
    db.session.add(new_user)
    db.session.commit()
    return "OK MI REY"
    # return product_schema.dumps(new_product)
