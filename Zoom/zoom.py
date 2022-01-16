#!/bin/python3

import requests
import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--token", help="Zoom API token (JWE)", required=True)
parser.add_argument("-r", "--roomid", help="Zoom room id", required=False)
parser.add_argument("-d", "--deviceid", help="Zoom room device id", required=False)
args = parser.parse_args()

url = "https://api.zoom.us"
token = args.token

headers = {
    'authorization': "Bearer " + token,
    'content-type': "application/json"
    }

data = requests.get(url + '/v2/rooms', headers=headers)
rooms = [(room['room_id'], room['name']) for room in data.json()['rooms']]

if args.deviceid and args.roomid:
    data = requests.get(url + '/v2/rooms/' + args.roomid[3:] + '/devices', headers=headers)
    devices = data.json()['devices']
    data_dic = {}
    for x in devices:
        data_dic[x['id']] = {'ROOM_NAME': x['room_name'], 'DEVICETYPE': x['device_type'],
                             'APP_VERSION': x['app_version'], 'SYSTEM': x['device_system'],
                             'STATUS': x['status']}
    print(json.dumps(data_dic[args.deviceid[3:]]))
else:
    result = '{"data":  [\n'
    for room in rooms:
        data = requests.get(url + '/v2/rooms/' + room[0] + '/devices', headers=headers)
        devices = data.json()['devices']
        for device in devices:
            # Add "aaa" in ID for zabbix external check
            # ID with "-" at the beginning are incorrectly passed to the script
            result += ' { "{#ROOMID}": "' + 'aaa' + room[0] + '", "{#ROOMNAME}": "' + room[1] + '", "{#DEVICE_ID}": "' +\
                      'aaa' + device['id'] + \
                      '", "{#DEVICE_SYSTEM}": "' + device['device_system'] + '"},\n'
    result = result[:-2] + '\n]}'
    print(result)
