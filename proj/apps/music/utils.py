
from datetime import datetime
from datetime import timedelta


def get_max_wait_time():
    return datetime.now() + timedelta(minutes=10)
