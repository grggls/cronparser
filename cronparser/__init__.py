# -*- coding: utf-8 -*-
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

from . import helpers

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
        """

        # split along whitespace into 6 fields, last field as long as needed
        try:
            split = crontab.split(None, 5)

            self.minute = split[0]
            if self.validate_minute():
                self.hour = split[1]
                if self.validate_hour():
                    self.day_of_month = split[2]
                    if self.validate_day_of_month():
                        self.month = split[3]
                        if self.validate_month():
                            self.day_of_week = split[4]
                            if self.validate_day_of_week():
                                self.command = split[5]
        except IndexError:
            print 'ERROR: not enough fields in the crontab'

    def __str__(self):
        """
        (self) -> str
        Print CronTab object as a neat table, second field in the 14th column
        """
        ret_string = ''
        ret_string += '%-14s%s\n' % ('minute', self.minute)
        ret_string += '%-14s%s\n' % ('hour', self.hour)
        ret_string += '%-14s%s\n' % ('day of month', self.day_of_month)
        ret_string += '%-14s%s\n' % ('month', self.month)
        ret_string += '%-14s%s\n' % ('day of week', self.day_of_week)
        ret_string += '%-14s%s' % ('command', self.command)

        return ret_string

    def validate_minute(self):
        """
        (self) -> str
        Take the 'minute' field of the crontab and validate, then expand to the
        number of times the cron will run, e.g. '*/15' expands to '0 15 30 45'
        Return the string it expands to or None
        """
        if self.minute:
            if self.minute.find('-') >= 0:
                self.minute = helpers.expand_range(self.minute, 0, 59)
            elif self.minute.find('/') >= 0:
                self.minute = helpers.expand_div(self.minute, 0, 59)
            elif self.minute.find(',') >= 0:
                self.minute = helpers.expand_list(self.minute, 0, 59)
            elif self.minute.find('*') >= 0:
                self.minute = helpers.expand_all(self.minute, 0, 59)

        # check our methods didn't return None (indicative of err)
        return self.minute if self.minute else None

    def validate_hour(self):
        """
        (self) -> str
        Take the 'hour' field of the crontab and validate, then expand to when
        the cron will run, e.g. '*/4' expands to '0 4 8 12 16 20 24'
        Return the string it expands to or None
        """
        if self.hour:
            if self.hour.find('-') >= 0:
                self.hour = helpers.expand_range(self.hour, 0, 23)
            elif self.hour.find('/') >= 0:
                self.hour = helpers.expand_div(self.hour, 0, 23)
            elif self.hour.find(',') >= 0:
                self.hour = helpers.expand_list(self.hour, 0, 23)
            elif self.hour.find('*') >= 0:
                self.hour = helpers.expand_all(self.hour, 0, 23)

        # check our methods didn't return None (indicative of err)
        return self.hour if self.hour else None

    def validate_day_of_month(self):
        """
        (self) -> bool
        Take the 'day of month' field of the crontab and validate, then expand
        to when cron will run, e.g. '*' expands to '0 1 2 3 ... 31', shoud  use
        the months to determine max days in the month but running out of time
        Return the string it expands to or None
        """
        if self.day_of_month:
            if self.day_of_month.find('-') >= 0:
                self.day_of_month = helpers.expand_range(self.day_of_month, 0, 31)
            elif self.day_of_month.find('/') >= 0:
                self.day_of_month = helpers.expand_div(self.day_of_month, 0, 31)
            elif self.day_of_month.find(',') >= 0:
                self.day_of_month = helpers.expand_list(self.day_of_month, 0, 31)
            elif self.day_of_month.find('*') >= 0:
                self.day_of_month = helpers.expand_all(self.day_of_month, 0, 31)

        # check our methods didn't return None (indicative of err)
        return self.day_of_month if self.day_of_month else None

    def validate_month(self):
        """
        (self) -> None
        Take the 'month' field of the crontab and validate, then expand
        to when cron will run, e.g. '*' expands to '0 1 2 3 ... 12'
        Return the string it expands to or None
        """
        if self.month:
            if self.month.find('-') >= 0:
                self.month = helpers.expand_range(self.month, 1, 12)
            elif self.month.find('/') >= 0:
                self.month = helpers.expand_div(self.month, 1, 12)
            elif self.month.find(',') >= 0:
                self.month = helpers.expand_list(self.month, 1, 12)
            elif self.month.find('*') >= 0:
                self.month = helpers.expand_all(self.month, 1, 12)
            else:
                pass

        # check our methods didn't return None (indicative of err)
        return self.month if self.month else None

    def validate_day_of_week(self):
        """
        (self) -> bool
        Take the 'day of week' field of the crontab and validate, then expand
        to when cron will run, e.g. '*' expands to '0 1 2 3 4 5 6 7'
        Return the string it expands to or None
        """
        if self.day_of_week:
            if self.day_of_week.find('-') >= 0:
                self.day_of_week = helpers.expand_range(self.day_of_week, 1, 7)
            elif self.day_of_week.find(',') >= 0:
                self.day_of_week = helpers.expand_list(self.day_of_week, 1, 7)
            elif self.day_of_week.find('/') >= 0:
                self.day_of_week = helpers.expand_div(self.day_of_week, 1, 7)
            elif self.day_of_week.find('*') >= 0:
                self.day_of_week = helpers.expand_all(self.day_of_week, 1, 7)
            else:
                pass

        # check our methods didn't return None (indicative of err)
        return self.day_of_week if self.day_of_week else None


if __name__ == '__main__':
    # grab cmd args, drop the name of the script, create CronTab, print
    import sys
    print CronTab(' '.join(sys.argv[1:]))
