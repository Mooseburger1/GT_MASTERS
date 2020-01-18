---
---
# Hadoop Streaming

::: tip

- Learn how to work with Hadoop Streaming.
- Learn how to write Hadoop Streaming programs using python.

:::

In this section, you will learn how to work with Hadoop Streaming, a tool to run any executable in Hadoop MapReduce. We will show how to count the frequency of different values of `event-id` for each patient [event sequence file](/data.html). The examples here are shown in Python code, but you will find that it's straightforward to adapt this concept to other languages.

## Mapper and Reducer

Streaming works by passing a data mapper and reducer written in another programming language through standard input and output. Let's have a look at the source code[^1] for the mapper and reducer one at at time.

### Mapper

The source code for the mapper is:

```python
#!/usr/bin/env python

import sys

for line in sys.stdin:
    line        = line.strip()
    splits      = line.split(',')

    if len(splits) != 4:
        # ignore problemactic line
        continue

    # unwind the splits
    patient_id, event_name, date_offset, value = splits

    # emit key-value pair seperated by \t for all events
    print(event_name + '\\' + '1')
```

This script reads lines from standard input and with some simple processing outputs to standard output the `event_name` as the key and `1` as the value.

### Reducer

The reducer is a little bit more complex. The output of the mapper will be shuffled by Hadoop framework's shuffle process (a part of MapReduce) and the reducer will get a list of key-value pairs. The MapReduce framework guarantees that all key-value pairs with the same key will go to same reducer instance.

The source code for the reducer is:

```python
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

## do not forget to output the last event_name if needed!
if current_event == event_name:
    print('%s\t%s' % (current_event, current_count))
```

This script checks the boundaries of the sorted input and sums up values from same key.

## How to run

### Local test

Before running it in Hadoop, it's more convenient to test the code in shell using the `cat` and `sort` commands. You will need to navigate to the _sample/hadoop-streaming_ folder. Then, run the below command in the shell:

```bash
cat data/* | python mapper.py | sort | python reducer.py                       
```

You will see results like:

```
DIAG0043        1
DIAG00845       8
DIAG0086        1
DIAG0088        4
DIAG01190       1
DIAG0201        1
DIAG0202        1
DIAG0204        1
DIAG0221        1
DIAG0232        1
...
```

Now that we've verified that it works as expected, we can run it in Hadoop.

### Hadoop

We first need to put the data into HDFS, then run hadoop:

```bash
hdfs dfs -mkdir streaming-data
hdfs dfs -put data/* streaming-data
hadoop jar hadoop-streaming.jar \
   -files mapper.py,reducer.py \
   -mapper "python mapper.py" \
   -reducer "python reducer.py" \
   -input streaming-data \
   -output streaming-output
```

Now we check the results and clean up:

```bash
## check result
hdfs dfs -ls streaming-output
hdfs dfs -cat streaming-output/*

## clean up
hdfs dfs -rm -r streaming-output
hdfs dfs -rm -r streaming-data
```

<ExerciseComponent
    question="Update mapper and reducer to output diagnostic code occurred more than once"
    answer="">

You will need to update both the mapper and reducer, for the mapper:

```python
## emit key-value pair seperated by \t for all diagnostic code
if event_name.startswith('DIAG'):
    print(event_name + '\\' + '1')
```

and the reducer looks like:

```python
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
        if current_event and current_count > 1:
            # write result to STDOUT
            print('%s\t%s' % (current_event, current_count))
        current_count = count
        current_event = event_name

## do not forget to output the last event_name if needed!
if current_event == event_name and current_count > 1:
    print('%s\t%s' % (current_event, current_count))

```

</ExerciseComponent>

## Further reading

Streaming is a good machanism to reuse existing code. Wrapping existing code to work with Hadoop can be simplified with framework like [mrjob](https://github.com/Yelp/mrjob) and [Luigi](http://luigi.readthedocs.org/en/latest/index.html) for Python. You can find more explanation and description of Streaming in its [offical documentation](http://hadoop.apache.org/docs/r1.2.1/streaming.html).

[^1]: this example is adapted from [Michael G. Noll's blog](http://www.michael-noll.com/tutorials/writing-an-hadoop-mapreduce-program-in-python/), copyright to original author.
