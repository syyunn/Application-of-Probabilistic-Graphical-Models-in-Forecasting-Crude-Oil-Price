import datetime


def convert_to_datetime(time: str):
    return datetime.datetime.strptime(time[:9], "%Y %m ").date()
