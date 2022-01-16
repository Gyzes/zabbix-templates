#!/bin/python3

import ssl
import sys
import socket
import OpenSSL
import argparse
import json
from datetime import datetime


def get_certificate(host, port=443, timeout=10):
    context = ssl.create_default_context()
    conn = socket.create_connection((host, port))
    sock = context.wrap_socket(conn, server_hostname=host)
    sock.settimeout(timeout)
    try:
        der_cert = sock.getpeercert(True)
    finally:
        sock.close()
    return ssl.DER_cert_to_PEM_cert(der_cert)


parser = argparse.ArgumentParser()
parser.add_argument("-u", "--url", help="website address", required=False)
parser.add_argument("-p", "--port", help="https port", required=False)
args = parser.parse_args()

if not args.url:
    with open('/usr/lib/zabbix/externalscripts/ssl_site_check.txt') as f:
        data = f.readlines()
    res = '{"data":  [\n'
    for row in data:
        res += ' { "{#URL}": "' + row.split(',')[0] + '", "{#PORT}": "' + row.split(',')[1][:-1] + '" },\n'
    res = res[:-2] + '\n]}'
    print(res)
else:
    if not args.port:
        port = 443
    else:
        port = args.port
    try:
        certificate = get_certificate(args.url, port=int(port))
    except Exception as err:
        result = {"error": err.args[1]}
        print(json.dumps(result))
        sys.exit()

    x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, certificate)

    result = {
        'subject': dict(x509.get_subject().get_components()),
        'issuer': dict(x509.get_issuer().get_components()),
        'serialNumber': x509.get_serial_number(),
        'version': x509.get_version(),
        'notBefore': datetime.strptime(x509.get_notBefore().decode(), '%Y%m%d%H%M%SZ'),
        'notAfter': datetime.strptime(x509.get_notAfter().decode(), '%Y%m%d%H%M%SZ'),
    }
    result = {"ISSUE": result['subject'][b'CN'].decode(), "ISSUER": result['issuer'][b'CN'].decode(),
              "NOTBEFORE": int(result['notBefore'].timestamp()), "NOTAFTER": int(result['notAfter'].timestamp()),
              "error": ""}
    print(json.dumps(result))
