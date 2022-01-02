from flask import redirect, request, jsonify
from tent.models import producto
from tent.models import proveedor
from tent.models.compra import Compra, CompraSchema
from tent.utils.DTE import DTE
from tent import db
from tent.controllers.productos_controller import productos_from_json_list
from tent.controllers.productos_controller import add_or_update
from tent.controllers.productos_controller import query_many_productos_by
from tent.models.proveedor import Proveedor, ProveedorSchema
from tent.models.producto import ProductSchema
from tent.models.productocompra import ProductoCompra
import json
from sqlalchemy.dialects.mysql import insert
from flask_restful import Resource, reqparse, abort
from tent.utils.parsers import pagination_arg_parser
from sqlalchemy.sql.expression import and_, text
from werkzeug.datastructures import FileStorage
from typing import Tuple
from pprint import pprint


compra_schema = CompraSchema()
proveedor_schema = ProveedorSchema()
compras_schema = CompraSchema(many=True)
productos_schema = ProductSchema(many=True)


def _allowed_file(filename: str) -> bool:
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ['xml']


def check_and_dump_products(datos_compra: dict, lista_productos: list[dict]) -> Tuple[list[dict], Compra]:
    cmp = query_compra_by('folio', datos_compra['folio'])
    cmp = Compra.query.filter_by(folio=datos_compra['folio']).first()
    prods = productos_from_json_list(lista_productos)
    prods_dump = productos_schema.dump(prods)
    if cmp is not None:
        print('la compra ya se encuentra registrada en el sistema!!')
    return prods_dump, cmp


def query_compra_by(_key: str, _value: str) -> Compra:
    query_funcs = {

        'idCompra': Compra.query.get,
        'folio': lambda x: Compra.query.filter(
            Compra.folio == x).first()
    }
    f = query_funcs.get(_key)
    if f is not None:
        return f(_value)


def abort_if_no_compra_found(idCompra: int) -> Compra:
    compra = Compra.query.get(idCompra)
    if compra is None:
        abort(404, message=f"No se encontro compra con id {idCompra}")
    return compra


def abort_if_compra_exists(key: str, value: any) -> Compra:
    compra = query_compra_by(key, value)
    if compra is not None:
        abort(409, message=f"ya existe compra con {key} {value}")


class CompraManager(Resource):
    def __init__(self) -> None:
        super().__init__()
        self.args_loc = ['args', 'form', 'json']

    def get(self, idCompra):
        compra = abort_if_no_compra_found(idCompra)
        compra_info = compra_schema.dump(compra)
        pcs = self.pc_query(compra.idCompra)

        productos_id = [pc.idProducto for pc in pcs]

        _prods = productos_schema.dump(
            query_many_productos_by('idProducto', productos_id))

        _prov = Proveedor.query.filter(Proveedor
                                       .idProveedor == compra_info['idProveedor']).first()
        prov = proveedor_schema.dump(_prov)

        prods_dict = {p['idProducto']: p for p in _prods}
        output_prods = []
        for pc in pcs:
            prod_json = prods_dict[pc.idProducto]
            prod_json['cantidad'] = pc.cantidad
            prod_json['stock'] = pc.cantidad
            prod_json['precioUnitario'] = pc.precio
            output_prods.append(prod_json)

        response = jsonify(info=compra_info,
                           proveedor=prov,
                           productos=output_prods,
                           )
        return response

    def pc_query(self, idCompra):
        return ProductoCompra.query.filter(
            ProductoCompra.idCompra == idCompra)


class CompraListManager(Resource):
    def __init__(self) -> None:
        super().__init__()
        self.init_parsers()
        self.operation_methods = {'documento': self.process_file,
                                  'json': self.upload_json}

    def init_parsers(self) -> None:
        self.pagination_parser = pagination_arg_parser.copy()
        self.base_post_parser = pagination_arg_parser.copy()
        self.base_post_parser.add_argument('uploading', type=str,
                                           required=True,
                                           choices=['documento', 'json'])

        self.post_document_parser = reqparse.RequestParser()
        self.post_document_parser.add_argument('file',
                                               type=FileStorage,
                                               location='files')
        self.post_json_parser = reqparse.RequestParser()
        # el server no deberia confiar y validar por su cuenta
        # self.post_json_parser.add_argument('registrada',
        #                                    type=bool,
        #                                    location='json',
        #                                    required=True)
        self.post_json_parser.add_argument('proveedor',
                                           type=dict,
                                           location='json',
                                           required=True)
        self.post_json_parser.add_argument('info',
                                           type=dict,
                                           location='json',
                                           required=True)
        self.post_json_parser.add_argument('productos',
                                           type=list,
                                           location='json',
                                           required=True)

    def process_file(self):
        args = self.post_document_parser.parse_args()
        file = args['file']
        # abort if invalid file
        if file and _allowed_file(file.filename):
            xml_compras = (file.read().decode())
            cmp = DTE(xml_compras)
            # pprint(cmp.get_productos_compra())
            prods, _comp = check_and_dump_products(
                cmp.datos_dict, cmp.productos_compra)
            registrada = True if _comp is not None else False
            response = jsonify(info=cmp.datos_dict,
                               proveedor=cmp.proveedor_dict,
                               productos=prods,
                               registrada=registrada)
        return response

    def upload_json(self):
        args = self.post_json_parser.parse_args()
        info_compra = args['info']
        abort_if_compra_exists('folio', info_compra['folio'])
        info_proveedor = args['proveedor']
        info_productos = args['productos']
        prov = Proveedor.query.filter_by(rut=info_proveedor['rut']).first()
        if prov is None:
            prov = Proveedor.from_dict(info_proveedor)

        compra = Compra.from_dict(info_compra)
        prov.compras.append(compra)
        _prods = productos_from_json_list(info_productos)
        prods = add_or_update(_prods)
        for prod in prods:
            pc = ProductoCompra(cantidad=prod.stock)
            pc.producto = prod
            pc.compra = compra
            pc.precio = prod.precioUnitario

        db.session.add(prov)
        db.session.commit()
        return "Compra registrada satisfactoriamente"

    def get(self):
        args = self.pagination_parser.parse_args()
        _order_by = f"{args['sortby']} {args['order']}" if args['sortby'] else ""
        filtered_query = Compra.query.order_by(text(_order_by))
        rowsNumber = filtered_query.count()
        all_compras = filtered_query.paginate(
            page=args['page'], per_page=args['perpage'])
        result = compras_schema.dump(all_compras.items)
        return jsonify(items=result,
                       rowsNumber=rowsNumber)

    # update, cancelar, pagar, anular
    def post(self):
        args = self.base_post_parser.parse_args()
        op = args['uploading']
        return self.operation_methods[op]()
