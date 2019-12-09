from pprint import pprint
import urllib.request
import json
import datetime
import time
import functools

import constant
import cf_api

def getAllDivTwoBets():
    values = constant.service.spreadsheets().values().get(
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

    constant.service.spreadsheets().values().batchUpdate(
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