"""
Функции для генерации случайных дат и времени.
"""

import datetime as _dt
from .core import randint, random, choices, uniform
import time as _time
import calendar as _calendar

def date(start_date=None, end_date=None):
    """
    Генерирует случайную дату в указанном диапазоне.
    
    Args:
        start_date: Начальная дата диапазона (в формате datetime.date, ISO-строка 'YYYY-MM-DD' или None).
            По умолчанию None (1970-01-01).
        end_date: Конечная дата диапазона (в формате datetime.date, ISO-строка 'YYYY-MM-DD' или None).
            По умолчанию None (текущая дата).
            
    Returns:
        datetime.date: Случайная дата в указанном диапазоне.
    """
    if start_date is None:
        start_date = _dt.date(1970, 1, 1)
    
    if end_date is None:
        end_date = _dt.date.today()
    
    if isinstance(start_date, str):
        start_date = _dt.datetime.strptime(start_date, "%Y-%m-%d").date()
    
    if isinstance(end_date, str):
        end_date = _dt.datetime.strptime(end_date, "%Y-%m-%d").date()
    
    delta_days = (end_date - start_date).days
    
    if delta_days < 0:
        raise ValueError("start_date должна быть до end_date")
    
    random_days = randint(0, delta_days)
    
    return start_date + _dt.timedelta(days=random_days)

