# Cron Parser
A command line application written in python which parses a cron string and expands each field to show the times at which it will run, written in python. Doctests/unittests included.

Time boxing this exercise to three hours of development time. Doesn't handle all possible cron strings. Considering only the standard cron format with five time fields (minute, hour, day of month, month, and day of week) plus a command. Not handling the special time strings such as "@yearly". Also not accepting text input like "JAN" or "WED". The input will be on a single line. All fields are mandatory:

|| Index|| Field        ||Allowed Values||
| 0     |  minute       | 0-60, `*/,-`  |
| 1     |  hour         | 0-23, `*/,-`  |
| 2     |  day of month | 0-31, `*/,-`  |
| 3     |  month        | 1-12, `*/,-`  |
| 4     |  day of week  | 1-7,  `*/,-`  |
| 5     |  command      | N/A, no validation necessary |

Specific error checking should be added such that it's not possible to specify, for example the 31st of February.

Anything can be placed in the `command` field.  Is it possible to validate that it is a valid command, script, or program?

The cron string will be passed to the application as a single argument. The output will be formatted as a table with the field name taking the first 14 columns and the times as a space-separated list following it.

For example given the input argument:
```
*/15 0 1,15 * 1-5 /usr/bin/find
```

The output should be:
```
012345678901234567890
----------------------------------------
minute        0 15 30 45
hour          0
day of month  1 15
month         1 2 3 4 5 6 7 8 9 10 11 12
day of week   1 2 3 4 5
command       /usr/bin/find
```
