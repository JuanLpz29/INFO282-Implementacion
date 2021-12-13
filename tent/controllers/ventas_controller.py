from logging import DEBUG
from flask import redirect, request, jsonify
from sqlalchemy.sql.expression import and_, text
from tent.models.venta import Venta, VentaSchema
from tent.models.venta import EN_CURSO, CONFIRMADA, ANULADA, PAGADA
from tent import db
from tent.controllers.productos_controller import get_many as get_many_prods
from tent.controllers.productos_controller import actualizar_stock
from tent.models.producto import Producto, ProductSchema
from tent.models.usuario import Usuario, UsuarioSchema, ADMIN, VENDEDOR
from tent.models.productoventa import ProductoVenta
from sqlalchemy.dialects.mysql import insert
from sqlalchemy import func

DEBUGXD = True

venta_schema = VentaSchema()
usuario_schema = UsuarioSchema()
ventas_schema = VentaSchema(many=True)
productos_schema = ProductSchema(many=True)
producto_schema = ProductSchema()


def index():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    # _filter = request.args.get('filter', '', type=str)
    sort_by = request.args.get('sortby', '', type=str)
    order = request.args.get('order', '', type=str)

    if sort_by:
        _order_by = f"{sort_by} {order}"
    else:
        _order_by = ""

    filtered_query = Venta.query.order_by(text(_order_by))

    rowsNumber = filtered_query.count()
    all_ventas = filtered_query.paginate(page=page, per_page=per_page)
    result = ventas_schema.dump(all_ventas.items)
    return jsonify(items=result,
                   rowsNumber=rowsNumber)


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
        return f"{username} ya tiene una venta en curso idVenta:{vnt.idVenta}"

    barcode = request.args.get('barcode', '', type=str)
    prod = actualizar_stock(barcode=barcode)
    if prod:
        pv = ProductoVenta(cantidad=1)
        pv.producto = prod
        pv.venta = vnt
        vnt.total = prod.valorItem
        prod_info = producto_schema.dump(prod)
        prod_info['cantidad'] = pv.cantidad
        prod_info['subtotal'] = pv.cantidad * prod.valorItem
    else:
        # front debe registrarlo
        prod_info = None
    db.session.add(usuario)
    db.session.commit()
    return jsonify(venta=venta_schema.dump(vnt),
                   producto=prod_info)


def update():
    _id = request.args.get('idVenta', None, type=int)
    cantidad = request.args.get('cantidad', 1, type=int)
    barcode = request.args.get('barcode', '', type=str)
    _set = request.args.get('set', False, type=bool)
    if not all([_id, barcode]) or cantidad < 0:
        return "idVenta y barcode, cantidad > 0 required", 400
    vnt = Venta.query.get(_id)
    if not vnt:
        return f"Venta con id: {_id} no econtrada", 404
    elif vnt.estado != EN_CURSO:
        return f"Venta con id: {_id} ya se encuentra {vnt.estado}", 400

    prod = Producto.query.filter(
        Producto.codigoBarra == barcode).first()
    if not prod:
        return f"Producto con barcode: {barcode} no encontrado", 404
    pv = ProductoVenta.query.filter(
        and_(
            ProductoVenta.idProducto == prod.idProducto,
            ProductoVenta.idVenta == _id)
    ).first()
    # si el producto ya estaba en la venta actual
    if pv:
        # aqui se puede validar que la venta no este solicitando
        # mas productos de los que hay en el inventario
        # mientras el inventario no se haya estabilidazo por completo se
        # agregan te todas formas y el stock se deja >= 0
        qty = cantidad - pv.cantidad if _set else cantidad
        print(qty, _set)
        pv.cantidad += qty
    # si no, se agrega uno a la venta
    else:
        pv = ProductoVenta(cantidad=1)
        pv.producto = prod
        pv.venta = vnt
        qty = 1

    actualizar_stock(producto=prod, cantidad=qty)
    vnt.total += prod.valorItem * qty
    prod_info = producto_schema.dump(prod)
    prod_info['cantidad'] = pv.cantidad
    prod_info['subtotal'] = pv.cantidad * prod.valorItem
    # verificar que efectivamente se quita de la venta un producto
    # con cantidad 0
    if pv.cantidad == 0:
        db.session.delete(pv)
    db.session.add(vnt)
    db.session.commit()
    return jsonify(venta=venta_schema.dump(vnt),
                   producto=prod_info)


def check_args():
    # cambair codigo repetitivo de validacion de args
    pass


def cancel():
    # obtener args
    _id = request.args.get('idVenta', None, type=int)
    username = request.args.get('user', '', type=str)

    # validacion de args
    if not _id or not username:
        return "idVenta y user requeridos", 400

    # validar venta
    vnt = Venta.query.get(_id)
    if not vnt:
        return f"venta con {_id} no econtrada", 404
    elif vnt.estado != EN_CURSO:
        return f"venta con id: {_id} ya se encuentra {vnt.estado}", 400

    # validar usuario que realiza la operacion
    # solo el mismo propietario de la venta o un admin puede cancelarla
    # seria mas rapido trabajar con el id
    usuario = Usuario.query.filter(Usuario.nombre == username).first()
    if not usuario:
        return "permiso penegado", 401
    if vnt.idUsuario != usuario.idUsuario and usuario.rol != ADMIN:
        return "permiso penegado", 401

    # devolver los productos
    prods_info = {prod.idProducto: prod.cantidad for prod in vnt.productos}
    print("id : cantidad \n", prods_info)
    prods = Producto.query.filter(
        Producto.idProducto.in_(prods_info.keys())
    )
    for prod in prods:
        prod.stock += prods_info[prod.idProducto]

    # anular la venta
    vnt.estado = ANULADA
    db.session.add(usuario)
    db.session.commit()
    return f"Venta {_id} cancelada"


def confirm():
    _id = request.args.get('idVenta', None, type=int)
    username = request.args.get('user', '', type=str)
    if not all([_id, username]):
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
    _prods = get_many_prods(productos_id)
    _user = Usuario.query.filter(Usuario
                                 .idUsuario == venta_info['idUsuario']).first()
    user = usuario_schema.dump(_user)
    user.pop('contraseña')
    prods_dict = {p['idProducto']: p for p in _prods}
    output_prods = []
    for pv in pvs:
        prod_json = prods_dict[pv.idProducto]
        prod_json['cantidad'] = pv.cantidad
        prod_json['stock'] = pv.cantidad
        output_prods.append(prod_json)

    response = jsonify(info=venta_info,
                       vendedor=user,
                       productos=output_prods,
                       )
    return response
