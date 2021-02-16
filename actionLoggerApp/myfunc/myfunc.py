import datetime

def isTime(month, day, time):
    try:
        date = datetime.datetime.now()
        strDate = str(date.year) + '-' + month + '-' + day + ' ' + time + ':00:00'
        after = datetime.datetime.strptime(strDate, '%Y-%m-%d %H:%M:%S')
        return after
    except ValueError:
        return datetime.datetime.strptime('2000-1-1 00:00:30','%Y-%m-%d %H:%M:%S')