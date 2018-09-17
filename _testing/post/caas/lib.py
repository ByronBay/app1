import datetime
import uuid


def get_uuid():
    return uuid.uuid4()

def get_timestamp():
    return datetime.datetime.now().isoformat().replace(':','-')
