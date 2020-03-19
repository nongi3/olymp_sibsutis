import datetime
import functools
import json
import random
import time
import urllib.request

import secret_constants

spreadsheet_id_832 = "1HljGGA8sQJYfq5NuITA5kUVeKsVxtGP8DZBuY44rZfs"
spreadsheet_id_841 = "1LQ09dByQaGFUf3uOs6hLQoRNtykRqJtNBcsM0ddQs4I"
spreadsheet_id_842 = "19lLtyCv-I3RRRJUb2wk51Pr5RHK9sKPPXyPU1uf5FlY"


def getAllUsersInfo(group):
    if group == '832':
        spreadsheet_id = spreadsheet_id_832
    elif group == '841':
        spreadsheet_id = spreadsheet_id_841
    else:
        spreadsheet_id = spreadsheet_id_842
    values = secret_constants.service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range='A2:N20',
        majorDimension='ROWS'
    ).execute()
    return values['values']


def setAllUsersInfo(values, group):
    if group == '832':
        spreadsheet_id = spreadsheet_id_832
    elif group == '841':
        spreadsheet_id = spreadsheet_id_841
    else:
        spreadsheet_id = spreadsheet_id_842
    data = {'range': 'A2:N20', 'majorDimension': 'ROWS',
            'values': values}
    buv = {'value_input_option': 'USER_ENTERED', 'data': data}

    secret_constants.service.spreadsheets().values().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body=buv
    ).execute()


def setLab(row, col, group, url):
    info = getAllUsersInfo(group)
    if 2 <= row <= len(info) and 1 <= col <= 12:
        info[row - 2][col] = url
        setAllUsersInfo(info, group)
