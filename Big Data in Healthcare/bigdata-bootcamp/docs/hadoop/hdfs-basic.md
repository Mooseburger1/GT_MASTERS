---
---
# HDFS Basics

::: tip

- Being familiar with basic operations of HDFS.

:::

Hadoop comes with a distributed filesystem called **HDFS**, which stands for *Hadoop Distributed File System*. Although Hadoop supports many other filesystems (e.g., Amazon S3), HDFS is the most popular choice and will be used throughout this bootcamp. Therefore, in this section, you will learn how to move data between your local filesystem and HDFS.

## HDFS Operations

Hadoop provides a command line utility `hdfs` to interact with HDFS. Basic operations are placed under `hdfs dfs` subcommand. Let's play with some basic operations.

### Create home directory

When you use HDFS for the first time, it's likely that your home directory in HDFS has not been created yet. Your home directory in HDFS is `/user/<username>/` by default. In the environment that we provide, there's a special user `hdfs` who is an HDFS administrator and has the permission to create new home directories.

First, you will need to switch to the `hdfs` user via

``` bash
> sudo su - hdfs
```

Then, you can create a directory and change ownership of the newly created folder

``` bash
> hdfs dfs -mkdir -p /user/<username>
> hdfs dfs -chown <username> /user/<username>
```

Please remember to change `<username>` to your actual linux user name. Currently, the default user of our Docker image is `root`. Since it is a virtual environment, you don't need to worry about using `root` user and its permission. After you create the folder, switch back to your user with `exit`.

### Create directory

Similar to creating local directory via linux command `mkdir`, creating a folder named `input` in HDFS use

``` bash
> hdfs dfs -mkdir input
```

where `hdfs` is the HDFS utility program, `dfs` is the subcommand to handle basic HDFS operations,  `-mkdir` means you want to create a directory and the directory name is specified as `input`. Above commands actually create the `input` directory in your home directory in HDFS. Of course, you can create it to other place with absolute or relative path.

### Copy data in and out

Suppose you followed previous instructions and created an directory named `input`, you can then copy data from local file system to HDFS using `-put`. For example,

``` bash
> cd /bigdata-bootcamp/data
> hdfs dfs -put case.csv input
> hdfs dfs -put control.csv input
```

You can find detailed description about these two files in [sample data](/data.html).

Similar to `-put`, `-get` operation will copy data out of HDFS to the local folder. For example

``` bash
hdfs dfs -get input/case.csv local_case.csv
```

will copy the `input/case.csv` file out HDFS into the current working directory using a new name `local_case.csv`. If you didn't specify `local_case.csv`, the original name `case.csv` will be kept. You will be able to verify your copy by `-ls` and `-cat` operation described below.

### List File Information

Just like linux `ls` command, `-ls` is the operation to list files and folders in HDFS. For example, the following command list items in your home directory of HDFS (i.e `/user/<username>/`)

``` bash
> hdfs dfs -ls
Found 1 items
-rwxr-xr-x   - hadoop supergroup          0 2015-07-11 06:10 input
```

You can see the newly created `input` directory is listed. You can also see the files inside a particular directory

``` bash
>hdfs dfs -ls input
found 2 items
-rw-r--r--   1 hadoop supergroup     536404 2015-07-11 06:10 input/case.csv
-rw-r--r--   1 hadoop supergroup     672568 2015-07-11 06:08 input/control.csv
```

### Fetch file content

Actually you don't need to copy files out local in order to see its content, you can directly use `-cat` to printing the content of files in HDFS. For example, the following command print out content of the one file you just put into HDFS.

``` bash
> hdfs dfs -cat input/case.csv
...
020E860BD31CAC69,DRUG00440128228,976,60.0
020E860BD31CAC69,DIAG486,907,1.0
020E860BD31CAC69,DIAG7863,907,1.0
020E860BD31CAC69,DIAGV5866,907,1.0
020E860BD31CAC69,DIAG3659,907,1.0
020E860BD31CAC69,DIAGRG199,907,1.0
020E860BD31CAC69,PAYMENT,907,15000.0
020E860BD31CAC69,heartfailure,956,1.0
...
```

You will find wildcard character very useful since output of MapReduce and other Hadoop-based tools tendsto be directory. For example, to print content of all csv files (the case.csv and control.csv) in the `input` HDFS folder, you can

``` bash
hdfs dfs -cat input/*.csv
```

### Further reading

For more detailed usage of different commands and parameters, you can type

``` bash
hdfs dfs -help
```

<ExerciseComponent
    question="Remove what you just created (hint: similar to the Linux command)"
    answer="">

``` bash
hdfs dfs -rm -r input
```

You may miss the `-r` option and get error. `-r` tells HDFS to remove recursively. This is similar to linux command `rm`.

</ExerciseComponent>
