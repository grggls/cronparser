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

        *** somehow all our tests and validation work down below, but when we
            pass * to the 'month' field we don't expand it. probably a simple
            logic error but running out of time here.
        """

        # split along whitespace into 6 fields, last field as long as needed
        try:
            split = crontab.split(None, 5)

            # the 'validate_*' methods are pretty gross, in that they change
            # object attributes, then return a bool. also causing this nesting
            # nightmare. But it works!
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
        (self) -> bool
        Take the 'minute' field of the crontab and validate, then expand to the
        number of times the cron will run, e.g. '*/15' expands to '0 15 30 45'
        """
        if self.minute:
            if self.minute.find('-') >= 0:
                self.minute = self._expand_range(self.minute, 0, 59)
            elif self.minute.find('/') >= 0:
                self.minute = self._expand_div(self.minute, 0, 59)
            elif self.minute.find(',') >= 0:
                self.minute = self._expand_list(self.minute, 0, 59)
            elif self.minute.find('*') >= 0:
                self.minute = self._expand_all(self.minute, 0, 59)

        # check our methods didn't return None (indicative of err)
        return True if self.minute else False

    def validate_hour(self):
        """
        (self) -> None
        Take the 'hour' field of the crontab and validate, then expand to when
        the cron will run, e.g. '*/4' expands to '0 4 8 12 16 20 24'
        """
        if self.hour:
            if self.hour.find('-') >= 0:
                self.hour = self._expand_range(self.hour, 0, 23)
            elif self.hour.find('/') >= 0:
                self.hour = self._expand_div(self.hour, 0, 23)
            elif self.hour.find(',') >= 0:
                self.hour = self._expand_list(self.hour, 0, 23)
            elif self.hour.find('*') >= 0:
                self.hour = self._expand_all(self.hour, 0, 23)

        # check our methods didn't return None (indicative of err)
        return True if self.hour else False

    def validate_day_of_month(self):
        """
        (self) -> bool
        Take the 'day of month' field of the crontab and validate, then expand
        to when cron will run, e.g. '*' expands to '0 1 2 3 ... 31', shoud  use
        the months to determine max days in the month but running out of time
        """
        if self.day_of_month:
            if self.day_of_month.find('-') >= 0:
                self.day_of_month = self._expand_range(self.day_of_month, 0, 31)
            elif self.day_of_month.find('/') >= 0:
                self.day_of_month = self._expand_div(self.day_of_month, 0, 31)
            elif self.day_of_month.find(',') >= 0:
                self.day_of_month = self._expand_list(self.day_of_month, 0, 31)
            elif self.day_of_month.find('*') >= 0:
                self.day_of_month = self._expand_all(self.day_of_month, 0, 31)

        # check our methods didn't return None (indicative of err)
        return True if self.day_of_month else False

    def validate_month(self):
        """
        (self) -> None
        Take the 'month' field of the crontab and validate, then expand
        to when cron will run, e.g. '*' expands to '0 1 2 3 ... 12'
        """
        if self.month:
            if self.month.find('-') >= 0:
                self.month = self._expand_range(self.month, 1, 12)
            elif self.month.find('/') >= 0:
                self.month = self._expand_div(self.month, 1, 12)
            elif self.month.find(',') >= 0:
                self.month = self._expand_list(self.month, 1, 12)
            elif self.month.find('*') >= 0:
                self.month = self._expand_all(self.month, 1, 12)
            else:
                pass

        # check our methods didn't return None (indicative of err)
        return True if self.month else False

    def validate_day_of_week(self):
        """
        (self) -> bool
        Take the 'day of week' field of the crontab and validate, then expand
        to when cron will run, e.g. '*' expands to '0 1 2 3 4 5 6 7'
        """
        if self.day_of_week:
            if self.day_of_week.find('-') >= 0:
                self.day_of_week = self._expand_range(self.day_of_week, 1, 7)
            elif self.day_of_week.find(',') >= 0:
                self.day_of_week = self._expand_list(self.day_of_week, 1, 7)
            elif self.day_of_week.find('/') >= 0:
                self.day_of_week = self._expand_div(self.day_of_week, 1, 7)
            elif self.day_of_week.find('*') >= 0:
                self.day_of_week = self._expand_all(self.day_of_week, 1, 7)
            else:
                pass

        # check our methods didn't return None (indicative of err)
        return True if self.day_of_week else False

    def _expand_range(self, range_string, range_min, range_max):
        """
        (str, int, int) -> str
        Given a 'day of week' cron field like '1-3', call this method like so:
        CronTab._expand_range('1-3', 1, 7), where the two integer fields are the
        upper and lower bounds of the cron range

        Validate this is valid input (e.g. '0-8' is not valid day of week range)

        Retun a None to indicate an out of range error to the caller
        """

        ranges = range_string.split('-')
        try:
            lower = int(ranges[0])
            upper = int(ranges[1])
        except ValueError:
            return None

        ret_string = ''

        if lower >= range_min:
            if upper <= range_max:
                ret_range = range(lower, upper + 1)
                for member in ret_range:
                    ret_string += str(member)
                    ret_string += ' '
                return ret_string.strip()

        return None

    def _expand_div(self, div_string, range_min, range_max):
        """
        (str, int, int) -> str
        Given an 'hour' cron field like '*/4', call this method like so:
        CronTab._expand_div('*/4', 0, 23), where the integer attributes are the
        upper and lower bounds for that cron field.

        Validate that this is valid input (e.g. */27 is not valid for hours)

        Return None to indicate an out of range error to the caller
        """

        ret_string = ''
        divs = div_string.split('/')

        # must start with a *
        if divs[0] != '*':
            return ret_string

        # divisor must be an int, catches cases that don't use '/' correctly
        try:
            div = int(divs[1])
        except ValueError:
            return ret_string
        except IndexError:
            # non-range input like '*'
            return ret_string

        # check that our divisor is inside min and max specified
        if div < range_min:
            return ret_string
        if div > range_max:
            return ret_string

        # iterate through min to max and create ret_string
        for time_slice in range(range_min, range_max+1):
            if time_slice % div == 0:
                ret_string += str(time_slice) + ' '

        return ret_string.strip()

    def _expand_list(self, list_string, range_min, range_max):
        """
        (str, int, int) -> str
        Verify that 'list_string' conforms to '1,2,3' syntax, expand to white-
        space delimited list (no commas).

        Return None to indicate any error to the caller
        """
        ret_string = ''
        list_items = list_string.split(',')

        for item in list_items:
            try:
                # cast to int, check range, cast back to string and append
                item_int = int(item)
                if item_int < range_min or item_int > range_max:
                    return None

                ret_string += str(item_int) + ' '
            except (TypeError, ValueError):
                return None

        return ret_string.strip()

    def _expand_all(self, all_string, range_min, range_max):
        """
        (str, int, int) -> str
        Verify that 'all_string' is '*' and then enumerate min to max

        Hopefully requires much less error checking than the previous two methods

        Return None to indicate an out of range error to the caller
        """
        ret_string = ''

        if all_string == '*':
            for time_slice in range(range_min, range_max+1):
                ret_string += str(time_slice) + ' '

        return ret_string.strip()


if __name__ == '__main__':
    # grab cmd args, drop the name of the script, create CronTab, print
    import sys
    args = sys.argv
    cron = ' '.join(args[1:])
    cron = CronTab(cron)
    print cron
