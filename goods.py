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

def tryToAddBet(handle, lot_name, bet):
    if lot_name in constants.DIV_ONE_:
        return tryToAddDivOneBet(handle, bet)
    elif lot_name in constants.DIV_TWO_:
        return tryToAddDivTwoBet(handle, bet)
    elif lot_name in constants.DIV_THREE_:
        return tryToAddDivThreeBet(handle, bet)
    elif lot_name in constants.LECTURE_WORDS_:
        return tryToAddLectureBet(handle, bet)
    else:
        return False

def tryToAddDivOneBet(handle, bet):
    return False

def tryToAddDivTwoBet(handle, bet):
    values = getAllDivTwoBets()
    for value in values:
        if value[0] == handle:
            return False
    values.append([handle])
    values.append([str(bet)])
    setAllDivTwoBets(values)
    setSumOfDivTwoBets(bet * len(values) / 2)
    return True

def tryToAddDivThreeBet(handle, bet):
    return False

def tryToAddLectureBet(handle, bet):
    return False

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
    values = secret_constants.service.spreadsheets().values().get(
        spreadsheetId=secret_constants.os_goods_sh_id,
        range='C3:C3',
        majorDimension='ROWS'
    ).execute()
    if 'values' in values and len(values['values']) > 0 and len(values['values'][0]) > 0:
        return int(values['values'][0][0])
    else:
        return 0

def setSumOfDivTwoBets(new_sum):
    data = {}
    data['range'] = 'C3:C3'
    data['majorDimension'] = 'ROWS'
    data['values'] = [[new_sum]]
    buv = {}
    buv['value_input_option'] = 'USER_ENTERED'
    buv['data'] = data
    secret_constants.service.spreadsheets().values().batchUpdate(
        spreadsheetId=secret_constants.os_goods_sh_id,
        body=buv
    ).execute()

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
