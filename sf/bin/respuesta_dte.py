#!/usr/bin/env python3
import xml.etree.ElementTree as ET
import os
import logging
import subprocess
import base64
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_FILE = os.path.join(BASE_DIR, 'logs', 'respuesta_dte.log')
logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                    format='%(asctime)s %(levelname)s:%(message)s')

KEY_PATH = os.path.join(BASE_DIR, 'cert', 'key.pem')
EMISOR_RUT = '76146267-9'


def sign_file(path: str) -> str:
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


def create_respuesta(dte_folio: str, estado: str, output_path: str):
    root = ET.Element('RespuestaDTE')
    ET.SubElement(root, 'RUTRecep').text = EMISOR_RUT
    ET.SubElement(root, 'Folio').text = str(dte_folio)
    ET.SubElement(root, 'Estado').text = estado
    ET.SubElement(root, 'TmstFirmaResp').text = datetime.now().isoformat()

    tree = ET.ElementTree(root)
    tree.write(output_path, encoding='utf-8', xml_declaration=True)

    sig = sign_file(output_path)
    sig_elem = ET.SubElement(root, 'Signature')
    sig_elem.text = sig
    tree.write(output_path, encoding='utf-8', xml_declaration=True)

    logging.info('Respuesta creada %s', output_path)
    print(f'Respuesta creada en {output_path}')


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Crear respuesta de DTE')
    parser.add_argument('folio', help='Folio del DTE recibido')
    parser.add_argument('estado', choices=['ACEPTADO', 'RECHAZADO'],
                        help='Estado a informar')
    parser.add_argument('--output', default='respuesta.xml', help='Archivo salida')
    args = parser.parse_args()

    out = os.path.join(BASE_DIR, 'dte_emitidos', args.output)
    create_respuesta(args.folio, args.estado, out)
