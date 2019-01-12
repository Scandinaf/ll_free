import datetime

from utils.helper import DateTimeHelper

year = 2020
month = 5
day = 17
hour = 12
minute = 45
helper = DateTimeHelper()
helper.current_date_time = datetime.datetime(year=year, month=month, day=day, hour=hour, minute=minute)


def test_subtract_months():
    count = 1
    result = helper.subtract_months(count)
    assert result == datetime.datetime(year=year, month=month-count, day=day, hour=hour, minute=minute)


def test_subtract_days():
    count = 5
    result = helper.subtract_days(count)
    assert result == datetime.datetime(year=year, month=month, day=day-count, hour=hour, minute=minute)


def test_subtract_minutes():
    count = 30
    result = helper.subtract_minutes(30)
    assert result == datetime.datetime(year=year, month=month, day=day, hour=hour, minute=minute-count)


def test_get_current_date():
    result = helper.get_current_date_time()
    assert result == datetime.datetime(year=year, month=month, day=day, hour=hour, minute=minute)