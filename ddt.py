import datetime
import time

import cf_api
import constants
import table


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


def taskDiffOfTwoUsers(from_user, to_user):
    tasks = cf_api.getInfoAboutSolvedTasksWithHandle(from_user)
    return cf_api.getUnsolvedTasksWithHandleAndTasks(to_user, tasks)
