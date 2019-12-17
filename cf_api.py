from pprint import pprint

import urllib.request
import json
import datetime
import time
import functools

import constant

handles_ = []

def cmp(a, b):
    if a[0] < b[0]:
        return -1
    elif a[0] > b[0]:
        return 1
    else:
        return 0

def add_new_handle(new_handle):
    global handles_
    handles_ = table.getHandles()
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
    return int(res)

def getVkIdFromCodeforces(handle):
    request_url = 'http://codeforces.com/api/user.info?handles=' + handle
    response = urllib.request.urlopen(request_url)
    res = json.loads(response.read())
    return res['result'][0]['vkId']