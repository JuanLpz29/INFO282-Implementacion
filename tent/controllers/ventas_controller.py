from flask import request, jsonify
from flask_restful import Resource, reqparse, abort
from sqlalchemy.sql.expression import and_, text

from tent import db
from tent.models.venta import Venta, VentaSchema
from tent.models.venta import (
    EN_CURSO,
    CONFIRMADA,
    ANULADA,
    PAGADA,
    NO_FINALIZADA
)
from tent.controllers.productos_controller import query_many_productos_by
from tent.controllers.productos_controller import (
    actualizar_stock,
    abort_if_no_producto_found
)
from tent.controllers.usuarios_controller import (
    query_user_by,
    abort_if_no_usuario,
    abort_if_not_authorized,
    query_venta_en_curso_usuario
)
from tent.models.producto import Producto, ProductSchema
from tent.models.usuario import Usuario, UsuarioSchema, ADMIN, VENDEDOR
from tent.models.productoventa import ProductoVenta
from tent.utils.parsers import pagination_arg_parser


venta_schema = VentaSchema()
usuario_schema = UsuarioSchema()
ventas_schema = VentaSchema(many=True)
productos_schema = ProductSchema(many=True)
producto_schema = ProductSchema()


def query_venta_by(_key: str, _value: str):
    query_funcs = {
        'idVenta': Venta.query.get,
        'nombre': lambda x: Venta.query.filter(
            Venta.nombre == x).first(),
        'estado': lambda x: Venta.query.filter(
            Venta.estado == x).items(),
    }
    f = query_funcs.get(_key)
    if f is not None:
        return f(_value)


def abort_if_no_venta_found(idVenta: int) -> Venta:
    venta = Venta.query.get(idVenta)
    if venta is None:
        abort(404, message=f"No se encontro venta con id {idVenta}")
    return venta


def abort_if_has_venta_en_curso(idUsuario: int) -> Venta:
    venta = query_venta_en_curso_usuario(idUsuario)
    if venta is not None:
        msg = f"idUsuario {idUsuario} ya tiene una venta en curso"
        + " idVenta:{venta.idVenta}"
        abort(409, message=msg)


def abort_if_no_identifier(idProducto: int, codigoBarra: str):
    if idProducto:
        return ('idProducto', idProducto)
    if codigoBarra:
        return ('codigoBarra',codigoBarra)
    msg = "La solicitud debe incluir un codigoBarra o idProducto"
    abort(400, message=msg)


def abort_if_insufficient_stock(prod:Producto,cantidad:int):
    if cantidad> prod.stock:
        msg=f"El producto {prod.nombre} no tiene suficiente stock ({prod.stock})"
        abort(403, message=msg)


def abort_if_invalid_status(venta:Venta,valid_status=EN_CURSO) -> None:
    if venta.estado!=valid_status:
        msg=f"Venta con id: {venta.idVenta} no se encuentra {valid_status}"
        abort(400,message=msg)


