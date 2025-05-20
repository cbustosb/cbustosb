#!/usr/bin/env python3
import json
import xml.etree.ElementTree as ET
import os
import logging
import subprocess
import base64
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_FILE = os.path.join(BASE_DIR, 'logs', 'create_dte.log')
logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                    format='%(asctime)s %(levelname)s:%(message)s')

EMISOR = {
    'RUTEmisor': '76146267-9',
    'RznSoc': 'INGENIERIA DE SISTEMAS ARTICLYNX SPA',
    'GiroEmis': 'Servicios informáticos',
    'DirOrigen': 'Canto del Valle 1951',
    'CmnaOrigen': 'Concepción',
    'Telefono': '+56 9 74309000',
    'CorreoEmisor': 'sii@articlynx.com',
    'Acteco': '620200',
}

CERT_PATH = os.path.join(BASE_DIR, 'cert', 'cert.pem')
KEY_PATH = os.path.join(BASE_DIR, 'cert', 'key.pem')


def sign_file(path: str) -> str:
    """Sign file with openssl and return base64 signature string."""
    sig_path = path + '.sig'
    try:
        subprocess.run(['openssl', 'dgst', '-sha256', '-sign', KEY_PATH,
                        '-out', sig_path, path], check=True)
        with open(sig_path, 'rb') as f:
            sig = base64.b64encode(f.read()).decode()
    finally:
        if os.path.exists(sig_path):
            os.remove(sig_path)
    return sig


def build_xml(data: dict) -> ET.ElementTree:
    folio = str(data['IdDoc']['Folio'])
    dte = ET.Element('DTE', version='1.0')
    documento = ET.SubElement(dte, 'Documento', ID=f'DTE{folio}')
    encabezado = ET.SubElement(documento, 'Encabezado')

    iddoc = ET.SubElement(encabezado, 'IdDoc')
    for k, v in data['IdDoc'].items():
        ET.SubElement(iddoc, k).text = str(v)

    emisor = ET.SubElement(encabezado, 'Emisor')
    for k, v in EMISOR.items():
        ET.SubElement(emisor, k).text = v

    receptor = ET.SubElement(encabezado, 'Receptor')
    for k, v in data['Receptor'].items():
        ET.SubElement(receptor, k).text = str(v)

    totales = ET.SubElement(encabezado, 'Totales')
    for k, v in data['Totales'].items():
        ET.SubElement(totales, k).text = str(v)

    # Detalle
    for det in data.get('Detalle', []):
        detalle = ET.SubElement(documento, 'Detalle')
        for k, v in det.items():
            ET.SubElement(detalle, k).text = str(v)

    # Referencias
    for ref in data.get('Referencias', []):
        referencia = ET.SubElement(documento, 'Referencia')
        for k, v in ref.items():
            ET.SubElement(referencia, k).text = str(v)

    return ET.ElementTree(dte)


def save_dte(tree: ET.ElementTree, tipo: str, folio: str) -> str:
    path = os.path.join(BASE_DIR, 'dte_emitidos', f'dte_{tipo}_{folio}.xml')
    tree.write(path, encoding='utf-8', xml_declaration=True)
    return path


def insert_signature(tree: ET.ElementTree, signature: str):
    documento = tree.find('.//Documento')
    sig = ET.SubElement(documento, 'Signature')
    sig.text = signature


def create_dte(json_path: str):
    with open(json_path) as f:
        data = json.load(f)

    tipo = str(data['IdDoc']['TipoDTE'])
    folio = str(data['IdDoc']['Folio'])
    tree = build_xml(data)
    path = save_dte(tree, tipo, folio)

    signature = sign_file(path)
    insert_signature(tree, signature)
    tree.write(path, encoding='utf-8', xml_declaration=True)

    logging.info('Created DTE %s', path)
    print(f'DTE creado en {path}')


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Crear DTE desde JSON')
    parser.add_argument('json_file', help='Ruta al archivo JSON con la definicion del DTE')
    args = parser.parse_args()
    create_dte(args.json_file)
