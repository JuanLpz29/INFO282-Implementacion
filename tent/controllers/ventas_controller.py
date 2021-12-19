from flask import request, jsonify
from sqlalchemy.sql.expression import and_, text
from tent.models.venta import Venta, VentaSchema
from tent.models.venta import EN_CURSO, CONFIRMADA, ANULADA, PAGADA, NO_FINALIZADA
from tent import db
from tent.controllers.productos_controller import query_many_productos_by
from tent.controllers.productos_controller import actualizar_stock, abort_if_no_producto_found
from tent.controllers.usuarios_controller import query_user_by, abort_if_no_usuario, abort_if_not_authorized, query_venta_en_curso_usuario
from tent.models.producto import Producto, ProductSchema
from tent.models.usuario import Usuario, UsuarioSchema, ADMIN, VENDEDOR
from tent.models.productoventa import ProductoVenta
from flask_restful import Resource, reqparse, abort
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
        abort(
            409, message=f"idUsuario {idUsuario} ya tiene una venta en curso idVenta:{venta.idVenta}")


def abort_if_invalid_status(venta: Venta, valid_status=EN_CURSO) -> None:
    if venta.estado != valid_status:
        abort(
            400, message=f"Venta con id: {venta.idVenta} no se encuentra {valid_status}")


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
        medio = args['medio']
        venta.medioDePago = medio
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
        barcode, _set, cantidad = args['codigoBarra'], args['set'], args['cantidad']
        venta = abort_if_no_venta_found(idVenta)
        abort_if_invalid_status(venta, valid_status=EN_CURSO)
        prod = abort_if_no_producto_found('codigoBarra', barcode)
        pv = self.pv_query_one(idVenta, prod.idProducto)

        if pv:
            # aqui se puede validar que la venta no este solicitando
            # mas productos de los que hay en el inventario
            # mientras el inventario no se haya estabilizado por completo se
            # agregan te todas formas y el stock se deja >= 0
            qty = cantidad - pv.cantidad if _set else cantidad
            pv.cantidad += qty
        # si no, se agrega uno a la venta
        else:
            pv = ProductoVenta(cantidad=1)
            pv.producto = prod
            pv.precio = prod.valorItem
            pv.venta = venta
            qty = 1

        print('cantidad', qty)
        actualizar_stock(producto=prod, cantidad=qty)
        venta.total += prod.valorItem * qty
        prod_info = producto_schema.dump(prod)
        prod_info['cantidad'] = pv.cantidad
        prod_info['subtotal'] = pv.cantidad * prod.valorItem
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
        self.update_prods_parser.add_argument('cantidad', type=int,
                                              location=self.args_loc,
                                              default=1,
                                              )
        self.update_prods_parser.add_argument('codigoBarra', type=str,
                                              location=self.args_loc,
                                              required=True,
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
        self.payment_parser.add_argument('medio', type=str,
                                         location=self.args_loc,
                                         choices=['Efectivo',
                                                  'Debito', 'Credito'],
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

    def get(self):
        args = self.pagination_parser.parse_args()
        _order_by = f"{args['sortby']} {args['order']}" if args['sortby'] else ""
        filtered_query = Venta.query.order_by(text(_order_by))
        rowsNumber = filtered_query.count()
        all_ventas = filtered_query.paginate(
            page=args['page'], per_page=args['perpage'])
        result = ventas_schema.dump(all_ventas.items)
        return jsonify(items=result,
                       rowsNumber=rowsNumber)

    def post(self):
        args = self.post_parser.parse_args()
        nombre, barcode = args['nombre'], args['codigoBarra']
        usuario = abort_if_no_usuario('nombre', nombre)
        abort_if_has_venta_en_curso(usuario.idUsuario)
        abort_if_no_producto_found('codigoBarra', barcode)
        venta = Venta(usuario.idUsuario)
        usuario.ventas.append(venta)
        prod = actualizar_stock(barcode=barcode)
        if prod:
            pv = ProductoVenta(cantidad=1, precio=prod.valorItem)
            pv.producto = prod
            pv.venta = venta
            venta.total = prod.valorItem
            prod_info = producto_schema.dump(prod)
            prod_info['cantidad'] = pv.cantidad
            prod_info['subtotal'] = pv.cantidad * prod.valorItem
        else:
            # front debe registrarlo
            # prod_info = None
            prod_info = 'bruh'
        db.session.add(usuario)
        db.session.commit()
        return jsonify(venta=venta_schema.dump(venta),
                       producto=prod_info)
