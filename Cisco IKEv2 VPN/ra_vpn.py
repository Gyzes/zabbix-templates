#!/bin/python3

import sys
import subprocess
import argparse
import re


def get_command(snmp_oid, params='vq'):
    if args.snmpversion == '3':
        sh_cmd = 'snmpwalk -O {} -v 3 -a SHA -A "{}" -l authPriv -u {} -x AES -X "{}" {} {}'.format(params,
                                                                                                    args.authpass,
                                                                                                    args.username,
                                                                                                    args.privpass,
                                                                                                    args.host, snmp_oid)
    else:
        sh_cmd = 'snmpwalk -O {} -v {} -c "{}" {} {}'.format(params,
                                                             args.snmpversion,
                                                             args.community,
                                                             args.host,
                                                             snmp_oid)
    return sh_cmd


parser = argparse.ArgumentParser()
parser.add_argument("-v", "--snmpversion", help="snmp version 1/2c/3", required=True)
parser.add_argument("-c", "--community", help="snmp community for verion 1/2c")
parser.add_argument("-u", "--username", help="snmpv3 username")
parser.add_argument("-A", "--authpass", help="snmpv3 auth password")
parser.add_argument("-X", "--privpass", help="snmpv3 priv password")
parser.add_argument("-H", "--host", help="ip or hostname", required=True)
parser.add_argument("-i", "--snmpindex", help="snmpindex", required=True)
parser.add_argument("-m", "--method", help="time or tunaddress", required=True)
parser.add_argument("-r", "--remote", help="{#REMOTE} in zabbix template (VPN client)")
args = parser.parse_args()

command = 'snmpwalk -O n '

if args.snmpversion in ['1', '2c', '3']:
    pass
else:
    print('Incorrect snmp version')
    sys.exit()

if args.method == 'time':
    oid = '.1.3.6.1.4.1.9.9.171.1.2.2.1.8.1.4.194.84.250.77.9.24.'
    oid += ".".join([str(ord(x)) for x in args.remote]) + "." + str(args.snmpindex)
    reply = subprocess.check_output([str(get_command(oid))], shell=True)
    print(int(reply))

elif args.method == 'tunaddress':
    oid_remote = '.1.3.6.1.4.1.9.9.171.1.2.2.1.7.1.4.194.84.250.77.9.24.'
    oid_remote += ".".join([str(ord(x)) for x in args.remote]) + "." + str(args.snmpindex)
    remote_address = str(subprocess.check_output([str(get_command(oid_remote))], shell=True))[3:-5]

    oid_remote2 = '.1.3.6.1.4.1.9.9.171.1.3.2.1.5'
    remote_address2 = subprocess.check_output([str(get_command(oid_remote2, 'nq'))], shell=True)
    remote_addresses = re.findall(r'\.(\d{1,4}) "([0-9A-F]{2} [0-9A-F]{2} [0-9A-F]{2} [0-9A-F]{2})',
                                  str(remote_address2))

    for address in remote_addresses:
        if str(remote_address) == str(address[1]):
            index = address[0]
            break
    else:
        sys.exit()
    oid = '.1.3.6.1.4.1.9.9.171.1.3.3.1.10.{}.1'.format(index)
    tunaddress = subprocess.check_output([str(get_command(oid))], shell=True)[1:-3]
    print('.'.join([str(int(x, 16)) for x in str(tunaddress)[2:-1].split(' ')]))

else:
    print('Incorrect method')
    sys.exit()
