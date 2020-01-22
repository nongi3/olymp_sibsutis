from pprint import pprint
import urllib.request
import json
import datetime
import time
import functools

import constants
import secret_constants
import cf_api
import table

def getAllDivTwoBets():
    values = secret_constants.service.spreadsheets().values().get(
        spreadsheetId=secret_constants.os_goods_sh_id,
        range='C4:C200',
        majorDimension='ROWS'
    ).execute()
    if 'values' not in values:
        return []
    else:
        return values['values']

def resetAllDivTwoBets():
    data = {}
    data['range'] = 'C4:C200'
    data['majorDimension'] = 'ROWS'
    data['values'] = []
    for i in range(100):
        data['values'].append([''])
    buv = {}
    buv['value_input_option'] = 'USER_ENTERED'
    buv['data'] = data

    secret_constants.service.spreadsheets().values().batchUpdate(
        spreadsheetId=secret_constants.os_goods_sh_id,
        body=buv
    ).execute()

def setAllDivTwoBets(values):
    data = {}
    data['range'] = 'C4:C200'
    data['majorDimension'] = 'ROWS'
    data['values'] = values
    buv = {}
    buv['value_input_option'] = 'USER_ENTERED'
    buv['data'] = data

    secret_constants.service.spreadsheets().values().batchUpdate(
        spreadsheetId=secret_constants.os_goods_sh_id,
        body=buv
    ).execute()

def tryToAddDivTwoBet(handle, bet):
    values = getAllDivTwoBets()
    is_find = False
    for value in values:
        if is_find:
            value[0] = bet
            setAllDivTwoBets(values)
            return
        if value[0] == handle:
            is_find = True
    values.append([handle])
    values.append([str(bet)])
    setAllDivTwoBets(values)

def tryToCancelDivTwoBet(handle):
    values = getAllDivTwoBets()
    for i in range(0, len(values)):
        if values[i][0] == handle:
            table.afterSuccseccCanselingDivTo(values[i][0], values[i + 1][0])
            values.pop(i + 1)
            values.pop(i)
            resetAllDivTwoBets()
            setAllDivTwoBets(values)
            break

def getSumOfDivTwoBets():
    return int(secret_constants.service.spreadsheets().values().get(
        spreadsheetId=secret_constants.os_goods_sh_id,
        range='C3:C3',
        majorDimension='ROWS'
    ).execute()['values'][0][0])

def getDivTwoCost():
    return int(secret_constants.service.spreadsheets().values().get(
        spreadsheetId=secret_constants.os_goods_sh_id,
        range='C2:C2',
        majorDimension='ROWS'
    ).execute()['values'][0][0])

def getDivTwoParty():
    values = getAllDivTwoBets()
    res = []
    for i in range(0, len(values)):
        if i % 2 == 0:
            res.append(values[i][0])
    return res
