from datetime import datetime
# convert string to datetime
def strToDatetime(str_datetime):
    date_format = '%Y-%m-%d'
    try:
        dt = datetime.strptime(str_datetime, date_format)
        return dt
    except:
        print('Wrong datetime string formate!') 
    return


# convert datetime to int
def datetimeToInt(dt):
    return 10000*dt.year + 100*dt.month + dt.day