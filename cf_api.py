import datetime
import functools
import json
import random
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
        if 'tags' in task['problem'] and '*special' in task['problem']['tags']:
            continue
        if 'index' not in task['problem']:
            continue
        index = task['problem']['index']
        if 'name' not in task['problem']:
            continue
        task_name = task['problem']['name']
        if 'verdict' not in task:
            continue
        if task['verdict'] == 'OK':
            if contest_id < 10000:
                if 'rating' not in task['problem']:
                    continue
                rating = int(task['problem']['rating'])
                if rating not in solved_tasks:
                    solved_tasks[rating] = {}
                if task_name not in solved_tasks[rating]:
                    solved_tasks[rating][task_name] = {'creationTimeSeconds': task['creationTimeSeconds'],
                                                       'contestId': contest_id, 'index': index}
                if task['creationTimeSeconds'] > solved_tasks[rating][task_name]['creationTimeSeconds']:
                    solved_tasks[rating][task_name]['creationTimeSeconds'] = task['creationTimeSeconds']
            else:
                if 0 not in solved_tasks:
                    solved_tasks[0] = {}
                solved_tasks[0][task_name] = {'creationTimeSeconds': task['creationTimeSeconds'],
                                              'contestId': contest_id, 'index': index}
    return solved_tasks


def findCodeforcesPoints(handle):
    ans = getInfoAboutSolvedTasksWithHandle(handle)
    if 'Error' in ans:
        return -1
    res = 0
    for rating in ans:
        if rating == 0:
            continue
        d = min(len(ans[rating]), 100)
        res += ((int(rating) / 100) - 4) * (100 * 101 / 2 - (100 - d) * (100 - d + 1) / 2) / 100
    return int(res)


def findGymPoints(handle):
    info = getInfoAboutSolvedTasksWithHandle(handle)
    if 'Error' in info:
        return -1
    if 0 not in info:
        return 0
    return len(info[0])


def getVkIdFromCodeforces(handle):
    try:
        request_url = 'http://codeforces.com/api/user.info?handles=' + handle
        response = urllib.request.urlopen(request_url)
        res = json.loads(response.read())
    except Exception:
        return 'Error'
    if res['status'] != 'OK':
        return 'Error'
    return str(res['result'][0]['vkId'])


def get_codeforces_rating(handle):
    try:
        request_url = 'http://codeforces.com/api/user.info?handles=' + handle
        response = urllib.request.urlopen(request_url)
        res = json.loads(response.read())
    except Exception:
        return 'Error'
    if 'status' not in res or res['status'] != 'OK' or 'result' not in res or 'rating' not in res['result'][0]:
        return 'Error'
    return res['result'][0]['rating']


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
            if rating in all_tasks and name in all_tasks[rating]:
                all_tasks[rating].pop(name)
                if len(all_tasks[rating]) == 0:
                    all_tasks.pop(rating)
    return all_tasks


def getSetOfHundredTasks(handle, count, max_rating):
    unsolved_tasks = getUnsolvedTasksWithHandle(handle)
    if unsolved_tasks == {}:
        return []
    res = []
    current_rating = 500
    while len(res) < count and current_rating < min(max_rating+1, 2501):
        if current_rating not in unsolved_tasks or not isStillRelevant(handle, current_rating):
            current_rating = current_rating + 100
            continue
        count_of_section = int((max_rating - current_rating + 100) / 100)
        missing_tasks = count - len(res)
        needed_from_here = int((missing_tasks + count_of_section - 1) / count_of_section)
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


def countOfTasksWithRating(handle, rating):
    solved_tasks = getInfoAboutSolvedTasksWithHandle(handle)
    if int(rating) not in solved_tasks:
        return 0
    return len(solved_tasks[int(rating)])


def countOfPointsForATaskWithRating(handle, rating):
    count_of_tasks = min(countOfTasksWithRating(handle, rating), 100)
    if rating % 100 != 0 or rating < 500:
        return 0
    will_be_collected = ((int(rating) / 100) - 4) * (100 * 101 / 2 - (100 - count_of_tasks - 1) *
                                                     (100 - count_of_tasks) / 2) / 100
    already_collected_points = ((int(rating) / 100) - 4) * (100 * 101 / 2 - (100 - count_of_tasks) *
                                                            (100 - count_of_tasks + 1) / 2) / 100
    return will_be_collected - already_collected_points


def isStillRelevant(handle, rating):
    return countOfTasksWithRating(handle, rating) < 100


