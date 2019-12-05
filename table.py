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


CREDENTIALS_FILE = 'creds.json'
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    ['https://www.googleapis.com/auth/spreadsheets',
     'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http = httpAuth)

def getAllUsersInfo():
    values = service.spreadsheets().values().get(
        spreadsheetId=constant.spreadsheet_id,
        range='A2:F200',
        majorDimension='ROWS'
    ).execute()
    return values['values']

def getPointsWithHandle(handle):
    values = getAllUsersInfo()
    for value in values:
        if value[0] == handle:
            return value[2]
    return -1

def getPointsWithVkId(vkId):
    values = getAllUsersInfo()
    for value in values:
        if value[1] == vkId:
            return value[2]
    return -1

getAllUsersInfo()