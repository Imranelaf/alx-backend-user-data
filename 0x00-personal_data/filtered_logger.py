#!/usr/bin/env python3

'''
This module is a secure log filter
'''

import logging
from mysql.connector.connection import MySQLConnection
import os
import re
from typing import List

PII_FIELDS = ('name', 'email', 'phone', 'password', 'ssn')


def filter_datum(
        fields: List[str],
        redaction: str,
        message: str,
        separator: str,
) -> str:
    '''
    Returns a string.
    Args:
        fields: a list of strings.
        redaction: a string argument.
        message: a string argument.
        separator: a string argument.
    Returns:
        A string.
    '''
    logtext = message
    for field in fields:
        logtext = re.sub(field + "=.*?" + separator,
                         field + "=" + redaction + separator, logtext)
    return logtext


def get_logger() -> logging.Logger:
    '''
    Returns a logging.Logger object.
    Returns:
        A logging.Logger object.
    '''
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(stream_handler)
    return logger


def get_db() -> MySQLConnection:
    '''
    Returns a MySQLConnection object.
    Returns:
        A MySQLConnection object.
    '''
    return MySQLConnection(
        user=os.getenv("PERSONAL_DATA_DB_USERNAME", "root"),
        port=3306,
        password=os.getenv("PERSONAL_DATA_DB_PASSWORD", ""),
        host=os.getenv("PERSONAL_DATA_DB_HOST", "localhost"),
        database=os.getenv("PERSONAL_DATA_DB_NAME")
    )


class RedactingFormatter(logging.Formatter):
    '''
    This class inherits from logging.Formatter.
    Attributes:
        REDACTION: a string.
        FORMAT: a string.
        SEPARATOR: a string.
        fields: a list of strings.
    Methods:
        format: returns a string.
    '''
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        '''
        initialization
        '''
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        '''
        Returns a string.
        Args:
            record: a logging.LogRecord object.
        Returns:
            A string.
        '''
        return filter_datum(
            self.fields, self.REDACTION, super(
                RedactingFormatter, self).format(record), self.SEPARATOR)


def main() -> None:
    '''
    This function logs rows from the users table.
    Returns:
        None
    '''

    db_connector = get_db()
    csr = db_connector.cursor()
    csr.execute("SELECT * FROM users;")
    logger = get_logger()

    for row in csr:
        # Check if any of the row values are in PII_FIELDS
        if any(field in str(row) for field in PII_FIELDS):
            message = ""
            for i in range(len(row)):
                message += f"{csr.column_names[i]}={str(row[i])}; "
            logger.info(message)

    csr.close()
    db_connector.close()


if __name__ == "__main__":
    main()
