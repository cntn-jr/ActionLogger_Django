import datetime

def isTime(month, day, time):
    try:
        date = datetime.datetime.now()
        strDate = str(date.year) + '-' + month + '-' + day + ' ' + time + ':00:00'
        after = datetime.datetime.strptime(strDate, '%Y-%m-%d %H:%M:%S')
        return after
    except ValueError:
        #正当な値が入力されなかった場合
        return datetime.datetime.strptime('2000-1-1 00:00:30','%Y-%m-%d %H:%M:%S')

def printTopColumn(column):
    if(len(column) > 10):
        column=column[0:9] + '...'
    return column

week_list = ['月','火','水','木','金','土','日']
def dateFormat(logDate):
    logDate1 = logDate.strftime("%-m月%-d日（")
    logDate2 = logDate.strftime("） %-H時頃")
    week = week_list[logDate.weekday()]
    logDate = logDate1 + week + logDate2
    return logDate
