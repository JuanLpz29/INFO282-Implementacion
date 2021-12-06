from logging import DEBUG
from flask import redirect, request, jsonify
from sqlalchemy.sql.expression import and_
from tent.models.venta import Venta, VentaSchema
from tent.models.venta import EN_CURSO, CONFIRMADA, ANULADA, PAGADA
from tent import db
from tent.controllers.productos_controller import get_many as get_many_prods
from tent.controllers.productos_controller import actualizar_stock
from tent.models.producto import Producto, ProductSchema
from tent.models.usuario import Usuario, UsuarioSchema, ADMIN, VENDEDOR
from tent.models.productoventa import ProductoVenta
import json
from sqlalchemy.dialects.mysql import insert
# from DTE import DTE


DEBUGXD = True

venta_schema = VentaSchema()
usuario_schema = UsuarioSchema()
ventass_schema = VentaSchema(many=True)
productos_schema = ProductSchema(many=True)
producto_schema = ProductSchema()

# NO SE SI HAY UNA FORMA MEJOR PARA MANEJAR LOS PRODUCTOS
# DENTOR DE LA COMPRA... OTRA TABLA POR LA RELACION ESA?fal


def index():
    all_ventas = Venta.query.paginate(page=1, per_page=30)
    result = venta_schema.dump(all_ventas.items)
    # return jsonify(result)
    return result


# Retornamos solo un compra de la base de datos
def show(idVenta):
    venta = Venta.query.get(idVenta)
    if Venta is not None:
        return venta_schema.jsonify(venta)
    return f"no se encontro Venta con id {idVenta}", 404


def start():
    username = request.args.get('user', '', type=str)
    if not username:
        return "user required", 401
    usuario = Usuario.query.filter(Usuario.nombre == username).first()
    if not usuario:
        return f"usuario {username} invalido", 401

    vnt = Venta.query.filter(and_(
        Venta.idUsuario == usuario.idUsuario,
        Venta.estado == EN_CURSO
    )).first()
    if not vnt:
        vnt = Venta(usuario.idUsuario)
        usuario.ventas.append(vnt)
    else:
        # no permitir iniciar una venta si hay una en curso
        # o seria mejor
        # - reiniciar la venta (cancelando la anterior)
        # - permitir tener varias ventas en curso
        return f"{username} ya tiene una venta en curso (id: {vnt.idVenta})"

    barcode = request.args.get('barcode', '', type=str)
    prod = actualizar_stock(barcode=barcode)
    if prod:
        a = ProductoVenta(cantidad=1)
        a.producto = prod
        a.venta = vnt
        vnt.total = prod.valorItem

    db.session.add(usuario)
    db.session.commit()
    return venta_schema.dump(vnt)


# POR USERNAME O POR IDUSUARIO?
def update():
    _id = request.args.get('idVenta', None, type=int)
    if not _id:
        return "idVenta required", 400
    vnt = Venta.query.get(_id)
    if not vnt:
        return f"venta con id: {_id} no econtrada", 404
    elif vnt.estado != EN_CURSO:
        return f"venta con id: {_id} ya se encuentra econtrada {vnt.estado}", 400

    cantidad = request.args.get('cantidad', 1, type=int)
    barcode = request.args.get('barcode', '', type=str)
    if not barcode:
        return "barcode required", 400
    prod = Producto.query.filter(
        Producto.codigoBarra == barcode).first()
    if not prod:
        return f"producto con barcode: {barcode} no econtrado", 404
    pv = ProductoVenta.query.filter(
        and_(
            ProductoVenta.idProducto == prod.idProducto,
            ProductoVenta.idVenta == _id)
    ).first()
    if pv:
        if cantidad > 0:
            qty = cantidad if prod.stock > cantidad else prod.stock
        else:
            qty = -pv.cantidad if (cantidad + pv.cantidad) < 0 else cantidad
        pv.cantidad += qty
    else:
        pv = ProductoVenta(cantidad=1)
        pv.producto = prod
        pv.venta = vnt
        qty = 1

    actualizar_stock(producto=prod, cantidad=qty)
    vnt.total += prod.valorItem * qty
    db.session.add(vnt)
    db.session.commit()
    prod_info = producto_schema.dump(prod)
    prod_info['cantidadReservada'] = pv.cantidad
    return jsonify(venta=venta_schema.dump(vnt),
                   producto=prod_info)


def check_args():
    # cambair codigo repetitivo de validacion de args
    pass

# POR USERNAME O POR IDUSUARIO?


def cancel():
    _id = request.args.get('idVenta', None, type=int)
    username = request.args.get('user', '', type=str)

    if not _id or not username:
        return "idVenta y user requeridos", 400
    vnt = Venta.query.get(_id)
    if not vnt:
        return f"venta con {_id} no econtrada", 404

    usuario = Usuario.query.filter(Usuario.nombre == username).first()
    if not usuario:
        return "permiso penegado", 401
    if vnt.idUsuario != usuario.idUsuario and usuario.rol != ADMIN:
        return "permiso penegado", 401

    prods_info = {prod.idProducto: prod.cantidad for prod in vnt.productos}
    print(prods_info)
    prods = Producto.query.filter(
        Producto.idProducto.in_(prods_info.keys())
    )
    for prod in prods:
        prod.stock += prods_info[prod.idProducto]

    vnt.estado = ANULADA
    db.session.add(usuario)
    db.session.commit()
    return f"Venta {_id} cancelada"


def confirm():
    _id = request.args.get('idVenta', None, type=int)
    username = request.args.get('user', '', type=str)
    if not _id or not username:
        return "idVenta y user requeridos", 400
    vnt = Venta.query.get(_id)
    if not vnt:
        return f"venta con {_id} no econtrada", 404

    usuario = Usuario.query.filter(Usuario.nombre == username).first()
    if not usuario:
        return "permiso penegado", 401
    if vnt.idUsuario != usuario.idUsuario and usuario.rol != ADMIN:
        return "permiso penegado", 401
    vnt.estado = CONFIRMADA
    db.session.add(usuario)
    db.session.commit()
    return venta_schema.dump(vnt)


def details(idVenta):
    venta = Venta.query.get(idVenta)
    if venta is None:
        return f"no se encontro venta con id {idVenta}"
    venta_info = venta_schema.dump(venta)
    pvs = ProductoVenta.query.filter(
        ProductoVenta.idVenta == idVenta)
    productos_id = [pc.idProducto for pc in pvs]
    prods = get_many_prods(productos_id)
    print(venta_info['idUsuario'])
    _user = Usuario.query.filter(Usuario
                                 .idUsuario == venta_info['idUsuario']).first()
    user = usuario_schema.dump(_user)
    user.pop('contraseña')
    # print(prods)
    for (pv, prod) in zip(pvs, prods):
        if pv.idProducto != prod['idProducto']:
            print('f')
        else:
            prod['stock'] = pv.cantidad
    response = jsonify(info=venta_info,
                       vendedor=user,
                       productos=prods,
                       )

    return response
