import datetime
import time

import cf_api
import constants
import table

active_users = []


def isRuban(vk_id):
    return vk_id == '5310380'


def getAllActiveUsers(number_of_days):  # probably not work
    global active_users
    active_users = []
    table.getAllUsersInfo()
    users = table.getAllUsersInfo()
    for user in users:
        last_submission_time = cf_api.getTimeOfLastSubmissionWithHandle(user[constants.TABLE_COLUMN_HANDLE_])
        unixtime = time.mktime(datetime.datetime.now().timetuple())
        if unixtime - number_of_days * 86400 <= last_submission_time:
            active_users.append(user)


def mostDifficultTaskForSomeDay(number_of_days):  # probably not work
    getAllActiveUsers(number_of_days)
    res = {}
    unixtime = time.mktime(datetime.datetime.now().timetuple())
    for user in active_users:
        handle = user[constants.TABLE_COLUMN_HANDLE_]
        info = cf_api.getInfoAboutSolvedTasksWithHandle(handle)
        if 'Error' in info:
            continue
        if len(info) < 1:
            continue
        diff = 0
        for rating in info:
            if rating == 0:
                continue
            for task_name in info[rating]:
                if unixtime - number_of_days * 86400 <= info[rating][task_name] and rating > diff:
                    diff = rating
        res[handle] = diff
    res = sorted(res.items(), key=lambda value: int(value[1]), reverse=True)
    return res


def theMostSolvedTaskFromUnsolved(handle):
    bad_users = ['ruban', 'nongi', 'uwplp']
    if handle in bad_users:
        return "U r too good, sry!"
    solved_tasks_with_handle = cf_api.getInfoAboutSolvedTasksWithHandle(handle)
    if 'Error' in solved_tasks_with_handle:
        return ""
    users = table.getAllUsersInfo()
    task_counter = {}
    tasks = {}
    for user in users:
        if user[constants.TABLE_COLUMN_HANDLE_] in bad_users:
            continue
        solved_tasks = cf_api.getInfoAboutSolvedTasksWithHandle(user[constants.TABLE_COLUMN_HANDLE_])
        if 'Error' in solved_tasks:
            continue
        for rating in solved_tasks:
            if rating == 0:
                continue
            for name in solved_tasks[rating]:
                if rating in solved_tasks_with_handle and name in solved_tasks_with_handle[rating]:
                    continue
                if name not in task_counter:
                    task_counter[name] = 0
                    tasks[name] = solved_tasks[rating][name]
                task_counter[name] = task_counter[name] + 1
    mx = 0
    name = ""
    for task_name in task_counter:
        if task_counter[task_name] > mx:
            mx = task_counter[task_name]
            name = task_name
    return "https://codeforces.com/problemset/problem/" + str(tasks[name]["contestId"]) + '/' \
           + str(tasks[name]["index"])


def getExempted(handle):
    start_time = 1577891404
    index_of_dinamic_training = '100135'
    index_of_graph = '100235'
    index_of_geometry = '100168'
    solved_dinamic_tasks = cf_api.getCountOfSolvedTaskWithContestId(index_of_dinamic_training, handle)
    solved_graph_tasks = cf_api.getCountOfSolvedTaskWithContestId(index_of_graph, handle)
    solved_geometry_tasks = cf_api.getCountOfSolvedTaskWithContestId(index_of_geometry, handle)
    count_of_rated_contest = cf_api.getCountOfRatedContestFromTime(handle, start_time)
    return {'dinamic': str(solved_dinamic_tasks),
            'graph': str(solved_graph_tasks),
            'geometry': str(solved_geometry_tasks),
            'contests': str(count_of_rated_contest)}


def specialForYou():
    tasks = cf_api.getInfoAboutSolvedTasksWithHandle('justBoss')
    return cf_api.getUnsolvedTasksWithHandleAndTasks('fancyFox', tasks)

    # tasks = cf_api.getInfoAboutSolvedTasksWithHandle('nongi')
    # users = table.getAllUsersInfo()
    # for user in users:
    #     handle = user[constants.TABLE_COLUMN_HANDLE_]
    #     if handle == 'uwplp' or handle == 'ruban' or handle == 'nongi' or handle == 'kcherdakov':
    #         continue
    #     cf_api.getUnsolvedTasksWithHandleAndTasks(handle, tasks)
    # mn = 100000
    # for rating in tasks:
    #     if 999 < rating < mn:
    #         mn = rating
    # for name in tasks[mn]:
    #     print("https://codeforces.com/problemset/problem/" + str(tasks[mn][name]["contestId"]) + '/'
    #           + str(tasks[mn][name]["index"]))


def some_unsolved_tasks():
    return ["https://codeforces.com/problemset/problem/620/B",
            "https://codeforces.com/problemset/problem/837/A",
            "https://codeforces.com/problemset/problem/844/A",
            "https://codeforces.com/problemset/problem/820/A",
            "https://codeforces.com/problemset/problem/810/A",
            "https://codeforces.com/problemset/problem/834/A",
            "https://codeforces.com/problemset/problem/818/A",
            "https://codeforces.com/problemset/problem/805/B",
            "https://codeforces.com/problemset/problem/805/A",
            "https://codeforces.com/problemset/problem/793/A",
            "https://codeforces.com/problemset/problem/801/B",
            "https://codeforces.com/problemset/problem/768/A",
            "https://codeforces.com/problemset/problem/94/A",
            "https://codeforces.com/problemset/problem/137/A",
            "https://codeforces.com/problemset/problem/246/A",
            "https://codeforces.com/problemset/problem/29/A",
            "https://codeforces.com/problemset/problem/263/B",
            "https://codeforces.com/problemset/problem/376/A",
            "https://codeforces.com/problemset/problem/221/A",
            "https://codeforces.com/problemset/problem/265/B"]
