#!/usr/bin/env python3
"""
    that returns the log message obfuscated
"""
from typing import List
import re
import logging

field_list = []
file = open('user_data.csv', 'r')
first_line = file.readline()
args = first_line.split(',')
PII_FIELDS = tuple(args[1:-2])


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """return:  log message"""
    for field in fields:
        pattern = rf'({re.escape(field)}=)([^{re.escape(separator)}]*)'
        message = re.sub(pattern, rf'\1{redaction}', message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    # custom formatter instead of self.DEFAULT_FORMAT by default
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """method to filter values in incoming log records"""
        filter_msg = filter_datum(self.fields, self.REDACTION,
                                  record.msg, self.SEPARATOR)
        record.msg = filter_msg
        return super().format(record)


def get_logger() -> logging.Logger:
    """returns a logging.Logger object"""
    # Create a logger and configure logging
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    # create handler
    handler = logging.StreamHandler()
    form = RedactingFormatter(fields=PII_FIELDS)
    handler.setFormatter(form.format(logger))
    # add handler
    logger.addHandler(handler)

    return logger