def getCountOfSolvedTaskWithContestId(contest_id, handle):
    try:
        request_url = "https://codeforces.com/api/contest.status?contestId=" + str(contest_id) + "&handle=" + str(handle)
        response = urllib.request.urlopen(request_url)
        res = json.loads(response.read())
    except Exception:
        return -1
    solved_indexes = {}
    if 'result' not in res or res['status'] != 'OK':
        return -1
    for solution in res['result']:
        if 'problem' not in solution or 'index' not in solution['problem'] or 'verdict' not in solution \
                or solution['verdict'] != 'OK':
            continue
        solved_indexes[solution['problem']['index']] = solution['verdict']
    return len(solved_indexes)


def getCountOfRatedContestFromTime(handle, start_time):
    try:
        request_url = "https://codeforces.com/api/user.rating?handle=" + handle
        response = urllib.request.urlopen(request_url)
        res = json.loads(response.read())
    except Exception:
        return {"Error": "can not get info from cf"}
    if res['status'] != 'OK':
        return {"Error": "can not get info from cf"}
    count_of_contests = 0
    for contest in res['result']:
        if contest['ratingUpdateTimeSeconds'] >= start_time:
            count_of_contests = count_of_contests + 1
    return count_of_contests


def getTaskWithTagAndRating(handle, tag, rating):
    try:
        request_url = 'http://codeforces.com/api/user.info?handles=' + handle
        response = urllib.request.urlopen(request_url)
        res = json.loads(response.read())
    except Exception:
        return {'Error', 'incorrect handle'}
    try:
        request_url = "https://codeforces.com/api/problemset.problems?tags=" + str(tag)
        response = urllib.request.urlopen(request_url)
        res = json.loads(response.read())
    except Exception:
        return {"Error": "can not get info from cf"}
    if 'status' not in res or res['status'] != 'OK' or 'result' not in res or 'problems' not in res['result']:
        return {"Error": "can not get info from cf"}
    solved_tasks = getInfoAboutSolvedTasksWithHandle(handle)
    list_of_unsolved_tasks = []
    for task in res['result']['problems']:
        if 'rating' not in task or 'contestId' not in task or 'index' not in task or 'name' not in task:
            continue
        if str(task['rating']) == str(rating) and task['name'] not in solved_tasks[rating]:
            list_of_unsolved_tasks.append("https://codeforces.com/problemset/problem/" + str(task['contestId']) +
                                          '/' + str(task['index']))
    size = len(list_of_unsolved_tasks)
    if size == 0:
        return {"Error": "there no unsolved tasks with this rating and tag"}
    position = random.randint(0, max(size - 1, 0))
    return list_of_unsolved_tasks[position]


def getCountOfSubmissionsForAMonth(handle):
    try:
        request_url = 'http://codeforces.com/api/user.status?handle=' + handle
        response = urllib.request.urlopen(request_url)
        res = json.loads(response.read())
    except Exception:
        return {"Error": "can not get info from cf"}
    if 'result' not in res:
        return {"Error": "can not find result in json"}
    one_month_ago_time = time.mktime(datetime.datetime.now().timetuple()) - 86400 * 30
    count_of_sub = 0
    for task in res['result']:
        if 'creationTimeSeconds' not in task:
            continue
        if task['creationTimeSeconds'] < one_month_ago_time:
            break
        count_of_sub += 1
    return count_of_sub


def get_count_of_solved_tasks_for_some_days(handle, count_of_days):
    info_about_solved_tasks = getInfoAboutSolvedTasksWithHandle(handle)
    start = time.mktime(datetime.datetime.now().timetuple()) - 86400 * count_of_days
    count_of_solved_task = 0
    for rating in info_about_solved_tasks:
        for name in info_about_solved_tasks[rating]:
            if info_about_solved_tasks[rating][name]['creationTimeSeconds'] >= start:
                count_of_solved_task += 1
    return count_of_solved_task


def count_of_comp_points(handle):
    info = getInfoAboutSolvedTasksWithHandle(handle)
    if 'Error' in info:
        return -1
    points = 0
    for rating in info:
        for name in info[rating]:
            if info[rating][name]['creationTimeSeconds'] <= constants.comp_time_of_last_reset[handle]:
                break
            if info[rating][name]['creationTimeSeconds'] >= constants.comp_start_time:
                if handle not in constants.comp_time_of_last_reset:
                    constants.comp_time_of_last_reset[handle] = info[rating][name]['creationTimeSeconds']
                else:
                    constants.comp_time_of_last_reset[handle] = max(info[rating][name]['creationTimeSeconds'],
                                                                    constants.comp_time_of_last_reset[handle])
                r = rating
                if rating == 0:
                    r = 1500
                points += (r - 500) / 100
    return points
