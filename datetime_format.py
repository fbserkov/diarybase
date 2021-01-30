from datetime import date, datetime

DATE_FORMAT = '%d.%m.%Y'
TIME_FORMAT = '%H:%M:%S'
FORMAT = DATE_FORMAT + ' ' + TIME_FORMAT


def date_to_str(d: date) -> str:
    """
    >>> date_to_str(date(2021, 1, 30))
    '30.01.2021'
    """
    return d.strftime(DATE_FORMAT)


def datetime_to_str(dt: datetime) -> str:
    """
    >>> datetime_to_str(datetime(2021, 1, 30, 18, 29, 30))
    '30.01.2021 18:29:30'
    """
    return dt.strftime(FORMAT)


def str_to_datetime(str_dt) -> datetime:
    """
    >>> str_to_datetime('30.01.2021 18:29:30')
    datetime.datetime(2021, 1, 30, 18, 29, 30)
    """
    return datetime.strptime(str_dt, FORMAT)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
