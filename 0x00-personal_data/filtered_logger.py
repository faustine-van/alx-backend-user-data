#!/usr/bin/env python3
"""
    that returns the log message obfuscated
"""
from typing import List
import re
import logging


file = open('user_data.csv', 'r', encoding='utf-8')
first_line = file.readline()
args = first_line.split(',')
PII_FIELDS = tuple(args[2:-1])


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
    # set logging level
    logger.setLevel(logging.INFO)
    # prevents propagate messages to other loggers
    # set propagate to False
    logger.propagate = False
    # #create handler
    handler = logging.StreamHandler()
    formatter = RedactingFormatter(fields=PII_FIELDS)
    handler.setFormatter(formatter)
    # add handler
    logger.addHandler(handler)

    return logger
