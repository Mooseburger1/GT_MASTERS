---
---
# Hadoop HBase

::: tip

- Know HBase interactive shell.
- Being able to conduct CRUD operations.

:::

Apache HBase is a distributed column-oriented database built on top of the Hadoop file system. Use HBase when you need random, realtime read/write access to your Big Data. It provides a convenient interactive shell as well as a Java API.

## Interactive Shell

You can start the HBase interactive shell using the command `hbase shell`. After entering this command, you will see the following output:

```bash
HBase Shell; enter 'help<RETURN>' for list of supported commands.
Type "exit<RETURN>" to leave the HBase Shell
Version 0.94.18, rb149f3f0d25c5cd2f195b39fe05d42507fdeabfc, Sat May 23 00:09:16 GMT 2015

hbase(main):001:0>
```

To exit the interactive shell, type `exit` or `<ctrl+c>`.

## Create

The syntax to create a table from an HBase shell is shown below.

```bash
create 'table name', 'column family'
```

Note that in the HBase data model columns are grouped into "column families", which must be defined up front during table creation. These column families are stored together on disk. Because of this HBase is consided a column-oriented data store.

Let's create a table called `hospital` with two column families: `id` and `value`.

```bash
hbase(main):002:0> create 'hospital', 'id', 'value'
```

And it will give you the following output.

```bash
0 row(s) in 1.9850 seconds

=> Hbase::Table - hospital
```

## Update

### List table(s)

```bash
hbase(main):003:0> list
TABLE
hospital
1 row(s) in 0.0180 seconds
```

### Describe and alter table

The `describe` command returns the description of the table. 

```bash
hbase(main):004:0> describe 'hospital'
'hospital', {NAME => 'id', DATA_BLOCK_ENCODING => 'NONE', BLOOMFILTER => 'NONE', REPLICATION_SCOPE => true
  '0', VERSIONS => '3', COMPRESSION => 'NONE', MIN_VERSIONS => '0', TTL => '2147483647', KEEP_DELETED_
 CELLS => 'false', BLOCKSIZE => '65536', IN_MEMORY => 'false', ENCODE_ON_DISK => 'true', BLOCKCACHE =>
  'true'}, {NAME => 'value', DATA_BLOCK_ENCODING => 'NONE', BLOOMFILTER => 'NONE', REPLICATION_SCOPE =
 > '0', VERSIONS => '3', COMPRESSION => 'NONE', MIN_VERSIONS => '0', TTL => '2147483647', KEEP_DELETED
 _CELLS => 'false', BLOCKSIZE => '65536', IN_MEMORY => 'false', ENCODE_ON_DISK => 'true', BLOCKCACHE =
 > 'true'}
1 row(s) in 0.0350 seconds
```

This shows some basic information for each column family. For example, the `id` column family has block size of 65536 and keeps at most 3 versions for each cell (distinguishable by timestamp).

We can alter the the table settings by using `alter`. But first we must disable the table.

```bash
hbase(main):005:0> disable 'hospital'
hbase(main):006:0> alter 'hospital', {NAME => 'id', VERSIONS => 5}
```

Don't forget to re-enable after changing the setting.

```bash
hbase(main):007:0> enable 'hospital'

```

### Put data

Using the `put` command, you can insert rows into a table. The syntax is as follows:

```bash
put 'table name', 'row key', 'colfamily:colname', 'value'
```

For example, let's put a patient-id record.

```bash
hbase(main):008:0> put 'hospital', 'row1', 'id:patient', 'patient-id-1'
0 row(s) in 0.0140 seconds
```

This puts the value `patient-id-1` in row `row1` and column `patient` (within the column family `id`).
Let's put some more records.

```bash
hbase(main):009:0> put 'hospital', 'row1', 'id:event', 'event-id-1'
hbase(main):010:0> put 'hospital', 'row1', 'value:value', '1'
hbase(main):011:0> put 'hospital', 'row2', 'id:event', 'event-id-2'
```

## Read

### Cluster status

To check the status of the cluster use the `status` command:

```bash
hbase(main):001:0> status
(may have some debug messages)
2 servers, 0 dead, 1.0000 average load
```

### Table data

Using the `scan` command, you can view the table data.

```bash
hbase(main):012:0> scan 'hospital'
ROW            COLUMN+CELL
 row1          column=id:event, timestamp=1436623001980, value=event-id-1
 row1          column=id:patient, timestamp=1436622532169, value=patient-id-1
 row1          column=value:value, timestamp=1436622642925, value=1
 row2          column=id:event, timestamp=1436623003694, value=event-id-2
2 row(s) in 0.0130 seconds
```

If you only want to know the number of rows in a table, you can use:

```bash
hbase(main):013:0> count 'hospital'
2 row(s) in 0.0130 seconds
```

The `get` command can be used to retrieve a single row of data at a time.

```bash
hbase(main):014:0> get 'hospital', 'row1' 
COLUMN                                   CELL
 id:event           timestamp=1436623001980, value=event-id-1
 id:patient         timestamp=1436622532169, value=patient-id-1
 value:value        timestamp=1436622642925, value=1
3 row(s) in 0.0270 seconds
```

To retrieve the data in a particular column within a row we can use the following syntax:

```bash
hbase(main):015:0> get 'hospital', 'row1', {COLUMN => 'id:patient'}
 id:patient       timestamp=1436622532169, value=patient-id-1
 1 row(s) in 0.9730 seconds
```

## Delete

### Delete cell

You can delete a specific cell in a table by using the `delete` command

```bash
hbase(main):016:0> delete 'hospital', 'row1', 'id:event'
0 row(s) in 0.0100 seconds
```

To delete all the cells in a row, use the `deleteall` command

```bash
hbase(main):017:0> deleteall 'hospital', 'row1'
0 row(s) in 0.0110 seconds
```

### Drop table

Using the `drop` command, you can delete a table. Before dropping a table, you must disable it.

```bash
hbase(main):018:0> disable 'hospital'
0 row(s) in 1.1000 seconds

hbase(main):019:0> drop 'hospital'
```
