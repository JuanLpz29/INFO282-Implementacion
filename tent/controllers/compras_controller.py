from logging import DEBUG
from operator import add
from flask import redirect, request, jsonify
from tent.models import producto
from tent.models import proveedor
from tent.models.compra import Compra, CompraSchema
from tent.utils.DTE import DTE
from tent import db
from tent.controllers.productos_controller import productos_compra_json
from tent.controllers.productos_controller import add_or_update
from tent.controllers.productos_controller import get_many as get_many_prods
from tent.models.proveedor import Proveedor, ProveedorSchema
from tent.models.producto import ProductSchema
from tent.models.productoscompra import ProductoCompra
import json
from sqlalchemy.dialects.mysql import insert
# from DTE import DTE

DEBUGXD = True

compra_schema = CompraSchema()
proveedor_schema = ProveedorSchema()
compras_schema = CompraSchema(many=True)
productos_schema = ProductSchema(many=True)

# NO SE SI HAY UNA FORMA MEJOR PARA MANEJAR LOS PRODUCTOS
# DENTOR DE LA COMPRA... OTRA TABLA POR LA RELACION ESA?fal


def index():
    all_compras = Compra.query.paginate(page=1, per_page=30)
    result = compras_schema.dump(all_compras.items)
    return jsonify(result)


# Retornamos solo un compra de la base de datos
def show(idCompra):
    compra = Compra.query.get(idCompra)
    if compra is not None:
        return compra_schema.jsonify(compra)
    return f"no se encontro Compra con id {idCompra}"


def details(idCompra):
    compra = Compra.query.get(idCompra)
    if compra is None:
        return f"no se encontro Compra con id {idCompra}"
    compra_info = compra_schema.dump(compra)
    pcs = ProductoCompra.query.filter(
        ProductoCompra.idCompra == idCompra)
    productos_id = [pc.idProducto for pc in pcs]
    prods = get_many_prods(productos_id)
    print(compra_info['idProveedor'])
    _prov = Proveedor.query.filter(Proveedor
                                   .idProveedor == compra_info['idProveedor']).first()
    prov = proveedor_schema.dump(_prov)
    # print(prods)
    for (pc, prod) in zip(pcs, prods):
        if pc.idProducto != prod['idProducto']:
            print('f')
        else:
            prod['stock'] = pc.cantidad
    response = jsonify(info=compra_info,
                       proveedor=prov,
                       productos=prods,
                       )

    return response


def _allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ['xml']


def check_and_dump_products(datos_compra: dict, lista_productos: list[dict]):
    cmp = Compra.query.filter_by(folio=datos_compra['folio']).first()
    prods = productos_compra_json(lista_productos)
    prods_dump = productos_schema.dump(prods)
    if cmp is not None and DEBUGXD:
        print('la compra ya se encuentra registrada en el sistema!!')
    return prods_dump, cmp


def upload_json():
    body = request.data.decode()
    body_json = json.loads(body)
    if body_json['registrada'] == True:
        return "ya existe"  # porsiaca

    datos_proveedor = body_json['proveedor']
    prov = Proveedor.query.filter_by(rut=datos_proveedor['rut']).first()
    if prov is None:
        prov = Proveedor.from_dict(datos_proveedor)

    cmp = Compra.from_dict(body_json['info'])
    # una comprita pal master
    prov.compras.append(cmp)
    _prods = productos_compra_json(body_json['productos'])
    prods = add_or_update(_prods)
    # cmp.productosCompra = []
    # manejar cambios en el precio
    for i, prod in enumerate(prods):
        if prod.idProducto is not None:
            qty = _prods[i].stock
        else:
            qty = prod.stock
        a = ProductoCompra(cantidad=qty)
        a.producto = prod
        a.compra = cmp
    db.session.add(prov)
    db.session.commit()
    return "ok"


def upload_documento():
    # check if the post request has the file part
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files.get('file')
    if file.filename == '':
        print("NINGUN ARCHIVO SELECCIONADO")
        return redirect(request.url)
    if file and _allowed_file(file.filename):
        xml_compras = (file.read().decode())
        cmp = DTE(xml_compras)
        prods, _comp = check_and_dump_products(
            cmp.datos_dict, cmp.productos_compra)
        registrada = True if _comp is not None else False
        response = jsonify(info=cmp.datos_dict,
                           proveedor=cmp.proveedor_dict,
                           productos=prods,
                           registrada=registrada)
    return response
