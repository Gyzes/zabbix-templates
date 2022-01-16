#!/bin/python3

from bs4 import BeautifulSoup
import requests
import argparse
import re
from pysnmp.hlapi import *

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--pageid", help="Confluence page id", required=True)
parser.add_argument("-u", "--username", help="Confluence username", required=True)
parser.add_argument("-p", "--password", help="Confluence password", required=True)
parser.add_argument("-c", "--url", help="Confluence URL", required=True)
args = parser.parse_args()

contentApiUrl = '/rest/api/content'
confluenceBaseUrl = args.url
pageId = args.pageid
username = args.username
password = args.password

requestUrl = '{confluenceBaseUrl}{contentApiUrl}/{pageId}?expand=body.storage'.format(confluenceBaseUrl=confluenceBaseUrl,
                                                                                      contentApiUrl=contentApiUrl,
                                                                                      pageId=pageId)
requestResponse = requests.get(requestUrl, auth=(username, password))

html = requestResponse.json()['body']['storage']['value']
soup = BeautifulSoup(html, 'html.parser')

rows = soup.find_all('tr')

result = '{"data":  [\n'
for i in range(1, len(rows[1::])+1):
    try:
        cells = rows[i].find_all('td')
        if re.match(r'[A-Z]{3}-PRN\d{2}', cells[-1].get_text()):
            errorIndication, errorStatus, errorIndex, varBinds = next(getCmd(SnmpEngine(),
                                                                      CommunityData('public'),
                                                                      UdpTransportTarget((cells[-1].get_text(), 161)),
                                                                      ContextData(),
                                                                      ObjectType(ObjectIdentity('1.3.6.1.2.1.1.5.0')),
                                                                      lookupMib=False,
                                                                      lexicographicMode=False))
            if varBinds[0][1]:
                result += ' { "{#HOST}": "' + cells[-1].get_text() + '", "{#NAME}": "' + varBinds[0][1] + '"},\n'
    except:
        pass
result = result[:-2] + '\n]}'
print(result)
