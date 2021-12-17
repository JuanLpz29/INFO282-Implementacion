from flask_restful import reqparse

prod_args_parser = reqparse.RequestParser()
_prod_args_location = ['form', 'json']
arglist = [('nombre', str, True), ('precioVenta', int, True),
           ('codigoBarra', str, True), ('descripcion', str, False),
           ('stock', int, False), ('categoria', str, False),
           ('formato', str, False), ('cantidadRiesgo', int, False),
           ('precioUnitario', int, False)]

for arg, _type, required in arglist:
    prod_args_parser.add_argument(arg, type=_type,
                                  location=_prod_args_location,
                                  required=required)

pagination_arg_parser = reqparse.RequestParser()
pagination_arg_parser.add_argument('page', default=1, type=int,
                                   help='Page cannot be converted')
pagination_arg_parser.add_argument("perpage", default=10, type=int,
                                   help='perpage cannot be converted')
pagination_arg_parser.add_argument("filter", default="", type=str,)
pagination_arg_parser.add_argument("sortby", default="", type=str,)
pagination_arg_parser.add_argument("order", default="", type=str,
                                   choices=["ASC", "DESC", ""],)
