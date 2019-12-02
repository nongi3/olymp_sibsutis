from pprint import pprint

import urllib.request
import httplib2
import apiclient.discovery
import json
import datetime
import time
import functools
from oauth2client.service_account import ServiceAccountCredentials


CREDENTIALS_FILE = 'creds.json'
# ID Google Sheets документа (можно взять из его URL)
spreadsheet_id = '1gJYZf7wQE0ReIgR8idpZnqqgSPKQmlkQtnaO3XwGcJI'


handles = [
"nongi",
"UWPLP",
"kcherdakov",
"Qalmee",
"genybr",
"Mazx1998",
"stMark",
"Thundbird",
"bedsus",
"Allen_Mett",
"Shadow-of-Dreams",
"Levcor",
"andrew_raiden",
"niloniol",
"Mary12",
"Minddarkness",
"PowerOfBalls",
"Alecks",
"Tornem",
"ikrisi",
"RushBush",
"fkz_12",
"Arishenk",
"Flanterz",
"Fonriter98",
"ruban",
"jeanstefanovich",
"Brandon_Roadgears_",
"Soul_Catcher",
"shise",
"Izeytee",
"wartemw",
"deluck",
"gedenteen",
"Marks53",
"Dream_Tea",
"Kagary",
"F14rk",
"JustBoss",
"Animeshka",
"Lampcomm",
"Nottey",
"alexger1999",
"Tod-cun",
"osipovcf",
"MikeAirone",
"Karina8941",
"Aleksey-Kn",
"Makisto",
"Asakujaku",
"Hostel_B",
"fredboy",
"aldinger_a",
"Restov",
"BarebuhPuh",
"virride",
"Hazzi",
"fancyFox",
"Sheshesi",
"Gadyka",
"Grawyn",
"Baburr",
"tryblyat7",
"MangriMen",
"_HiFive",
"QWOP1234",
"Daniil_hrpo",
"isugihere",
"sweetechka",
"El_Duderino",
"QualDiv2",]


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

# Пример чтения файла
values = service.spreadsheets().values().get(
    spreadsheetId=spreadsheet_id,
    range='A1:E10',
    majorDimension='COLUMNS'
).execute()

def findCodeforcesPoints(handle):
    request_url = 'http://codeforces.com/api/user.status?handle=' + handle
    response = urllib.request.urlopen(request_url)
    time.sleep(1)
    res = json.loads(response.read())
    ans = {}
    usedContestNames = {}
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
        res += ((i / 100) - 4) * ans[i]
    print(handle)
    return res

def myOwnSort(data):
    i = 0
    while i + 1 < len(data):
        j = 0
        while j + 1 < len(data) - i:
            if float(data[j][1]) < float(data[j + 1][1]):
                data[j], data[j + 1] = data[j + 1], data[j]
            j = j + 1
        i = i + 1
    return data

def changeCodeforcesInfo():
    ind = 1
    data = {}
    data['range'] = 'A2:D' + str(len(handles) + 1)
    data['majorDimension'] = 'ROWS'
    data['values'] = []
    for i in handles:
        tmp = []
        tmp.append(i)
        codeforces_points = findCodeforcesPoints(i)
        additional_points = 0
        tmp.append(str(codeforces_points + additional_points))
        tmp.append(str(codeforces_points))
        tmp.append(str(additional_points))
        data['values'].append(tmp);
    data['values'] = myOwnSort(data['values'])
    # data['values'] = sorted(data['values'], key=functools.cmp_to_key(cmp))

    buv = {}
    buv['value_input_option'] = 'USER_ENTERED'
    buv['data'] = data

    # print(buv)

    service.spreadsheets().values().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body=buv
    ).execute()

def changeHeader():
    data = {}
    data['range'] = 'A1:D1'
    data['majorDimension'] = 'Columns'
    data['values'] = [['Ники на codeforces'], ['Общее количество баллов'], ['Очки с кодфорса'], ['Дополнительные баллы']]
    buv = {}
    buv['value_input_option'] = 'USER_ENTERED'
    buv['data'] = data
    service.spreadsheets().values().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body=buv
    ).execute()

# changeHeader()
changeCodeforcesInfo()
