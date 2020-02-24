import datetime
import functools
import json
import time
import urllib.request

import constants


def getInfoAboutSolvedTasksWithHandle(handle):
    try:
        request_url = 'http://codeforces.com/api/user.status?handle=' + handle
        response = urllib.request.urlopen(request_url)
        res = json.loads(response.read())
    except Exception:
        return {"Error": "can not get info from cf"}
    if 'result' not in res:
        return {"Error": "can not find result in json"}
    solved_tasks = {}
    for task in res['result']:
        if 'contestId' not in task:
            continue
        contest_id = task['contestId']
        if 'problem' not in task:
            continue
        if 'name' not in task['problem']:
            continue
        if 'rating' not in task['problem']:
            continue
        if 'tags' in task['problem'] and '*special' in task['problem']['tags']:
            continue
        rating = task['problem']['rating']
        task_name = task['problem']['name']
        if task['verdict'] == 'OK':
            if contest_id < 10000:
                if rating not in solved_tasks:
                    solved_tasks[rating] = {}
                if task_name not in solved_tasks[rating]:
                    solved_tasks[rating][task_name] = 0
                if task['creationTimeSeconds'] > solved_tasks[rating][task_name]:
                    solved_tasks[rating][task_name] = task['creationTimeSeconds']
    return solved_tasks


def findCodeforcesPoints(handle):
    ans = getInfoAboutSolvedTasksWithHandle(handle)
    res = 0
    for i in ans:
        d = min(len(ans[i]), 100)
        res += ((i / 100) - 4) * (100 * 101 / 2 - (100 - d) * (100 - d + 1) / 2) / 100
    return int(res)


def getVkIdFromCodeforces(handle):
    request_url = 'http://codeforces.com/api/user.info?handles=' + handle
    response = urllib.request.urlopen(request_url)
    res = json.loads(response.read())
    return res['result'][0]['vkId']


def getTimeOfLastSubmissionWithHandle(handle):
    info = getInfoAboutSolvedTasksWithHandle(handle)
    if 'Error' in info:
        return 0
    last_sub = 0
    for rating in info:
        for task in info[rating]:
            if info[rating][task] > last_sub:
                last_sub = info[rating][task]
    return last_sub


def getUnsolvedTasksWithHandle(handle):
    all_tasks = getInfoAboutSolvedTasksWithHandle('ruban')
    if 'Error' in all_tasks:
        return {}
    solved_tasks = getInfoAboutSolvedTasksWithHandle(handle)
    if 'Error' in solved_tasks:
        return {}
    for rating in solved_tasks:
        for name in solved_tasks[rating]:
            if name in all_tasks[rating]:
                all_tasks[rating].pop(name)
                if len(all_tasks[rating]) == 0:
                    all_tasks.pop(rating)
    return all_tasks
