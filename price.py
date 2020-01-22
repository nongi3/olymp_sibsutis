import urllib.request
import json
import datetime
import time
import functools

import constants
import secret_constants

def getAllPricesInfo():
    values = secret_constants.service.spreadsheets().values().get(
        spreadsheetId=secret_constants.PRICE_SH_ID_,
        range='B1:Q200',
        majorDimension='COLUMNS'
    ).execute()
    if 'values' not in values:
        return []
    else:
        return values['values']

def getPriceWithName(name):
    values = getAllPricesInfo()
    for value in values:
        for lot in value[0].split('/'):
            if lot == name:
                return value[1]
    return -1
