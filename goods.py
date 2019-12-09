from pprint import pprint
import urllib.request
import json
import datetime
import time
import functools

import constant
import cf_api
import table

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

def resetAllDivTwoBets():
    data = {}
    data['range'] = 'D4:D200'
    data['majorDimension'] = 'ROWS'
    data['values'] = []
    for i in range(100):
        data['values'].append([''])
    buv = {}
    buv['value_input_option'] = 'USER_ENTERED'
    buv['data'] = data

    constant.service.spreadsheets().values().batchUpdate(
        spreadsheetId=constant.os_goods_sh_id,
        body=buv
    ).execute()

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
            print(values)
            setAllDivTwoBets(values)
            return 0
        if value[0] == handle:
            is_find = True
    values.append([handle])
    values.append([str(bet)])
    setAllDivTwoBets(values)
    return 0

def tryToCancelDivTwoBet(handle):
    values = getAllDivTwoBets()
    for i in range(0, len(values)):
        if values[i][0] == handle:
            table.afterSuccseccCanselingDiwTo(values[i][0], values[i + 1][0])
            values.pop(i + 1)
            values.pop(i)
            resetAllDivTwoBets()
            setAllDivTwoBets(values)
            break

# resetAllDivTwoBets()
# tryToCancelDivTwoBet('nongi')