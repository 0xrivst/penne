"""
Module with various time-related utility functions.
"""

from datetime import datetime, timezone


def get_current_utc_datetime():
    """
    Returns the current UTC datetime
    """
    return datetime.now(tz=timezone.utc)
