from datetime import datetime
from datetime import timedelta


def date_plus_days(date, days):
    if date == '':
        return current_day()
    my_date = datetime(int(date[0:4]), int(date[4:6]), int(date[6:8]))
    my_date = my_date + timedelta(days=days)
    if my_date > datetime.today():
        print(current_day())
        return current_day()
    print(my_date.strftime('%Y%m%d'))
    return my_date.strftime('%Y%m%d')


def date_less_days(date, days):
    my_date = datetime(int(date[0:4]), int(date[4:6]), int(date[6:8]))
    my_date = my_date - timedelta(days=days)
    return my_date.strftime('%Y%m%d')


def day_of_year(date):
    my_date = datetime.strptime(date, '%Y-%m-%d')
    return my_date.timetuple().tm_yday


def current_day():
    return datetime.today().strftime('%Y%m%d')


def current_day_weather():
    return datetime.today().strftime('%Y-%m-%d')


def date_weather_format(date):
    my_date = datetime(int(date[0:4]), int(date[4:6]), int(date[6:8]))
    return my_date.strftime('%Y-%m-%d')
