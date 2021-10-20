from xml_to_pdf_functions import sii_doc_XMLtoPDF, datos_xml_to_df
import re
from pathlib import Path


XML_VERSION = '<?xml version="1.0" encoding="ISO-8859-1"?>'
SETDTE_OPEN = '<SetDTE>'
SETDTE_CLOSE = '</SetDTE>'
DTE_OPEN = '<DTE version="1.0" >'
DTE_CLOSE = '</DTE>'
NEW_DTE_OPEN = '<DTE version="1.0" xmlns="http://www.sii.cl/SiiDte">'


def preprocess_xml(xml_file, n_compras):
    archivo_compra = ""
    for line in xml_file:
        archivo_compra += re.sub(r"(>)(\s+)(<)", r'\1\n\3', line)
    return split_xml(archivo_compra, n_compras)


# n_compras = 0 -> retornar todas las compras del archivo
def split_xml(xml_file, n_compras):
    xml_compras = []
    current = XML_VERSION + '\n' + SETDTE_OPEN + '\n'
    compras_found = 1
    for line in xml_file:
        if line.find(DTE_OPEN) >= 0:
            current += NEW_DTE_OPEN + '\n'
        elif line.find(DTE_CLOSE) >= 0:
            current += line + SETDTE_CLOSE + '\n'
            xml_compras.append(current)
            compras_found += 1
            if n_compras != 0 and compras_found > n_compras:
                return xml_compras
            current = XML_VERSION + '\n' + SETDTE_OPEN
        elif 'SetDTE' not in line and line.find(XML_VERSION) == -1:
            current += line
    if compras_found == 1:
        return [xml_file]
    return xml_compras


class TPDV:
    def __init__(self):
        self.compras = []
        self.ventas = []

    def subir_compras(self, xml_file, n_compras=1):
        archivos_compras = preprocess_xml(xml_file, n_compras)
        self.compras_found = len(archivos_compras)
        if self.compras_found < n_compras:
            print(
                f"error ymy solo se encontraron {self.compras_found} compras")
            n_compras = self.compras_found
        # no se si sirve de algo guardarlas aca
        for i in range(n_compras):
            self.compras.append(Compra(archivos_compras[i]))

    def mostrar_info_compras(self):
        for compra in self.compras:
            compra.print_info_compra()


class Compra:
    def __init__(self, xml_file):
        self.productos = []
        self.get_info_compra(xml_file)
        self.get_info_productos(xml_file)

    def get_info_compra(self, xml_file):
        df_datos = datos_xml_to_df(xml_file)
        dict_datos = df_datos.iloc[0].to_dict()
        # forma corta, no se ve que se esta agregando
        for key, value in dict_datos.items():
            setattr(self, key, value)
        """
        self.id = dict_datos['folio']
        self.tipo_documento = dict_datos['tipoDoc']
        self.monto_neto = int(dict_datos['montoNeto'])
        self.monto_iva = int(dict_datos['montoIVA'])
        self.monto_total = int(dict_datos['montoTotal'])
        self.proveedor = dict_datos['proveedor']
        self.fecha = dict_datos['fecha']
        """

    def get_info_productos(self, xml_file):
        df_productos = sii_doc_XMLtoPDF(
            xml_file)[['descripcion', 'qty', 'Valor Item']]
        for i in range(len(df_productos)):
            self.productos.append(Producto.from_df(df_productos.iloc[i]))
            # self.products[i].print_info()

    def print_info_compra(self):
        for key, value in self.__dict__.items():
            if key != 'productos':
                print(f"{key:>20} : {value}")
        self.print_productos()

    def print_productos(self):
        print("\n", "*"*30, "DETALLE", "*"*30, '\n')
        print(f"{'nobmre':<40} cantidad   presio compra")
        for prod in self.productos:
            prod.print_info()
        print("\n", "*"*69, '\n')


class Producto:
    def __init__(self, nombre, cantidad=None, precio_compra=None):
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio_compra = precio_compra

    @classmethod
    def from_df(cls, df_row):
        return cls(df_row['descripcion'],
                   cantidad=int(df_row['qty']),
                   precio_compra=int(df_row['Valor Item'].replace('.', '')))

    def print_info(self):
        print(f"{self.nombre:<43} {self.cantidad:<15} {self.precio_compra:}")