class VentaManager(Resource):
    def __init__(self) -> None:
        super().__init__()
        self.update_prods_parser = reqparse.RequestParser()
        self.base_parser = reqparse.RequestParser()
        self.update_status_parser = reqparse.RequestParser()
        self.payment_parser = None
        self.args_loc = ['args', 'form', 'json']
        self.init_parsers()
        self.operation_methods = {'update': self.update_venta,
                                  'cancel': self.cancel_venta,
                                  'confirm': self.confirm_venta,
                                  'pay': self.pay_venta,
                                  'nullify': self.anular_venta}

    def get(self, idVenta):
        venta = abort_if_no_venta_found(idVenta)
        venta_info = venta_schema.dump(venta)
        pvs = self.pv_query(venta.idVenta)
        productos_id = [pc.idProducto for pc in pvs]
        _prods = productos_schema.dump(
            query_many_productos_by('idProducto', productos_id))
        _user = query_user_by('idUsuario', venta_info['idUsuario'])
        user = usuario_schema.dump(_user)

        user.pop('contraseña')
        prods_dict = {p['idProducto']: p for p in _prods}
        output_prods = []
        for pv in pvs:
            prod_json = prods_dict[pv.idProducto]
            prod_json['cantidad'] = pv.cantidad
            prod_json['stock'] = pv.cantidad
            prod_json['precioVenta'] = pv.precio
            output_prods.append(prod_json)

        response = jsonify(info=venta_info,
                           vendedor=user,
                           productos=output_prods,
                           )
        return response

    # update, cancelar, pagar, anular
    def put(self, idVenta):
        args = self.base_parser.parse_args()
        op = args['operation']
        return self.operation_methods[op](idVenta)

    def pv_query(self, idVenta):
        return ProductoVenta.query.filter(
            ProductoVenta.idVenta == idVenta)

    def pv_query_one(self, idVenta, idProducto):
        pv = ProductoVenta.query.filter(
            and_(
                ProductoVenta.idProducto == idProducto,
                ProductoVenta.idVenta == idVenta)
        ).first()
        return pv

    def check_conditions_for_status_update(self, idVenta, valid_status):
        args = self.update_status_parser.parse_args()
        nombre = args['nombre']
        venta = abort_if_no_venta_found(idVenta)
        abort_if_invalid_status(venta, valid_status=valid_status)
        usuario = abort_if_not_authorized(
            'nombre', nombre, idUsuario=venta.idUsuario)
        return venta, usuario

    def pay_venta(self, idVenta):
        venta, usuario = self.check_conditions_for_status_update(
            idVenta, CONFIRMADA)
        args = self.payment_parser.parse_args()
        medio = args['medioDePago']
        tipoDocumento = args['tipoDocumento']
        venta.medioDePago = medio
        venta.tipoDocumento = tipoDocumento
        venta.estado = PAGADA
        db.session.add(usuario)
        db.session.commit()
        return venta_schema.dump(venta)

    def confirm_venta(self, idVenta):
        venta, usuario = self.check_conditions_for_status_update(
            idVenta, EN_CURSO)
        venta.estado = CONFIRMADA
        venta.iva = int(venta.total * 0.19)
        venta.montoNeto = venta.total - venta.iva
        # calcular iva y monto neto
        db.session.add(usuario)
        db.session.commit()
        return venta_schema.dump(venta)

    def update_venta(self, idVenta):
        args = self.update_prods_parser.parse_args()
        venta = abort_if_no_venta_found(idVenta)
        abort_if_invalid_status(venta, valid_status=EN_CURSO)
        # se puede utilizar el id del producto o su codigo de barras
        barcode, idProducto = args['codigoBarra'], args['idProducto']
        identifier, value = abort_if_no_identifier(idProducto, barcode)
        _set, cantidad = args['set'], args['cantidad']
        prod = abort_if_no_producto_found('codigoBarra', barcode)
        pv = self.pv_query_one(idVenta, prod.idProducto)

        if pv:
            qty = cantidad - pv.cantidad if _set else cantidad
            pv.cantidad += qty
        else:
            qty = 1
            pv = ProductoVenta(cantidad=qty)
            pv.producto = prod
            pv.precio = prod.precioVenta
            pv.venta = venta
            qty = 1

        abort_if_insufficient_stock(prod, qty)
        actualizar_stock(producto=prod, cantidad=qty)
        venta.total += prod.precioVenta * qty
        prod_info = producto_schema.dump(prod)
        prod_info['cantidad'] = pv.cantidad
        prod_info['subtotal'] = pv.cantidad * prod.precioVenta
        # verificar que efectivamente se quita de la venta un producto
        # con cantidad 0
        if pv.cantidad == 0:
            db.session.delete(pv)
        db.session.add(venta)
        db.session.commit()
        return jsonify(venta=venta_schema.dump(venta),
                       producto=prod_info)

    def undo_stock_changes(self, venta, usuario, estado_final):
        prods_info = {
            prod.idProducto: prod.cantidad for prod in venta.productos
        }
        prods = Producto.query.filter(
            Producto.idProducto.in_(prods_info.keys())
        )
        for prod in prods:
            prod.stock += prods_info[prod.idProducto]

        # cancelar o anular la venta
        venta.estado = estado_final
        db.session.add(usuario)
        db.session.commit()
        return f"Venta {venta.idVenta} {estado_final}"

    def cancel_venta(self, idVenta):
        venta, usuario = self.check_conditions_for_status_update(
            idVenta, EN_CURSO)
        return self.undo_stock_changes(venta, usuario, NO_FINALIZADA)

    def anular_venta(self, idVenta):
        venta, usuario = self.check_conditions_for_status_update(
            idVenta, PAGADA)
        return self.undo_stock_changes(venta, usuario, ANULADA)

    def init_parsers(self):
        self.base_parser.add_argument('operation', type=str, required=True,
                                      choices=['update', 'cancel',
                                               'confirm', 'pay',
                                               'nullify'])

        # actualizar la venta en curso
        self.update_prods_parser.add_argument('codigoBarra', type=str,
                                              location=self.args_loc,
                                              required=True,
                                              )
        self.update_prods_parser.add_argument('idProducto', type=int,
                                              location=self.args_loc,
                                              default=0)
        self.update_prods_parser.add_argument('cantidad', type=int,
                                              location=self.args_loc,
                                              default=1,
                                              )
        self.update_prods_parser.add_argument('set', type=bool,
                                              location=self.args_loc,
                                              default=False,
                                              )

        # cancelar la venta en curso (estado -> no finalizada)
        self.update_status_parser.add_argument('nombre', type=str,
                                               location=self.args_loc,
                                               required=True,
                                               )
        self.payment_parser = self.update_status_parser.copy()
        self.payment_parser.add_argument('medioDePago', type=str,
                                         location=self.args_loc,
                                         choices=['Efectivo',
                                                  'Débito', 'Crédito'],
                                         required=True)
        self.payment_parser.add_argument('tipoDocumento', type=str,
                                         location=self.args_loc,
                                         choices=['Boleta',
                                                  'Factura',
                                                  'Guía de despacho'],
                                         required=True)


