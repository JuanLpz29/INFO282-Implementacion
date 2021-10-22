from xml_to_pdf_functions import sii_doc_XMLtoPDF, datos_xml_to_df
import re
from pathlib import Path
import pandas as pd
import json
from flask_sqlalchemy import SQLAlchemy  # Hace la conexión con la bd
# No cacho bien que hace pero es para poder mandar los cambios a la bd
from flask_marshmallow import Marshmallow


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


regexes = {'PET': r'^(.*PET)(?:\s)?(\d+)(?:CC)?(?:X)?(\d+)?.*',
           'CCX': r'^(.*?)(\d+)(?:CC)(?:X)(\d+).*',
           'LAT': r'^(.*?)(?: |_)(\d+)(?:.*?)(?:LAT|LATA)(\d+)(?:CC)?.*'}

nombres = pd.read_csv('codes_desc.csv')
nombres_dict = nombres.set_index('Original Code').to_dict()['description']
nombres_dict = {str(k): v for k, v in nombres_dict.items()}


def name_parser(key, desc):
    name = desc
    qty = None
    try:
        if key in ['PET', 'CCX']:
            _name, size, qty = re.match(regexes[key], desc).groups()
        elif key == 'LAT':
            _name, qty, size = re.match(regexes[key], desc).groups()
        name = f"{_name.title()} {size}CC"
    except AttributeError:
        # print(f'ERROR EN    "{desc}" ')
        pass
    except ValueError:
        # print('//////', desc)
        pass
    if qty is None:
        qty = 1
    return (name, int(qty))


def get_final_df(df):
    df.drop(columns=['Nro.', 'Código'], inplace=True)
    df['nombre'] = ""
    df.reset_index(inplace=True)
    for i, line in enumerate(df.iterrows()):
        desc = line[1].descripcion
        if 'PET' in desc:
            name, qty = name_parser('PET', desc)
        elif 'CCX' in desc:
            name, qty = name_parser('CCX', desc)
        elif 'LAT' in desc:
            name, qty = name_parser('LAT', desc)
        else:
            [name] = re.match(r'(?:\d{3,} )?(.*)', desc).groups()
            name, qty = name.title(), 1

        if nombres_dict.get(line[1].ean13) is not None:
            name = nombres_dict.get(line[1].ean13)
        df.at[i, 'nombre'] = name
        df.at[i, 'qty'] = qty * float(df.iloc[i].qty)
    return df


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
