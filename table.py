# coding=utf-8
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
        range='A2:C200',
        majorDimension='ROWS'
    ).execute()
    return values['values']


def setAllUsersInfo(values):
    data = {'range': 'A2:C200', 'majorDimension': 'ROWS',
            'values': sorted(values, key=lambda value: int(value[constants.TABLE_COLUMN_CF_POINTS_]), reverse=True)}
    buv = {'value_input_option': 'USER_ENTERED', 'data': data}

    secret_constants.service.spreadsheets().values().batchUpdate(
        spreadsheetId=secret_constants.spreadsheet_id,
        body=buv
    ).execute()


def getPointsWithHandle(handle):
    values = getAllUsersInfo()
    for value in values:
        if value[constants.TABLE_COLUMN_HANDLE_] == handle:
            return value[constants.TABLE_COLUMN_CF_POINTS_]
    return -1


def getPointsWithVkId(vk_id):
    values = getAllUsersInfo()
    for value in values:
        if str(value[constants.TABLE_COLUMN_VK_ID_]) == str(vk_id):
            return int(value[constants.TABLE_COLUMN_CF_POINTS_])
    return -1


def resetPointsWithVkId(vk_id):
    values = getAllUsersInfo()
    for value in values:
        if str(value[constants.TABLE_COLUMN_VK_ID_]) == str(vk_id):
            value[constants.TABLE_COLUMN_CF_POINTS_] = cf_api.findCodeforcesPoints(value[constants.TABLE_COLUMN_HANDLE_])
            setAllUsersInfo(values)
            return True
    return False


def getHandleWithVkId(vk_id):
    values = getAllUsersInfo()
    for value in values:
        if str(value[constants.TABLE_COLUMN_VK_ID_]) == str(vk_id):
            return value[constants.TABLE_COLUMN_HANDLE_]
    return "None"


def addNewUser(handle, vk_id):
    values = getAllUsersInfo()
    tmp = [handle, vk_id, cf_api.findCodeforcesPoints(handle)]
    values.append(tmp)
    setAllUsersInfo(values)


def getHandles():
    values = secret_constants.service.spreadsheets().values().get(
        spreadsheetId=secret_constants.spreadsheet_id,
        range='A2:A200',
        majorDimension='COLUMNS'
    ).execute()
    return values['values'][constants.TABLE_COLUMN_HANDLE_]


def changeHeader():
    data = {'range': 'A1:С1', 'majorDimension': 'Columns',
            'values': [['Ники на codeforces'], ['vk_id'], ['Очки архива']]}
    buv = {'value_input_option': 'USER_ENTERED', 'data': data}
    secret_constants.service.spreadsheets().values().batchUpdate(
        spreadsheetId=secret_constants.spreadsheet_id,
        body=buv
    ).execute()


def resetAllUsersInfo():
    values = getAllUsersInfo()
    for value in values:
        value[constants.TABLE_COLUMN_CF_POINTS_] = cf_api.findCodeforcesPoints(value[constants.TABLE_COLUMN_HANDLE_])
    setAllUsersInfo(values)


def isUserAlreadyExist(vk_id):
    values = getAllUsersInfo()
    for value in values:
        if str(value[constants.TABLE_COLUMN_VK_ID_]) == str(vk_id):
            return True
    return False


def getPositionWithVkId(vk_id):
    values = getAllUsersInfo()
    pos = 0
    for value in values:
        pos = pos + 1
        if str(vk_id) == str(value[constants.TABLE_COLUMN_VK_ID_]):
            return pos
    return -1


def getLeaders():
    values = getAllUsersInfo()
    res = []
    ind = 0
    for value in values:
        ind = ind + 1
        if ind > 10:
            break
        res.append(value)
    return res
