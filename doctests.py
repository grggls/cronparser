import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from cronparser import CronTab as CronTab

if __name__ == '__main__':
    import doctest
    run_CronTab_tests()

def run_CronTab_tests():
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
    True
    >>> foo = CronTab('*/5 * * * * ls -la')
    >>> foo.validate_minute()
    True
    >>> foo = CronTab('* * * * * ls -la')
    >>> foo.validate_minute()
    True
    >>> foo = CronTab('1,2,3 * * * * ls -la')
    >>> foo.validate_minute()
    True
    >>> foo = CronTab('1-59 * * * * ls -la')
    >>> foo.validate_minute()
    True
    >>> foo = CronTab('1-60 * * * * ls -la')
    >>> foo.validate_minute()
    False
        
    # validate_hour() tests
    >>> foo = CronTab('* 0 * * * ls -la')
    >>> foo.validate_hour()
    True
    >>> foo = CronTab('* */5 * * * ls -la')
    >>> foo.validate_hour()
    True
    >>> foo = CronTab('* * * * * ls -la')
    >>> foo.validate_hour()
    True
    >>> foo = CronTab('* 1,2,3 * * * ls -la')
    >>> foo.validate_hour()
    True
    >>> foo = CronTab('* 1-23 * * * ls -la')
    >>> foo.validate_hour()
    True
    >>> foo = CronTab('* 1-24 * * * ls -la')
    >>> foo.validate_hour()
    False
        
    # validate_day_of_month()
    >>> foo = CronTab('* * 0 * * ls -la')
    >>> foo.validate_day_of_month()
    True
    >>> foo = CronTab('* * */5 * * ls -la')
    >>> foo.validate_day_of_month()
    True
    >>> foo = CronTab('* * * * * ls -la')
    >>> foo.validate_day_of_month()
    True
    >>> foo = CronTab('* * 1,2,3 * * ls -la')
    >>> foo.validate_day_of_month()
    True
    >>> foo = CronTab('* * 1-23 * * ls -la')
    >>> foo.validate_day_of_month()
    True
    >>> foo = CronTab('* * 1-32 * * ls -la')
    >>> foo.validate_day_of_month()
    False

    # validate_month()
    >>> foo = CronTab('* * * 1 * ls -la')
    >>> foo.validate_month()
    True
    >>> foo = CronTab('* * * */2 * ls -la')
    >>> foo.validate_month()
    True
    >>> foo = CronTab('* * * * * ls -la')
    >>> foo.validate_month()
    True
    >>> foo = CronTab('* * * 1,2,3 * ls -la')
    >>> foo.validate_month()
    True
    >>> foo = CronTab('* * * 1-12 * ls -la')
    >>> foo.validate_month()
    True
    >>> foo = CronTab('* * * 1-13 * ls -la')
    >>> foo.validate_month()
    False

    validate_day_of_week()
    >>> foo = CronTab('* * * * 1 ls -la')
    >>> foo.validate_day_of_week()
    True
    >>> foo = CronTab('* * * * */2 ls -la')
    >>> foo.validate_day_of_week()
    True
    >>> foo = CronTab('* * * * * ls -la')
    >>> foo.validate_day_of_week()
    True
    >>> foo = CronTab('* * * * 1,2,3 ls -la')
    >>> foo.validate_day_of_week()
    True
    >>> foo = CronTab('* * * * 1-7 ls -la')
    >>> foo.validate_day_of_week()
    True
    >>> foo = CronTab('* * * * 1-8 ls -la')
    >>> foo.validate_day_of_week()
    False
