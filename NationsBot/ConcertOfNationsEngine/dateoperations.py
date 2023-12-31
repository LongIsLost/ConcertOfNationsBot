from math import *

def date_validate(date):

    if ('m' not in date.keys() or 'y' not in date.keys()):
        logInfo("Invalid date", details = saveObject(date))
        return False

    if (type(date['m']) not in (int, float)):
        logInfo(f"Invalid month {date['m']}")
        return False

    if (type(date['y']) not in (int, float)):
        logInfo(f"Invalid year {date['y']}")
        return False

    return True

def date_fromstr(datestr):

    dateSplit = datestr.split('/')

    return {'m': int(dateSplit[0]), 'y': int(dateSplit[-1])}

def date_tostr(date):
    return f"{date['m']}/{date['y']}"

def date_add(date, numMonths):
    
    return {
        'm': min(12, date['m'] + numMonths),
        'y': floor(((date['y'] * 12) + date['m'] + numMonths) / 12)
        }

def date_grtrThan(date0, date1):
    
    return (date0['m'] + (date0['y']*12)) > (date1['m'] + (date1['y']*12))

def date_grtrThan_EqlTo(date0, date1):
    
    return (date0['m'] + (date0['y']*12)) >= (date1['m'] + (date1['y']*12))