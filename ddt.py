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

getAllActiveUsers(7)
print(len(active_users))
for handle in active_users:
    print (handle[constants.TABLE_COLUMN_HANDLE_])
