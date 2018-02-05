def expand_range(range_string, range_min, range_max):
    """
    (str, int, int) -> str
    Given a 'day of week' cron field like '1-3', call this method like so:
    CronTab.expand_range('1-3', 1, 7), where the two integer fields are the
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

def expand_div(div_string, range_min, range_max):
    """
    (str, int, int) -> str
    Given an 'hour' cron field like '*/4', call this method like so:
    CronTab.expand_div('*/4', 0, 23), where the integer attributes are the
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

def expand_list(list_string, range_min, range_max):
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

def expand_all(all_string, range_min, range_max):
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
