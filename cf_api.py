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

handles_ = []

def cmp(a, b):
    if a[0] < b[0]:
        return -1
    elif a[0] > b[0]:
        return 1
    else:
        return 0


# Авторизуемся и получаем service — экземпляр доступа к API
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    ['https://www.googleapis.com/auth/spreadsheets',
     'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http = httpAuth)

def get_handles():
    values = service.spreadsheets().values().get(
        spreadsheetId=constant.spreadsheet_id,
        range='A2:A200',
        majorDimension='COLUMNS'
    ).execute()
    global handles_
    handles_ = values['values'][0]

def add_new_handle(new_handle):
    get_handles()
    global handles_
    if new_handle not in handles_:
        handles_.append(new_handle)
        changeCodeforcesInfo()


def findCodeforcesPoints(handle):
    request_url = 'http://codeforces.com/api/user.status?handle=' + handle
    response = urllib.request.urlopen(request_url)
    time.sleep(1)
    res = json.loads(response.read())
    ans = {}
    for i in res['result']:
        if 'contestId' not in i:
            continue
        contestId = i['contestId']
        if 'problem' not in i:
            continue
        if 'rating' not in i['problem']:
            continue
        rating = i['problem']['rating']
        ct = datetime.datetime.now()
        unixtime = time.mktime(ct.timetuple())
        tm = unixtime - i['creationTimeSeconds']
        contest_name = i['problem']['name']
        if i['verdict'] == 'OK':
            if contestId < 10000:
                if rating not in ans:
                    ans[rating] = 1
                else:
                    ans[rating] = ans[rating] + 1
    res = 0
    for i in ans:
        d = min(ans[i], 100)
        res += ((i / 100) - 4) * (100 * 101 / 2 - (100 - d) * (100 - d + 1) / 2) / 100
    # print(handle)
    return int(res)

def getVkIdFromCodeforces(handle):
    request_url = 'http://codeforces.com/api/user.info?handles=' + handle
    response = urllib.request.urlopen(request_url)
    res = json.loads(response.read())
    return res['result'][0]['vkId']

def changeHeader():
    data = {}
    data['range'] = 'A1:F1'
    data['majorDimension'] = 'Columns'
    data['values'] = [['Ники на codeforces'], ['vkId'], ['Общее количество баллов'], ['Очки с кодфорса'],
                      ['Дополнительные баллы'], ['Потраченные баллы']]
    buv = {}
    buv['value_input_option'] = 'USER_ENTERED'
    buv['data'] = data
    service.spreadsheets().values().batchUpdate(
        spreadsheetId=constant.spreadsheet_id,
        body=buv
    ).execute()

def getUserInfoWithHandle(handle):
    request_url = 'http://codeforces.com/api/user.status?handle=' + handle
    response = urllib.request.urlopen(request_url)
    res = json.loads(response.read())
    ans = {}
    for i in res['result']:
        if 'contestId' not in i:
            continue
        contestId = i['contestId']
        if 'problem' not in i:
            continue
        if 'rating' not in i['problem']:
            continue
        rating = i['problem']['rating']
        if i['verdict'] == 'OK':
            if contestId < 10000:
                if rating not in ans:
                    ans[rating] = 1
                else:
                    ans[rating] = ans[rating] + 1
    res = 0
    for i in ans:
        d = min(ans[i], 100)
        res += ((i / 100) - 4) * (100 * 101 / 2 - (100 - d) * (100 - d + 1) / 2) / 100
    tmp = []
    tmp.append(handle)
    tmp.append(getVkIdFromCodeforces(handle))
    tmp.append(str(int(res)))
    tmp.append(str(int(res)))
    tmp.append(str(0))
    return tmp

# changeHeader()
# changeCodeforcesInfo()
# get_handles()
# add_new_handle('nongi')
