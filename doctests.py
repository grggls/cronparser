import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from cronparser import CronTab as CronTab

if __name__ == '__main__':
    import doctest
    run_doctests()

def run_doctests():
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
