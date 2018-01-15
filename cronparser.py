# -*- coding: utf-8 -*-
#!/usr/local/bin/python2
"""
This module demonstrates a minimal functional command line tool for parsing
crontab-style strings and pretty-printing their contents in an easy-to-read
format that explains exactly when the cron will run.

Example:

        $ ./cronparser.py */15 0 1,15 * 1-5 /usr/bin/find
        minute        0 15 30 45
        hour          0
        day of month  1 15
        month         1 2 3 4 5 6 7 8 9 10 11 12
        day of week   1 2 3 4 5
        command       /usr/bin/find
"""

class CronTab(object):
    """
    CronTab object holds each field of a crontab line, or fails to be created
    Attributes:
        * minute
        * hour
        * day_of_month
        * month
        * day_of_week
        * command
    """
    def __init__(self, crontab):
        """
        CronTab constructor expects a newline-delimited string to parse
        (str) -> CronTab
        >>> foo = CronTab('1 2 3 4 5 ls -la')
        >>> foo = CronTab('1 2 3 4 5')
        ERROR: not enough fields in the crontab
        """

        # split along whitespace into 6 fields, last field as long as needed
        try:
            split = crontab.split(None, 5)
            self.minute = split[0]
            self.hour = split[1]
            self.day_of_month = split[2]
            self.month = split[3]
            self.day_of_week = split[4]
            self.command = split[5]
        except IndexError:
            print 'ERROR: not enough fields in the crontab'

    def __str__(self):
        """
        (self) -> str
        Print CronTab object as a neat table, second field in the 14th column
        >>> foo = CronTab('1 2 3 4 5 ls -la')
        >>> print foo
        minute        1
        hour          2
        day of month  3
        month         4
        day of week   5
        command       ls -la
        """
        ret_string = ''
        ret_string += 'minute %8s\n' % (self.minute)
        ret_string += 'hour %10s\n' % (self.hour)
        ret_string += 'day of month %2s\n' % (self.day_of_month)
        ret_string += 'month %9s\n' % (self.month)
        ret_string += 'day of week %3s\n' % (self.day_of_week)
        ret_string += 'command %12s' % (self.command)

        return ret_string

def validate_fields(cron):
    """
    (str) -> bool
    apply a regex to the input string and verify that it's valid cron syntax
    """
    cron.isinstance(cron, basestring)

if '__name__' == '__main__':
    import doctest
    doctest.testmod()
