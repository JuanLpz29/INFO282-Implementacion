from logging import DEBUG
from flask import redirect, request, jsonify
from sqlalchemy.sql.expression import and_
from tent.models.venta import Venta, VentaSchema
from tent import db
from tent.controllers.productos_controller import get_many as get_many_prods
from tent.controllers.productos_controller import actualizar_stock
from tent.models.producto import Producto, ProductSchema
from tent.models.usuario import Usuario, UsuarioSchema
from tent.models.productoventa import ProductoVenta
from tent.models.venta import Venta
import json
from sqlalchemy.dialects.mysql import insert
# from DTE import DTE

DEBUGXD = True

venta_schema = VentaSchema()
usuario_schema = UsuarioSchema()
ventass_schema = VentaSchema(many=True)
productos_schema = ProductSchema(many=True)

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
    return f"no se encontro Venta con id {idVenta}"


def start():
    username = request.args.get('user', '', type=str)
    if not username:
        return "user required", 400
    usuario = Usuario.query.filter(
        Usuario.nombre == username).first()
    if not usuario:
        return f"usuario {username} no econtrado", 401

    vnt = Venta(usuario.idUsuario)
    usuario.ventas.append(vnt)
    barcode = request.args.get('barcode', '', type=str)
    prod = actualizar_stock(barcode)
    if prod:
        a = ProductoVenta(cantidad=1)
        a.producto = prod
        a.venta = vnt
        vnt.total = prod.valorItem
        db.session.add(usuario)
        db.session.commit()
        return venta_schema.jsonify(vnt)

    return f"producto con barcode {barcode} no encontrado", 400


def update():
    _id = request.args.get('idVenta', None, type=int)
    if not _id:
        return "idVenta required", 400
    vnt = Venta.query.get(_id)
    if not vnt:
        return f"venta con {_id} no econtrada", 401

    if vnt.productos:
        vnt.productos[0]
    cantidad = request.args.get('cantidad', 1, type=int)
    barcode = request.args.get('barcode', '', type=str)
    if barcode:
        prod = actualizar_stock(barcode, cantidad)
        if prod:
            pv = ProductoVenta.query.filter(
                and_(
                    ProductoVenta.idProducto == prod.idProducto,
                    ProductoVenta.idVenta == _id)
            ).first()
            if pv:
                pv.cantidad += cantidad
            else:
                a = ProductoVenta(cantidad=1)
                a.producto = prod
                a.venta = vnt
            vnt.total += prod.valorItem * cantidad
            db.session.add(vnt)
            db.session.commit()
            return venta_schema.jsonify(vnt)
    return f"barcode piteao", 400


def details(idVenta):
    venta = Venta.query.get(idVenta)
    if venta is None:
        return f"no se encontro venta con id {idVenta}"
    venta_info = venta_schema.dump(venta)
    pvs = ProductoVenta.query.filter(
        ProductoVenta.idCompra == idVenta)
    productos_id = [pc.idProducto for pc in pvs]
    prods = get_many_prods(productos_id)
    print(venta_info['idUsuario'])
    _prov = Usuario.query.filter(Usuario
                                 .idUsuario == venta_info['idUsuario']).first()
    prov = usuario_schema.dump(_prov)
    # print(prods)
    for (pv, prod) in zip(pvs, prods):
        if pv.idProducto != prod['idProducto']:
            print('f')
        else:
            prod['stock'] = pv.cantidad
    response = jsonify(info=venta_info,
                       proveedor=prov,
                       productos=prods,
                       )

    return response
