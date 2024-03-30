"""Additional utils"""
import time
from datetime import datetime


def get_mexc_timestamp() -> int:
    """Returns the current timestamp in milliseconds."""
    return round(time.time() * 1000)


def get_timestamp():
    """Returns current timestamp"""
    return datetime.now()
