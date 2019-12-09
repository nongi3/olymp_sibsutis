from pprint import pprint
import urllib.request
import json
import datetime
import time
import functools

import constant
import cf_api

def getAllUsersInfo():
    values = constant.service.spreadsheets().values().get(
        spreadsheetId=constant.spreadsheet_id,
        range='A2:F200',
        majorDimension='ROWS'
    ).execute()
    return values['values']

def setAllUsersInfo(values):
    data = {}
    data['range'] = 'A2:F200'
    data['majorDimension'] = 'ROWS'
    data['values'] = sorted(values, key=lambda value: int(value[2]), reverse=True)
    buv = {}
    buv['value_input_option'] = 'USER_ENTERED'
    buv['data'] = data

    constant.service.spreadsheets().values().batchUpdate(
        spreadsheetId=constant.spreadsheet_id,
        body=buv
    ).execute()

def getPointsWithHandle(handle):
    values = getAllUsersInfo()
    for value in values:
        if value[0] == handle:
            return value[2]
    return -1

def getPointsWithVkId(vkId):
    values = getAllUsersInfo()
    for value in values:
        if str(value[1]) == str(vkId):
            return int(value[2])
    return -1

def setSpentPointsWithVkId(vkId, points):
    values = getAllUsersInfo()
    for value in values:
        if str(value[1]) == str(vkId):
            value[5] = str(int(value[5]) + int(points))
            value[2] = str(int(value[3]) + int(value[4]) - int(value[5]))
            setAllUsersInfo(values)
            break

def resetPointsWithVkId(vkId):
    values = getAllUsersInfo()
    for value in values:
        if str(value[1]) == str(vkId):
            value = cf_api.getUserInfoWithHandle(value[0])
            print (cf_api.getUserInfoWithHandle(value[0]), value)
            setAllUsersInfo(values)
            break

def isEnoughtForBet(vkId, bet):
    values = getAllUsersInfo()
    for value in values:
        if str(value[1]) == str(vkId):
            return int(bet) >= 10 and int(value[2]) >= int(bet)
    return 0

def getHandleWithVkId(vkId):
    values = getAllUsersInfo()
    for value in values:
        if str(value[1]) == str(vkId):
            return value[0]
    return "None"

def addNewUser(handle, vkId):
    values = getAllUsersInfo()
    tmp = []
    tmp.append(handle)
    tmp.append(vkId)
    codeforces_points = cf_api.findCodeforcesPoints(handle)
    additional_points = 0
    tmp.append(str(codeforces_points + additional_points))
    tmp.append(str(codeforces_points))
    tmp.append(str(additional_points))
    tmp.append(str(0));
    values.append(tmp)
    setAllUsersInfo(values)