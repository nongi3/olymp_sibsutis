from pprint import pprint

import urllib.request
import json
import datetime
import time
import functools

import constants

handles_ = []

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

def getTimeOfLastSubmissionWithHandle(handle):
    try:
        request_url = 'http://codeforces.com/api/user.status?handle=' + handle
        response = urllib.request.urlopen(request_url)
        res = json.loads(response.read())
    except Exception:
        return 0
    if 'result' not in res:
        return 0
    for task in res['result']:
        if 'verdict' not in task:
            continue
        if task['verdict'] == 'OK':
            return task['creationTimeSeconds']
    return 0


