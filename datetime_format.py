from datetime import date, datetime

DATE_FORMAT = '%d.%m.%Y'
TIME_FORMAT = '%H:%M:%S'
FORMAT = DATE_FORMAT + ' ' + TIME_FORMAT


def date_to_str(d: date) -> str:
    return d.strftime(DATE_FORMAT)


def datetime_to_str(dt: datetime) -> str:
    return dt.strftime(FORMAT)


def str_to_datetime(str_dt) -> datetime:
    return datetime.strptime(str_dt, FORMAT)