class VentaListManager(Resource):
    def __init__(self) -> None:
        super().__init__()
        self.pagination_parser = pagination_arg_parser.copy()
        self.post_parser = reqparse.RequestParser()
        self.post_parser.add_argument('nombre', type=str,
                                      location=['args', 'form', 'json'],
                                      required=True)

        self.post_parser.add_argument('codigoBarra', type=str,
                                      location=['args', 'form', 'json'],
                                      default='')

        self.post_parser.add_argument('idProducto', type=int,
                                      location=['args', 'form', 'json'],
                                      default=0)

    def get(self):
        args = self.pagination_parser.parse_args()
        if args['sortby']:
            _order_by = f"{args['sortby']} {args['order']}"
        else:
            _order_by = ""
        filtered_query = Venta.query.order_by(text(_order_by))
        rowsNumber = filtered_query.count()
        all_ventas = filtered_query.paginate(
            page=args['page'], per_page=args['perpage'])
        result = ventas_schema.dump(all_ventas.items)
        return jsonify(items=result,
                       rowsNumber=rowsNumber)

    def post(self):
        args = self.post_parser.parse_args()
        nombre = args['nombre']
        usuario = abort_if_no_usuario('nombre', nombre)
        # solo 1 venta activa por usuario
        abort_if_has_venta_en_curso(usuario.idUsuario)
        # se puede utilizar el id del producto o su codigo de barras
        barcode, idProducto = args['codigoBarra'], args['idProducto']
        identifier, value = abort_if_no_identifier(idProducto, barcode)
        prod = abort_if_no_producto_found(identifier, value)
        cantidad = 1
        abort_if_insufficient_stock(prod, cantidad)
        venta = Venta(usuario.idUsuario)
        usuario.ventas.append(venta)

        prod = actualizar_stock(producto=prod, cantidad=cantidad)
        pv = ProductoVenta(cantidad=1, precio=prod.precioVenta)
        pv.producto = prod
        pv.venta = venta
        venta.total = prod.precioVenta
        prod_info = producto_schema.dump(prod)
        prod_info['cantidad'] = pv.cantidad
        prod_info['subtotal'] = pv.cantidad * prod.precioVenta

        db.session.add(usuario)
        db.session.commit()
        return jsonify(venta=venta_schema.dump(venta),
                       producto=prod_info)
