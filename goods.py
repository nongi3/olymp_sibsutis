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

def getAllDivOneBets():
    values = secret_constants.service.spreadsheets().values().get(
        spreadsheetId=secret_constants.os_goods_sh_id,
        range='B4:B200',
        majorDimension='ROWS'
    ).execute()
    if 'values' not in values:
        return []
    else:
        return values['values']

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

def getAllDivThreeBets():
    values = secret_constants.service.spreadsheets().values().get(
        spreadsheetId=secret_constants.os_goods_sh_id,
        range='D4:D200',
        majorDimension='ROWS'
    ).execute()
    if 'values' not in values:
        return []
    else:
        return values['values']

def getAllLectureBets():
    values = secret_constants.service.spreadsheets().values().get(
        spreadsheetId=secret_constants.os_goods_sh_id,
        range='E4:E200',
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

def setAllDivOneBets(values):
    data = {}
    data['range'] = 'B4:B200'
    data['majorDimension'] = 'ROWS'
    data['values'] = values
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

def setAllDivThreeBets(values):
    data = {}
    data['range'] = 'D4:D200'
    data['majorDimension'] = 'ROWS'
    data['values'] = values
    buv = {}
    buv['value_input_option'] = 'USER_ENTERED'
    buv['data'] = data

    secret_constants.service.spreadsheets().values().batchUpdate(
        spreadsheetId=secret_constants.os_goods_sh_id,
        body=buv
    ).execute()

def setAllLectureBets(values):
    data = {}
    data['range'] = 'E4:E200'
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
    values = getAllDivOneBets()
    for value in values:
        if value[0] == handle:
            return False
    values.append([handle])
    values.append([str(bet)])
    setAllDivOneBets(values)
    setSumOfDivOneBets(bet * len(values) / 2)
    return True

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
    values = getAllDivThreeBets()
    for value in values:
        if value[0] == handle:
            return False
    values.append([handle])
    values.append([str(bet)])
    setAllDivThreeBets(values)
    setSumOfDivThreeBets(bet * len(values) / 2)
    return True

def tryToAddLectureBet(handle, bet):
    values = getAllLectureBets()
    for value in values:
        if value[0] == handle:
            return False
    values.append([handle])
    values.append([str(bet)])
    setAllLectureBets(values)
    setSumOfLectureBets(bet * len(values) / 2)
    return True

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

def getSumOfBets(lot_name):
    if lot_name in constants.DIV_ONE_:
        return getSumOfDivOneBets()
    elif lot_name in constants.DIV_TWO_:
        return getSumOfDivTwoBets()
    elif lot_name in constants.DIV_THREE_:
        return getSumOfDivThreeBets()
    elif lot_name in constants.LECTURE_WORDS_:
        return getSumOfLectureBets()
    else:
        return -1

def getSumOfDivOneBets():
    values = secret_constants.service.spreadsheets().values().get(
        spreadsheetId=secret_constants.os_goods_sh_id,
        range='B3:B3',
        majorDimension='ROWS'
    ).execute()
    if 'values' in values and len(values['values']) > 0 and len(values['values'][0]) > 0:
        return int(values['values'][0][0])
    else:
        return 0

def setSumOfDivOneBets(new_sum):
    data = {}
    data['range'] = 'B3:B3'
    data['majorDimension'] = 'ROWS'
    data['values'] = [[new_sum]]
    buv = {}
    buv['value_input_option'] = 'USER_ENTERED'
    buv['data'] = data
    secret_constants.service.spreadsheets().values().batchUpdate(
        spreadsheetId=secret_constants.os_goods_sh_id,
        body=buv
    ).execute()

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

def getSumOfDivThreeBets():
    values = secret_constants.service.spreadsheets().values().get(
        spreadsheetId=secret_constants.os_goods_sh_id,
        range='D3:D3',
        majorDimension='ROWS'
    ).execute()
    if 'values' in values and len(values['values']) > 0 and len(values['values'][0]) > 0:
        return int(values['values'][0][0])
    else:
        return 0

def getSumOfLectureBets():
    values = secret_constants.service.spreadsheets().values().get(
        spreadsheetId=secret_constants.os_goods_sh_id,
        range='E3:E3',
        majorDimension='ROWS'
    ).execute()
    if 'values' in values and len(values['values']) > 0 and len(values['values'][0]) > 0:
        return int(values['values'][0][0])
    else:
        return 0

def setSumOfDivThreeBets(new_sum):
    data = {}
    data['range'] = 'D3:D3'
    data['majorDimension'] = 'ROWS'
    data['values'] = [[new_sum]]
    buv = {}
    buv['value_input_option'] = 'USER_ENTERED'
    buv['data'] = data
    secret_constants.service.spreadsheets().values().batchUpdate(
        spreadsheetId=secret_constants.os_goods_sh_id,
        body=buv
    ).execute()

def setSumOfLectureBets(new_sum):
    data = {}
    data['range'] = 'E3:E3'
    data['majorDimension'] = 'ROWS'
    data['values'] = [[new_sum]]
    buv = {}
    buv['value_input_option'] = 'USER_ENTERED'
    buv['data'] = data
    secret_constants.service.spreadsheets().values().batchUpdate(
        spreadsheetId=secret_constants.os_goods_sh_id,
        body=buv
    ).execute()

def getDivOneCost():
    values = secret_constants.service.spreadsheets().values().get(
        spreadsheetId=secret_constants.os_goods_sh_id,
        range='B2:B2',
        majorDimension='ROWS'
    ).execute()
    if 'values' in values and len(values['values']) > 0 and len(values['values'][0]) > 0:
        return values['values'][0][0]
    else:
        return -1

def getDivTwoCost():
    values = secret_constants.service.spreadsheets().values().get(
        spreadsheetId=secret_constants.os_goods_sh_id,
        range='C2:C2',
        majorDimension='ROWS'
    ).execute()
    if 'values' in values and len(values['values']) > 0 and len(values['values'][0]) > 0:
        return values['values'][0][0]
    else:
        return -1

def getDivThreeCost():
    values = secret_constants.service.spreadsheets().values().get(
        spreadsheetId=secret_constants.os_goods_sh_id,
        range='D2:D2',
        majorDimension='ROWS'
    ).execute()
    if 'values' in values and len(values['values']) > 0 and len(values['values'][0]) > 0:
        return values['values'][0][0]
    else:
        return -1

def getLectureCost():
    values = secret_constants.service.spreadsheets().values().get(
        spreadsheetId=secret_constants.os_goods_sh_id,
        range='E2:E2',
        majorDimension='ROWS'
    ).execute()
    if 'values' in values and len(values['values']) > 0 and len(values['values'][0]) > 0:
        return values['values'][0][0]
    else:
        return -1

def getDivTwoParty():
    values = getAllDivTwoBets()
    res = []
    for i in range(0, len(values)):
        if i % 2 == 0:
            res.append(values[i][0])
    return res

def getPrice(lot_name):
    if lot_name in constants.DIV_ONE_:
        return getDivOneCost()
    elif lot_name in constants.DIV_TWO_:
        return getDivTwoCost()
    elif lot_name in constants.DIV_THREE_:
        return getDivThreeCost()
    elif lot_name in constants.LECTURE_WORDS_:
        return getLectureCost()
    else:
        return -1