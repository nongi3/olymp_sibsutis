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
        range='A2:E200',
        majorDimension='ROWS'
    ).execute()
    return values['values']


def setAllUsersInfo(values):
    data = {'range': 'A2:E200', 'majorDimension': 'ROWS',
            'values': sorted(values, key=lambda value: int(value[constants.TABLE_COLUMN_PROBLEMSET_]), reverse=True)}
    buv = {'value_input_option': 'USER_ENTERED', 'data': data}

    secret_constants.service.spreadsheets().values().batchUpdate(
        spreadsheetId=secret_constants.spreadsheet_id,
        body=buv
    ).execute()


def getPointsWithHandle(handle):
    values = getAllUsersInfo()
    for value in values:
        if value[constants.TABLE_COLUMN_HANDLE_] == handle:
            return value[constants.TABLE_COLUMN_PROBLEMSET_]
    return -1


def getPointsWithVkId(vk_id):
    values = getAllUsersInfo()
    for value in values:
        if str(value[constants.TABLE_COLUMN_VK_ID_]) == str(vk_id):
            return int(value[constants.TABLE_COLUMN_PROBLEMSET_])
    return -1


def resetPointsWithVkId(vk_id):
    values = getAllUsersInfo()
    for value in values:
        if str(value[constants.TABLE_COLUMN_VK_ID_]) == str(vk_id):
            points = cf_api.findCodeforcesPoints(value[constants.TABLE_COLUMN_HANDLE_])
            if points < 0:
                return False
            value[constants.TABLE_COLUMN_PROBLEMSET_] = points
            setAllUsersInfo(values)
            return True
    return False


def resetGymPointsWithVkId(vk_id):
    values = getAllUsersInfo()
    for value in values:
        if str(value[constants.TABLE_COLUMN_VK_ID_]) == str(vk_id):
            gym_points = cf_api.findGymPoints(value[constants.TABLE_COLUMN_HANDLE_])
            if gym_points == -1:
                return False
            value[constants.TABLE_COLUMN_GYMS_] = gym_points
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
    tmp = [handle, vk_id, cf_api.findCodeforcesPoints(handle), cf_api.findGymPoints(handle)]
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
    data = {'range': 'A1:D1', 'majorDimension': 'Columns',
            'values': [['Ники на codeforces'], ['vk_id'], ['Очки архива'], ['Очки тренировок']]}
    buv = {'value_input_option': 'USER_ENTERED', 'data': data}
    secret_constants.service.spreadsheets().values().batchUpdate(
        spreadsheetId=secret_constants.spreadsheet_id,
        body=buv
    ).execute()


def resetAllUsersInfo():
    values = getAllUsersInfo()
    for value in values:
        points = cf_api.findCodeforcesPoints(value[constants.TABLE_COLUMN_HANDLE_])
        if points > -1:
            value[constants.TABLE_COLUMN_PROBLEMSET_] = points
        gym_points = cf_api.findGymPoints(value[constants.TABLE_COLUMN_HANDLE_])
        if gym_points > -1:
            value[constants.TABLE_COLUMN_GYMS_] = gym_points
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


def tryToChangeName(new_name, vk_id):
    users = getAllUsersInfo()
    for user in users:
        if str(user[constants.TABLE_COLUMN_VK_ID_]) == str(vk_id):
            user[constants.TABLE_COLUMN_NAME_] = new_name
            setAllUsersInfo(users)
            return {}
    return {'Error': 'something go wrong'}
