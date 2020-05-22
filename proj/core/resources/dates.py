from datetime import datetime

EPOCH = datetime.utcfromtimestamp(0)

def unix_time(dt):
    return (dt.replace(tzinfo=None) - EPOCH).total_seconds() * 1000.0
