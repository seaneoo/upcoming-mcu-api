from datetime import datetime

import pytz

DATETIME_FORMAT = "%Y-%m-%d"


def get_current_datetime():
    tz = pytz.timezone("America/New_York")
    return datetime.now(tz)


def parse_date(date_str: str):
    return datetime.strptime(date_str, DATETIME_FORMAT)


def format_datetime(dt: datetime):
    return dt.strftime(DATETIME_FORMAT)
