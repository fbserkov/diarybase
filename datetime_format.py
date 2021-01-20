from datetime import datetime

FORMAT = '%d.%m.%Y %H:%M:%S'


def dt_to_str(_dt):
    return _dt.strftime(FORMAT)


def str_to_dt(str_dt):
    return datetime.strptime(str_dt, FORMAT)