def time(start_time=None, end_time=None):
    """
    Генерирует случайное время в указанном диапазоне.
    
    Args:
        start_time: Начальное время диапазона (в формате datetime.time, строка 'HH:MM:SS' или None).
            По умолчанию None (00:00:00).
        end_time: Конечное время диапазона (в формате datetime.time, строка 'HH:MM:SS' или None).
            По умолчанию None (23:59:59).
            
    Returns:
        datetime.time: Случайное время в указанном диапазоне.
    """
    if start_time is None:
        start_time = _dt.time(0, 0, 0)
    
    if end_time is None:
        end_time = _dt.time(23, 59, 59)
    
    if isinstance(start_time, str):
        start_time = _dt.datetime.strptime(start_time, "%H:%M:%S").time()
    
    if isinstance(end_time, str):
        end_time = _dt.datetime.strptime(end_time, "%H:%M:%S").time()
    
    start_seconds = start_time.hour * 3600 + start_time.minute * 60 + start_time.second
    end_seconds = end_time.hour * 3600 + end_time.minute * 60 + end_time.second
    
    if end_seconds < start_seconds:
        raise ValueError("start_time должно быть до end_time")
    
    random_seconds = randint(start_seconds, end_seconds)
    
    hours, remainder = divmod(random_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    return _dt.time(hours, minutes, seconds)

def datetime(start_datetime=None, end_datetime=None):
    """
    Генерирует случайную дату и время в указанном диапазоне.
    
    Args:
        start_datetime: Начальные дата и время диапазона (datetime.datetime, ISO-строка или None).
            По умолчанию None (1970-01-01 00:00:00).
        end_datetime: Конечные дата и время диапазона (datetime.datetime, ISO-строка или None).
            По умолчанию None (текущие дата и время).
            
    Returns:
        datetime.datetime: Случайные дата и время в указанном диапазоне.
    """
    if start_datetime is None:
        start_datetime = _dt.datetime(1970, 1, 1, 0, 0, 0)
    
    if end_datetime is None:
        end_datetime = _dt.datetime.now()
    
    if isinstance(start_datetime, str):
        start_datetime = _dt.datetime.strptime(start_datetime, "%Y-%m-%d %H:%M:%S")
    
    if isinstance(end_datetime, str):
        end_datetime = _dt.datetime.strptime(end_datetime, "%Y-%m-%d %H:%M:%S")
    
    delta_seconds = int((end_datetime - start_datetime).total_seconds())
    
    if delta_seconds < 0:
        raise ValueError("start_datetime должно быть до end_datetime")
    
    random_seconds = randint(0, delta_seconds)
    
    return start_datetime + _dt.timedelta(seconds=random_seconds)

def timestamp(start_timestamp=None, end_timestamp=None):
    """
    Генерирует случайную метку времени (timestamp) в указанном диапазоне.
    
    Args:
        start_timestamp: Начальная метка времени (число секунд с эпохи Unix или None).
            По умолчанию None (0, т.е. 1970-01-01 00:00:00 UTC).
        end_timestamp: Конечная метка времени (число секунд с эпохи Unix или None).
            По умолчанию None (текущее время).
            
    Returns:
        float: Случайная метка времени в указанном диапазоне.
    """
    if start_timestamp is None:
        start_timestamp = 0
    
    if end_timestamp is None:
        end_timestamp = int(_time.time())
    
    if isinstance(start_timestamp, str):
        start_timestamp = int(_dt.datetime.strptime(start_timestamp, "%Y-%m-%d %H:%M:%S").timestamp())
    
    if isinstance(end_timestamp, str):
        end_timestamp = int(_dt.datetime.strptime(end_timestamp, "%Y-%m-%d %H:%M:%S").timestamp())
    
    return randint(start_timestamp, end_timestamp)

def time_period(min_seconds=0, max_seconds=86400, as_timedelta=True):
    """
    Генерирует случайный временной период в указанном диапазоне.
    
    Args:
        min_seconds: Минимальное количество секунд. По умолчанию 0.
        max_seconds: Максимальное количество секунд. По умолчанию 86400 (1 день).
        as_timedelta: Возвращать ли результат как объект timedelta. По умолчанию True.
            
    Returns:
        datetime.timedelta или int: Случайный временной период.
    """
    if min_seconds < 0 or max_seconds < min_seconds:
        raise ValueError("min_seconds должно быть >= 0 и <= max_seconds")
    
    seconds = randint(min_seconds, max_seconds)
    
    if as_timedelta:
        return _dt.timedelta(seconds=seconds)
    else:
        return seconds

def future_date(min_days=1, max_days=365):
    """
    Генерирует случайную дату в будущем.
    
    Args:
        min_days: Минимальное количество дней от текущей даты. По умолчанию 1.
        max_days: Максимальное количество дней от текущей даты. По умолчанию 365.
            
    Returns:
        datetime.date: Случайная дата в будущем.
    """
    if min_days < 0 or max_days < min_days:
        raise ValueError("min_days должно быть >= 0 и <= max_days")
    
    today = _dt.date.today()
    days_to_add = randint(min_days, max_days)
    
    return today + _dt.timedelta(days=days_to_add)

def past_date(min_days=1, max_days=365):
    """
    Генерирует случайную дату в прошлом.
    
    Args:
        min_days: Минимальное количество дней до текущей даты. По умолчанию 1.
        max_days: Максимальное количество дней до текущей даты. По умолчанию 365.
            
    Returns:
        datetime.date: Случайная дата в прошлом.
    """
    if min_days < 0 or max_days < min_days:
        raise ValueError("min_days должно быть >= 0 и <= max_days")
    
    today = _dt.date.today()
    days_to_subtract = randint(min_days, max_days)
    
    return today - _dt.timedelta(days=days_to_subtract)

def weekday(return_name=False):
    """
    Генерирует случайный день недели.
    
    Args:
        return_name: Возвращать ли название дня недели вместо числа. По умолчанию False.
            
    Returns:
        int или str: Случайный день недели (0-6, где 0 - понедельник, или название).
    """
    day = randint(0, 6)
    
    if return_name:
        days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
        return days[day]
    else:
        return day

def month(return_name=False):
    """
    Генерирует случайный месяц.
    
    Args:
        return_name: Возвращать ли название месяца вместо числа. По умолчанию False.
            
    Returns:
        int или str: Случайный месяц (1-12 или название).
    """
    month_num = randint(1, 12)
    
    if return_name:
        months = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", 
                 "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]
        return months[month_num - 1]
    else:
        return month_num

def month_name(locale='en'):
    month_num = month()
    
    if locale.lower() == 'ru':
        month_names_ru = [
            'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
            'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'
        ]
        return month_names_ru[month_num - 1]
    else:
        return _calendar.month_name[month_num]

def day_of_month(month_num=None, year=None):
    if month_num is None:
        month_num = month()
    
    if year is None:
        year = randint(1970, _dt.date.today().year)
    
    max_day = _calendar.monthrange(year, month_num)[1]
    return randint(1, max_day)

def day_of_week():
    return randint(0, 6)

def day_of_week_name(locale='en'):
    day_num = day_of_week()
    
    if locale.lower() == 'ru':
        day_names_ru = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
        return day_names_ru[day_num]
    else:
        return _calendar.day_name[day_num]

def year(start_year=1970, end_year=None):
    if end_year is None:
        end_year = _dt.date.today().year
    
    return randint(start_year, end_year)

def hour(hour_format=24):
    if hour_format == 12:
        return randint(1, 12)
    elif hour_format == 24:
        return randint(0, 23)
    else:
        raise ValueError("hour_format должен быть 12 или 24")

def minute():
    return randint(0, 59)

def second():
    return randint(0, 59)

def millisecond():
    return randint(0, 999)

def timezone():
    offsets = list(range(-12, 15))
    offset = choices(offsets)[0]
    sign = "+" if offset >= 0 else "-"
    abs_offset = abs(offset)
    return f"UTC{sign}{abs_offset:02d}:00"

def iso8601(start_date=None, end_date=None):
    dt = datetime(start_date, end_date)
    return dt.isoformat()

def iso8601_date(start_date=None, end_date=None):
    d = date(start_date, end_date)
    return d.isoformat()

def iso8601_time(start_time=None, end_time=None):
    t = time(start_time, end_time)
    return t.isoformat()

def rfc3339(start_date=None, end_date=None):
    dt = datetime(start_date, end_date)
    return dt.strftime('%Y-%m-%dT%H:%M:%SZ')

def unix_time(start_time=None, end_time=None):
    return timestamp(start_time, end_time)

def time_delta(min_seconds=0, max_seconds=86400):
    seconds = randint(min_seconds, max_seconds)
    return _dt.timedelta(seconds=seconds)

def business_date(start_date=None, end_date=None):
    d = date(start_date, end_date)
    
    while d.weekday() >= 5:
        d += _dt.timedelta(days=1)
    
    return d

def business_datetime(start_datetime=None, end_datetime=None, start_hour=9, end_hour=17):
    dt = datetime(start_datetime, end_datetime)
    
    while dt.weekday() >= 5 or dt.hour < start_hour or dt.hour >= end_hour:
        if dt.weekday() >= 5:
            dt += _dt.timedelta(days=1)
            dt = dt.replace(hour=start_hour, minute=0, second=0)
        elif dt.hour < start_hour:
            dt = dt.replace(hour=start_hour, minute=0, second=0)
        elif dt.hour >= end_hour:
            dt += _dt.timedelta(days=1)
            dt = dt.replace(hour=start_hour, minute=0, second=0)
    
    return dt

def date_between_holidays(holidays, year=None):
    if year is None:
        year = _dt.date.today().year
    
    if not holidays:
        raise ValueError("holidays не может быть пустым")
    
    holidays_in_year = [holiday for holiday in holidays if isinstance(holiday, _dt.date) and holiday.year == year]
    
    if not holidays_in_year:
        raise ValueError(f"Нет праздников в указанном году {year}")
    
    holidays_in_year.sort()
    
    start_idx = randint(0, len(holidays_in_year) - 2)
    start_date = holidays_in_year[start_idx]
    end_date = holidays_in_year[start_idx + 1]
    
    delta_days = (end_date - start_date).days
    
    if delta_days <= 1:
        return end_date
    
    random_days = randint(1, delta_days - 1)
    
    return start_date + _dt.timedelta(days=random_days)

def quarter():
    return randint(1, 4)

def date_in_quarter(quarter_num=None, year=None):
    if quarter_num is None:
        quarter_num = quarter()
    
    if year is None:
        year = _dt.date.today().year
    
    quarter_start_month = (quarter_num - 1) * 3 + 1
    quarter_end_month = quarter_start_month + 2
    
    start_date = _dt.date(year, quarter_start_month, 1)
    
    if quarter_end_month == 12:
        end_date = _dt.date(year, 12, 31)
    else:
        end_date = _dt.date(year, quarter_end_month + 1, 1) - _dt.timedelta(days=1)
    
    return date(start_date, end_date)

def week_number():
    return randint(1, 53)

def date_in_week(week_num=None, year=None):
    if year is None:
        year = _dt.date.today().year
    
    if week_num is None:
        week_num = week_number()
    
    first_day = _dt.date(year, 1, 1)
    
    if first_day.weekday() > 0:
        first_day = first_day - _dt.timedelta(days=first_day.weekday())
    
    week_start = first_day + _dt.timedelta(weeks=week_num-1)
    week_end = week_start + _dt.timedelta(days=6)
    
    return date(week_start, week_end)

def date_with_age(min_age=18, max_age=100):
    today = _dt.date.today()
    min_date = today.replace(year=today.year - max_age)
    max_date = today.replace(year=today.year - min_age)
    
    return date(min_date, max_date)

def duration_string(max_hours=24):
    hours = randint(0, max_hours)
    minutes = randint(0, 59)
    seconds = randint(0, 59)
    
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

def cron_expression():
    minute = '*' if random() < 0.7 else str(randint(0, 59))
    hour = '*' if random() < 0.7 else str(randint(0, 23))
    day_of_month = '*' if random() < 0.7 else str(randint(1, 28))
    month = '*' if random() < 0.7 else str(randint(1, 12))
    day_of_week = '*' if random() < 0.7 else str(randint(0, 6))
    
    return f"{minute} {hour} {day_of_month} {month} {day_of_week}" 