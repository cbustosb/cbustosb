#!/usr/bin/env python3
import xml.etree.ElementTree as ET
import os
import logging
import subprocess
import base64
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_FILE = os.path.join(BASE_DIR, 'logs', 'create_envio.log')
logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                    format='%(asctime)s %(levelname)s:%(message)s')

EMISOR_RUT = '76146267-9'
RESOL_NUM = '80'
RESOL_FCH = '2014-08-22'
KEY_PATH = os.path.join(BASE_DIR, 'cert', 'key.pem')


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


def create_envio(dte_files, output_path):
    envio = ET.Element('EnvioDTE', version='1.0')
    setdte = ET.SubElement(envio, 'SetDTE')

    caratula = ET.SubElement(setdte, 'Caratula')
    ET.SubElement(caratula, 'RUTEmisor').text = EMISOR_RUT
    ET.SubElement(caratula, 'RUTEnvia').text = EMISOR_RUT
    ET.SubElement(caratula, 'FchResol').text = RESOL_FCH
    ET.SubElement(caratula, 'NroResol').text = RESOL_NUM
    ET.SubElement(caratula, 'TmstFirmaEnv').text = datetime.now().isoformat()

    for dte in dte_files:
        tree = ET.parse(dte)
        dte_elem = tree.getroot().find('Documento')
        if dte_elem is not None:
            setdte.append(dte_elem)

    tree = ET.ElementTree(envio)
    tree.write(output_path, encoding='utf-8', xml_declaration=True)

    sig = sign_file(output_path)
    sig_elem = ET.SubElement(envio, 'Signature')
    sig_elem.text = sig
    tree.write(output_path, encoding='utf-8', xml_declaration=True)

    logging.info('Envio creado %s', output_path)
    print(f'Envio creado en {output_path}')


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Crear EnvioDTE para SII')
    parser.add_argument('dte_files', nargs='+', help='Archivos DTE a incluir')
    parser.add_argument('--output', default='envio.xml', help='Archivo de salida')
    args = parser.parse_args()
    out = os.path.join(BASE_DIR, 'dte_emitidos', args.output)
    create_envio(args.dte_files, out)
