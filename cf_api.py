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
        if 'index' not in task['problem']:
            continue
        index = task['problem']['index']
        rating = task['problem']['rating']
        task_name = task['problem']['name']
        if task['verdict'] == 'OK':
            if contest_id < 10000:
                if rating not in solved_tasks:
                    solved_tasks[rating] = {}
                if task_name not in solved_tasks[rating]:
                    solved_tasks[rating][task_name] = {'creationTimeSeconds': task['creationTimeSeconds'],
                                                       'contestId': contest_id, 'index': index}
                if task['creationTimeSeconds'] > solved_tasks[rating][task_name]['creationTimeSeconds']:
                    solved_tasks[rating][task_name]['creationTimeSeconds'] = task['creationTimeSeconds']
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
            if info[rating][task]['creationTimeSeconds'] > last_sub:
                last_sub = info[rating][task]['creationTimeSeconds']
    return last_sub


def getAllUnsolvedTasks():
    return getInfoAboutSolvedTasksWithHandle('ruban')


def getUnsolvedTasksWithHandle(handle):
    all_tasks = getInfoAboutSolvedTasksWithHandle('ruban')
    return getUnsolvedTasksWithHandleAndTasks(handle, all_tasks)


def getUnsolvedTasksWithHandleAndTasks(handle, all_tasks):
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


def getSetOfHundredTasks(handle, count, max_rating):
    unsolved_tasks = getUnsolvedTasksWithHandle(handle)
    res = []
    current_rating = 500
    while len(res) < count and current_rating < min(max_rating, 2501):
        if current_rating not in unsolved_tasks or not isStillRelevant(handle, current_rating):
            current_rating = current_rating + 100
            continue
        count_of_section = (max_rating - current_rating + 100) / 100
        missing_tasks = count - len(res)
        needed_from_here = (missing_tasks + count_of_section - 1) / count_of_section
        i = 0
        for task in unsolved_tasks[current_rating]:
            tmp = {"rating": current_rating,
                   'contestId': unsolved_tasks[current_rating][task]['contestId'],
                   'index': unsolved_tasks[current_rating][task]['index']}
            res.append(tmp)
            i = i + 1
            if i == needed_from_here or len(res) == count:
                break
        current_rating = current_rating + 100
    return res


def isStillRelevant(handle, rating):
    solved_tasks = getInfoAboutSolvedTasksWithHandle(handle)
    return len(solved_tasks[rating]) < 100
