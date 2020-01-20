from pprint import pprint
import urllib.request
import json
import datetime
import time
import functools

import constants
import secret_constants
import cf_api

def getAllUsersInfo():
    values = secret_constants.service.spreadsheets().values().get(
        spreadsheetId=secret_constants.spreadsheet_id,
        range='A2:F200',
        majorDimension='ROWS'
    ).execute()
    return values['values']

def setAllUsersInfo(values):
    data = {}
    data['range'] = 'A2:F200'
    data['majorDimension'] = 'ROWS'
    data['values'] = sorted(values, key=lambda value: int(value[TABLE_COLUMN_ALL_POINTS_]), reverse=True)
    buv = {}
    buv['value_input_option'] = 'USER_ENTERED'
    buv['data'] = data

    secret_constants.service.spreadsheets().values().batchUpdate(
        spreadsheetId=secret_constants.spreadsheet_id,
        body=buv
    ).execute()

def getPointsWithHandle(handle):
    values = getAllUsersInfo()
    for value in values:
        if value[TABLE_COLUMN_HANDLE_] == handle:
            return value[TABLE_COLUMN_ALL_POINTS_]
    return -1

def getPointsWithVkId(vkId):
    values = getAllUsersInfo()
    for value in values:
        if str(value[TABLE_COLUMN_VKID_]) == str(vkId):
            return int(value[TABLE_COLUMN_ALL_POINTS_])
    return -1

def setSpentPointsWithVkId(vkId, points):
    values = getAllUsersInfo()
    for value in values:
        if str(value[TABLE_COLUMN_VKID_]) == str(vkId):
            value[TABLE_COLUMN_SPENT_POINTS_] = str(int(value[TABLE_COLUMN_SPENT_POINTS_]) + int(points))
            value[TABLE_COLUMN_ALL_POINTS_] = str(int(value[TABLE_COLUMN_CF_POINTS_]) +
                                                  int(value[TABLE_COLUMN_ADDITIONAL_POINTS_]) -
                                                  int(value[TABLE_COLUMN_SPENT_POINTS_]))
            setAllUsersInfo(values)
            break

def resetPointsWithVkId(vkId):
    values = getAllUsersInfo()
    for value in values:
        if str(value[TABLE_COLUMN_VKID_]) == str(vkId):
            value[TABLE_COLUMN_CF_POINTS_] = cf_api.findCodeforcesPoints(value[TABLE_COLUMN_HANDLE_])
            value[TABLE_COLUMN_ALL_POINTS_] = str(int(value[TABLE_COLUMN_CF_POINTS_]) +
                                                  int(value[TABLE_COLUMN_ADDITIONAL_POINTS_]) -
                                                  int(value[TABLE_COLUMN_SPENT_POINTS_]))
            setAllUsersInfo(values)
            break

def isEnoughtForBet(vkId, bet):
    values = getAllUsersInfo()
    for value in values:
        if str(value[TABLE_COLUMN_VKID_]) == str(vkId):
            return int(bet) >= 10 and int(value[TABLE_COLUMN_ALL_POINTS_]) >= int(bet)
    return 0

def getHandleWithVkId(vkId):
    values = getAllUsersInfo()
    for value in values:
        if str(value[TABLE_COLUMN_VKID_]) == str(vkId):
            return value[TABLE_COLUMN_HANDLE_]
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
    tmp.append(str(0))
    values.append(tmp)
    setAllUsersInfo(values)

def getHandles():
    values = secret_constants.service.spreadsheets().values().get(
        spreadsheetId=secret_constants.spreadsheet_id,
        range='A2:A200',
        majorDimension='COLUMNS'
    ).execute()
    return values['values'][TABLE_COLUMN_HANDLE_]

def changeHeader():
    data = {}
    data['range'] = 'A1:F1'
    data['majorDimension'] = 'Columns'
    data['values'] = [['Ники на codeforces'], ['vkId'], ['Общее количество баллов'], ['Очки с кодфорса'],
                      ['Дополнительные баллы'], ['Потраченные баллы']]
    buv = {}
    buv['value_input_option'] = 'USER_ENTERED'
    buv['data'] = data
    secret_constants.service.spreadsheets().values().batchUpdate(
        spreadsheetId=secret_constants.spreadsheet_id,
        body=buv
    ).execute()

def afterSuccseccCanselingDivTo(handle, sp):
    values = getAllUsersInfo()
    for value in values:
        if value[TABLE_COLUMN_HANDLE_] == handle:
            value[TABLE_COLUMN_SPENT_POINTS_] = str(int(value[TABLE_COLUMN_SPENT_POINTS_]) - int(sp))
            value[TABLE_COLUMN_ALL_POINTS_] = str(int(value[TABLE_COLUMN_CF_POINTS_]) +
                                                  int(value[TABLE_COLUMN_ADDITIONAL_POINTS_]) -
                                                  int(value[TABLE_COLUMN_SPENT_POINTS_]))
            setAllUsersInfo(values)
            break

def resetAllUsersInfo():
    values = getAllUsersInfo()
    for value in values:
        value[TABLE_COLUMN_CF_POINTS_] = cf_api.findCodeforcesPoints(value[TABLE_COLUMN_HANDLE_])
        value[TABLE_COLUMN_ALL_POINTS_] = str(int(value[TABLE_COLUMN_CF_POINTS_]) +
                                              int(value[TABLE_COLUMN_ADDITIONAL_POINTS_]) -
                                              int(value[TABLE_COLUMN_SPENT_POINTS_]))
    setAllUsersInfo(values)
