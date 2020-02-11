import datetime
import time

import cf_api
import constants
import table


active_users = []

def isRuban(vk_id):
    return vk_id == '5310380'

def getAllActiveUsers(number_of_days):
    global active_users
    active_users = []
    table.getAllUsersInfo()
    users = table.getAllUsersInfo()
    for user in users:
        last_submission_time = cf_api.getTimeOfLastSubmissionWithHandle(user[constants.TABLE_COLUMN_HANDLE_])
        unixtime = time.mktime(datetime.datetime.now().timetuple())
        if unixtime - number_of_days * 86400 <= last_submission_time:
            active_users.append(user)

def mostDifficultTaskForSomeDay(number_of_days):
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
            for task_name in info[rating]:
                if unixtime - number_of_days * 86400 <= info[rating][task_name] and rating > diff:
                    diff = rating
        res[handle] = diff
    res = sorted(res.items(), key=lambda value: int(value[1]), reverse=True)
    return res
