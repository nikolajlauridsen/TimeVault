"""
Helpful rebindings and helper functions, for that extra laziness
"""
import datetime


def convert_unix(unix_stamp, _format):
    """Convert a unix timestamp to a time string"""
    return datetime.datetime.fromtimestamp(unix_stamp).strftime(_format)


def convert_timestamp(stamp, _format):
    """Convert a timestamp to a unix timestamp"""
    return datetime.datetime.strptime(stamp, _format).timestamp()