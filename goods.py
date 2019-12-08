from pprint import pprint

import urllib.request
import httplib2
import apiclient.discovery
import json
import datetime
import time
import functools
from oauth2client.service_account import ServiceAccountCredentials

import constant
import cf_api


CREDENTIALS_FILE = 'creds.json'
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    ['https://www.googleapis.com/auth/spreadsheets',
     'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http = httpAuth)

def getAllDivTwoBets():
    values = service.spreadsheets().values().get(
        spreadsheetId=constant.os_goods_sh_id,
        range='D4:D200',
        majorDimension='ROWS'
    ).execute()
    if 'values' not in values:
        return []
    else:
        return values['values']

def setAllDivTwoBets(values):
    data = {}
    data['range'] = 'D4:D200'
    data['majorDimension'] = 'ROWS'
    data['values'] = values
    buv = {}
    buv['value_input_option'] = 'USER_ENTERED'
    buv['data'] = data

    service.spreadsheets().values().batchUpdate(
        spreadsheetId=constant.os_goods_sh_id,
        body=buv
    ).execute()

def tryToAddDivTwoBet(handle, bet):
    values = getAllDivTwoBets()
    is_find = False
    for value in values:
        if is_find:
            value[0] = str(int(value[0]) + int(bet))
            setAllDivTwoBets(values)
            return 0
        if value[0] == handle:
            is_find = True
    values.append([handle])
    values.append([str(bet)])
    setAllDivTwoBets(values)

    return 0

# print(tryToAddDivTwoBet('dnongi', 5))