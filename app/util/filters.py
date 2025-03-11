"""
A module for registering Jinja filters.
"""

from flask import current_app


def format_time(value):
    """
    Converts a datetime to a formatted string
    """
    return value.strftime("%d.%m.%Y %H:%M")


def register_filters():
    """
    Register defined filters
    """
    current_app.jinja_env.filters["format_time"] = format_time
