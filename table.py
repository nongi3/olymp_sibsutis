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
import cf_api


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

def setAllUsersInfo(values):
    data = {}
    data['range'] = 'A2:F200'
    data['majorDimension'] = 'ROWS'
    data['values'] = sorted(values, key=lambda value: int(value[2]), reverse=True)
    buv = {}
    buv['value_input_option'] = 'USER_ENTERED'
    buv['data'] = data

    service.spreadsheets().values().batchUpdate(
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

# getAllUsersInfo()

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


# TODO: удалить метод ниже к хуйам

def cmp(a, b):
	if len(a) == len(b):
		if a < b:
			return -1
		elif a > b:
			return 1
		else:
			return 0
	else:
		return len(a) - len(b)

def resetCfPoints():
    handles = [
        "aldinger_a",
        "Restov",
        "BarebuhPuh",
        "virride",
        "Hazzi",
        "fancyFox",
        "Hazzi",
        "Hazzi",
        "Hazzi",
        "Hazzi",
        "Hazzi",
        "Sheshesi",
        "Gadyka",
        "Grawyn",
        "Baburr",
        "tryblyat7",
        "MangriMen",
        "Hazzi",
        "_HiFive",
        "QWOP1234",
        "Daniil_hrpo",
        "isugihere",
        "sweetechka",
        "El_Duderino",
        "Hazzi",
        "Hazzi",
        "Hazzi",
        "QualDiv2", ]
    task_time = {}
    ans = {}

    for handle in handles:
        ans[handle] = 0
        if handle == 'Hazzi':
            continue
        request_url = 'http://codeforces.com/api/user.status?handle=' + handle
        response = urllib.request.urlopen(request_url)
        time.sleep(1)
        res = json.loads(response.read())
        for i in res['result']:
            if 'contestId' not in i:
                continue
            if 'problem' not in i:
                continue
            if 'rating' not in i['problem']:
                continue
            ct = datetime.datetime.now()
            unixtime = time.mktime(ct.timetuple())
            tm = unixtime - i['creationTimeSeconds']
            contest_name = str(i['problem']['contestId']) + i['problem']['index']
            if i['verdict'] == 'OK':
                if i['creationTimeSeconds'] >= 1571097600:
                    ans[handle] += 1
                    if contest_name not in task_time:
                        task_time[contest_name] = tm
                else:
                    task_time[contest_name] = tm
    task_time = sorted(task_time, key=functools.cmp_to_key(cmp))

    tmp = []
    for handle in handles:
        tm = []
        tm.append(ans[handle])
        tmp.append(tm)

    data = {}
    data['range'] = 'E2:E29'
    data['majorDimension'] = 'ROWS'
    data['values'] = tmp
    buv = {}
    buv['value_input_option'] = 'USER_ENTERED'
    buv['data'] = data

    sh_id = '1YMEzW5M8vwipcn-vJFoPKZsBtAPoli-woSIC9SS58i4'
    service.spreadsheets().values().batchUpdate(
        spreadsheetId=sh_id,
        body=buv
    ).execute()