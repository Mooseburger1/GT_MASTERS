#!/usr/bin/env python

import sys

current_event = None
current_count = 0
event_name = None

for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()

    # parse the input we got from mapper.py
    event_name, count = line.split('\t', 1)

    # convert count (currently a string) to int
    try:
        count = int(count)
    except ValueError:
        # count was not a number, so silently
        # ignore/discard this line
        continue

    # line is sorted with key (event name)
    if current_event == event_name:
        # same key accumulate
        current_count += count
    else:
        # a new key to work on
        if current_event:
            # write result to STDOUT
            print('%s\t%s' % (current_event, current_count))
        current_count = count
        current_event = event_name

# do not forget to output the last event_name if needed!
if current_event == event_name:
    print('%s\t%s' % (current_event, current_count))
