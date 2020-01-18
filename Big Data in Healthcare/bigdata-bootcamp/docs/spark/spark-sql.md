---
---
# Spark Sql

::: tip Learning Objectives

- Load data into Spark SQL as DataFrame.
- Manipulate data with built-in functions.
- Define a User Defined Function (UDF).

:::

## Overview

Recent versions of Spark released the programming abstraction named `DataFrame`, which can be regarded as a table in a relational database. `DataFrame` is stored in a distributed manner so that different rows may locate on different machines. On `DataFrame` you can write `sql` queries, manipulate columns programatically with API etc.

## Loading data

Spark provides an API to load data from JSON, Parquet, Hive table etc. You can refer to the official [Spark SQL programming guide](https://spark.apache.org/docs/latest/sql-programming-guide.html#data-sources) for those formats. Here we show how to load csv files. And we will use the [spark-csv](https://github.com/databricks/spark-csv) module by Databricks.

Start the Spark shell in local mode with the command below to add extra dependencies which are needed to complete this training.

```bash
% spark-shell --master "local[2]" --driver-memory 3G --packages com.databricks:spark-csv_2.11:1.5.0
[logs]

Spark context available as sc.
15/05/04 13:12:57 INFO SparkILoop: Created sql context (with Hive support)..
SQL context available as sqlContext.

scala>
```

::: tip

Spark 2.0+ has built-in csv library now. This parameter is not required any more, and it is only used as a sample.

:::


::: tip

You may want to hide the log messages from spark. You can achieve that by

``` scala
import org.apache.log4j.Logger
import org.apache.log4j.Level
Logger.getRootLogger.setLevel(Level.ERROR)
```

:::


Now load data into the shell.

```scala
scala> val sqlContext = spark.sqlContext
sqlContext: org.apache.spark.sql.SQLContext = org.apache.spark.sql.SQLContext@5cef5fc9

scala> val patientEvents = sqlContext.load("input/", "com.databricks.spark.csv").
     toDF("patientId", "eventId", "date", "rawvalue").
     withColumn("value", 'rawvalue.cast("Double"))
patientEvents: org.apache.spark.sql.DataFrame = [patientId: string, eventId: string, date: string, rawvalue: string, value: double]
```

The first parameter is path to the data (in HDFS), and second is a class name, the specific adapter required to load a CSV file. Here we specified a directory name instead of a specific file name so that all files in that directory will be read and combined into one file. Next we call `toDF` to rename the columns in the CSV file with meaningful names. Finally, we add one more column that has double type of value instead of string which we will use ourselves for the rest of this material.

## Manipulating data

There are two methods to work with the DataFrame, either using SQL or using domain specific language (DSL). 

### SQL

Writing SQL is straightforward assuming you have experiences with relational databases.

```scala
scala> patientEvents.registerTempTable("events")
scala> sqlContext.sql("select patientId, eventId, count(*) count from events where eventId like 'DIAG%' group by patientId, eventId order by count desc").collect
res5: Array[org.apache.spark.sql.Row] = Array(...)
```

Here the `patientEvents` DataFrame is registered as a table in sql context so that we could run sql commands. Next line is a standard sql command with `where`, `group by` and `order by` statements.

### DSL

Next, we show how to manipulate data with DSL, the same result of previous SQL command can be achieved by:

```scala
scala> patientEvents.filter($"eventId".startsWith("DIAG")).groupBy("patientId", "eventId").count.orderBy($"count".desc).show
patientId        eventId   count
00291F39917544B1 DIAG28521 16   
00291F39917544B1 DIAG58881 16   
00291F39917544B1 DIAG2809  13   
00824B6D595BAFB8 DIAG4019  11   
0085B4F55FFA358D DIAG28521 9    
6A8F2B98C1F6F5DA DIAG58881 8    
019E4729585EF3DD DIAG4019  8    
0124E58C3460D3F8 DIAG4019  8    
2D5D3D5F03C8C176 DIAG4019  8    
01A999551906C787 DIAG4019  7    
...
```

For complete DSL functions, see [DataFrame](http://spark.apache.org/docs/latest/api/scala/index.html#org.apache.spark.sql.DataFrame) class API.

## Saving data

Spark SQL provides a convenient way to save data in a different format just like loading data. For example you can write 

```scala
scala> patientEvents.
    filter($"eventId".startsWith("DIAG")).
    groupBy("patientId", "eventId").
    count.
    orderBy($"count".desc).
    write.json("aggregated.json")
```

to save your transformed data in `json` format or

```scala
scala> patientEvents.
    filter($"eventId".startsWith("DIAG")).
    groupBy("patientId", "eventId").count.
    orderBy($"count".desc).
    write.format("com.databricks.spark.csv").save("aggregated.csv")
```

to save  in `csv` format.

## UDF

In many cases the built-in function of SQL like `count`, `max` is not enough, you can extend it with your own functions. For example, you want to _find_ the number of different event types with the following UDF.

### Define

Define and register an UDF

```scala
scala> sqlContext.udf.register("getEventType", (s: String) => s match {
    case diagnostics if diagnostics.startsWith("DIAG") => "diagnostics"
    case "PAYMENT" => "payment"
    case drug if drug.startsWith("DRUG") => "drug"
    case procedure if procedure.startsWith("PROC") => "procedure"
    case "heartfailure" => "heart failure"
    case _ => "unknown"
    })
```

### Use

Write sql and call your UDF

```scala
scala> sqlContext.sql("select getEventType(eventId) type, count(*) count from events group by getEventType(eventId) order by count desc").show
type          count
drug          16251
diagnostics   10820
payment       3259
procedure     514
heart failure 300
```

<ExerciseComponent
    question="Find top 10 patients with highest total payment using both SQL and DSL."
    answer="">

- SQL

```scala
scala> sqlContext.sql("select patientId, sum(value) as payment from events where eventId = 'PAYMENT' group by patientId order by payment desc limit 10").show

patientId        payment
0085B4F55FFA358D 139880.0
019E4729585EF3DD 108980.0
01AC552BE839AB2B 108530.0
0103899F68F866F0 101710.0
00291F39917544B1 99270.0
01A999551906C787 84730.0
01BE015FAF3D32D1 83290.0
002AB71D3224BE66 79850.0
51A115C3BD10C42B 76110.0
01546ADB01630C6C 68190.0
```

- DSL

```scala
scala> patientEvents.filter(patientEvents("eventId") === "PAYMENT").groupBy("patientId").agg("value" -> "sum").withColumnRenamed("sum(value)", "payment").orderBy($"payment".desc).show(10)

patientId        payment
0085B4F55FFA358D 139880.0
019E4729585EF3DD 108980.0
01AC552BE839AB2B 108530.0
0103899F68F866F0 101710.0
00291F39917544B1 99270.0
01A999551906C787 84730.0
01BE015FAF3D32D1 83290.0
002AB71D3224BE66 79850.0
51A115C3BD10C42B 76110.0
01546ADB01630C6C 68190.0
```

</ExerciseComponent>
