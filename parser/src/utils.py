"""Additional utils"""
from datetime import datetime
import time


def get_mexc_timestamp() -> int:
    """Returns the current timestamp in milliseconds."""
    return round(time.time() * 1000)


def get_timestamp():
    """Returns current timestamp"""
    return datetime.now()
