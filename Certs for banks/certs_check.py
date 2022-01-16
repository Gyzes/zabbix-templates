#!/bin/python3

from bs4 import BeautifulSoup
import requests
import argparse
import json
from datetime import datetime

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--pageid", help="Confluence page id", required=True)
parser.add_argument("-u", "--username", help="Confluence username", required=True)
parser.add_argument("-p", "--password", help="Confluence password", required=True)
parser.add_argument("-c", "--url", help="Confluence URL", required=True)
parser.add_argument("-r", "--row", help="row in table", required=False)
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

if args.row:
    cells = rows[int(args.row)].find_all('td')
    result = {"FIO": cells[1].get_text(), "DATE": int(datetime.strptime(cells[2].get_text(), '%Y.%m.%d').timestamp()),
              "PHONE": cells[3].get_text()}
    print(json.dumps(result))
else:
    result = '{"data":  [\n'
    for i in range(1, len(rows[1::])+1):
        cells = rows[i].find_all('td')
        result += ' { "{#ROW}": "' + str(i) + '", "{#NAME}": "' + cells[0].get_text() + '"},\n'
    result = result[:-2] + '\n]}'
    print(result)
