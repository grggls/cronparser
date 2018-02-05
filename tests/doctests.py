"""This is a doctest based regression suite for cronparser.py Each '>>>' line
is run as if in a python shell, and counts as a test. The next line, if not
'>>>' is the expected output of the previous line. If anything doesn't match
exactly (including trailing spaces), the test fails.

Run these tests with 'make test'"""

from cronparser import CronTab
from cronparser import helpers

if __name__ == '__main__':
    import doctest
    doctest.testmod()
    CronTab('* * * * * df -h')

def run_init_tests():
    """
    >>> foo = CronTab('1 2 3 4 5')
    ERROR: not enough fields in the crontab
    >>> foo = CronTab('1 2 3 4 5 ls -la')
    >>> print foo
    minute        1
    hour          2
    day of month  3
    month         4
    day of week   5
    command       ls -la
    >>> foo = CronTab('1 * 3 4 5 ls -la')
    >>> print foo
    minute        1
    hour          0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23
    day of month  3
    month         4
    day of week   5
    command       ls -la
    >>> foo = CronTab('*/15 0 1,15 * 1-5 /usr/bin/find')
    >>> print foo
    minute        0 15 30 45
    hour          0
    day of month  1 15
    month         1 2 3 4 5 6 7 8 9 10 11 12
    day of week   1 2 3 4 5
    command       /usr/bin/find
    """

def run_validate_tests():
    """
    # validate_minute() tests
    >>> foo = CronTab('0 * * * * ls -la')
    >>> foo.validate_minute()
    '0'
    >>> foo = CronTab('*/5 * * * * ls -la')
    >>> foo.validate_minute()
    '0 5 10 15 20 25 30 35 40 45 50 55'
    >>> foo = CronTab('*/10 * * * * ls -la')
    >>> foo.validate_minute()
    '0 10 20 30 40 50'
    >>> foo = CronTab('1,2,3 * * * * ls -la')
    >>> foo.validate_minute()
    '1 2 3'
    >>> foo = CronTab('57-59 * * * * ls -la')
    >>> foo.validate_minute()
    '57 58 59'
    >>> foo = CronTab('1-60 * * * * ls -la')
    >>> foo.validate_minute()

    # validate_hour() tests
    >>> foo = CronTab('* 0 * * * ls -la')
    >>> foo.validate_hour()
    '0'
    >>> foo = CronTab('* */5 * * * ls -la')
    >>> foo.validate_hour()
    '0 5 10 15 20'
    >>> foo = CronTab('* * * * * ls -la')
    >>> foo.validate_hour()
    '0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23'
    >>> foo = CronTab('* 1,2,3 * * * ls -la')
    >>> foo.validate_hour()
    '1 2 3'
    >>> foo = CronTab('* 1-23 * * * ls -la')
    >>> foo.validate_hour()
    '1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23'
    >>> foo = CronTab('* 1-24 * * * ls -la')
    >>> foo.validate_hour()

    # validate_day_of_month()
    >>> foo = CronTab('* * 0 * * ls -la')
    >>> foo.validate_day_of_month()
    '0'
    >>> foo = CronTab('* * */5 * * ls -la')
    >>> foo.validate_day_of_month()
    '0 5 10 15 20 25 30'
    >>> foo = CronTab('* * * * * ls -la')
    >>> foo.validate_day_of_month()
    '0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31'
    >>> foo = CronTab('* * 1,2,3 * * ls -la')
    >>> foo.validate_day_of_month()
    '1 2 3'
    >>> foo = CronTab('* * 1-23 * * ls -la')
    >>> foo.validate_day_of_month()
    '1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23'
    >>> foo = CronTab('* * 1-32 * * ls -la')
    >>> foo.validate_day_of_month()

    # validate_month()
    >>> foo = CronTab('* * * 1 * ls -la')
    >>> foo.validate_month()
    '1'
    >>> foo = CronTab('* * * */2 * ls -la')
    >>> foo.validate_month()
    '2 4 6 8 10 12'
    >>> foo = CronTab('* * * * * ls -la')
    >>> foo.validate_month()
    '1 2 3 4 5 6 7 8 9 10 11 12'
    >>> foo = CronTab('* * * 1,2,3 * ls -la')
    >>> foo.validate_month()
    '1 2 3'
    >>> foo = CronTab('* * * 2-11 * ls -la')
    >>> foo.validate_month()
    '2 3 4 5 6 7 8 9 10 11'
    >>> foo = CronTab('* * * 1-13 * ls -la')
    >>> foo.validate_month()

    validate_day_of_week()
    >>> foo = CronTab('* * * * 1 ls -la')
    >>> foo.validate_day_of_week()
    '1'
    >>> foo = CronTab('* * * * */2 ls -la')
    >>> foo.validate_day_of_week()
    '2 4 6'
    >>> foo = CronTab('* * * * * ls -la')
    >>> foo.validate_day_of_week()
    '1 2 3 4 5 6 7'
    >>> foo = CronTab('* * * * 1,2,3 ls -la')
    >>> foo.validate_day_of_week()
    '1 2 3'
    >>> foo = CronTab('* * * * 1-7 ls -la')
    >>> foo.validate_day_of_week()
    '1 2 3 4 5 6 7'
    >>> foo = CronTab('* * * * 1-8 ls -la')
    >>> foo.validate_day_of_week()
    """

def runexpand_tests():
    """
    # expand_range()
    >>> helpers.expand_range('1-3', 1, 7)
    '1 2 3'
    >>> helpers.expand_range('0-3', 1, 7)
    >>> helpers.expand_range('1-26', 0, 59)
    '1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26'
    >>> helpers.expand_range('0-7', 1, 7)
    >>> helpers.expand_range('1-8', 1, 7)
    >>> helpers.expand_range('0-8', 1, 7)
    >>> helpers.expand_range('0--1', 1, 7)
    >>> helpers.expand_range('0-6.9', 1, 7)

    # expand_div()
    >>> helpers.expand_div('*/4', 0, 23)
    '0 4 8 12 16 20'
    >>> helpers.expand_div('*/1', 1, 7)
    '1 2 3 4 5 6 7'
    >>> helpers.expand_div('1/3', 0, 367)
    ''
    >>> helpers.expand_div('*/27', 0, 23)
    ''
    >>> helpers.expand_div('*//2', 1, 23)
    ''
    >>> helpers.expand_div('*/2.5', 1, 23)
    ''
    >>> helpers.expand_div('*', 1, 7)
    ''

    # expand_list()
    >>> helpers.expand_list('1,2,3', 1, 7)
    '1 2 3'
    >>> helpers.expand_list('1,2,3,4,5,6,7', 1, 7)
    '1 2 3 4 5 6 7'
    >>> helpers.expand_list('1,2,3,4,5,6,7,8', 1, 7)
    >>> helpers.expand_list('1.2,3,4,5,6,7', 1, 7)
    >>> helpers.expand_list('1,2,3,4.5,6,7', 1, 7)

    # expand_all()
    >>> helpers.expand_all('*', 1, 7)
    '1 2 3 4 5 6 7'
    >>> helpers.expand_all('&', 1, 7)
    ''
    """
