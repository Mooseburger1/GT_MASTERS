---
layout: post
title: Overview of Hadoop
categories: [section]
navigation:
  section: [1, 0]
---

{% objective %}
- To learn basic HDFS operations and be able to move data between the local filesyste and HDFS.
- To be able to write basic MapReduce programs.
- To get to know commonly used tools in the Hadoop ecosystem.
{% endobjective %}

[Hadoop](http://hadoop.apache.org) is a framework for distributed storage and processing of very large data sets on computer clusters built from commodity hardware. It's mainly composed of two parts: data storage and data processing. The distributed storage part is handled by the Hadoop Distributed File System (HDFS). The distributed processing part is achieved via MapReduce. Many powerful tools have being developed on top of the HDFS and MapReduce foundation. In this module you will learn the basics of HDFS and MapReduce, as well as more advanced Hadoop tools such as HBase, Pig and Hive. 
![hadoop-ecosystem]({{ site.baseurl }}/image/post/hadoop-ecosystem.jpg "Hadoop Tools to Cover")
This chapter is divided into the following sections

1. **[HDFS Basics]({{ site.baseurl }}/hdfs-basic/)**: You will learn the basic HDFS operations, including copy data into/out of HDFS, listing the files in HDFS, deleting files in HDFS, etc.

1. **[MapReduce Basics]({{ site.baseurl }}/mapreduce-basic/)**: You will learn how to write a basic MapReduce program in Java to count distinct diagnostic code in order to compute the prevalence of diseases in the given dataset.

2. **[Apache HBase]({{ site.baseurl }}/hadoop-hbase/)**: HBase is a powerful distributed NoSQL database inspired by Google BigTable. HBase provides SQL-like syntax to query big data. You will learn typical create, retrieve, update, delete (CRUD) operations.

3. **[Hadoop Streaming]({{ site.baseurl }}/hadoop-streaming)**: Hadoop streaming provides the mechanism to write MapReduce programs in any programming language. In this section, you will learn how to do the same count task done previously, but this time using Hadoop streaming to code the mapper and reducer in python.

4. **[Apache Pig]({{ site.baseurl }}/hadoop-pig)**: Apache Pig is a procedural language to manipulate data using Hadoop. You will learn 'Pig Latin', the syntax/grammar of Pig. The Pig system will processing pig latin scripts by translating them into low-level (often more cumbersome) MapReduce Java programs.

5. **[Apache Hive]({{ site.baseurl }}/hadoop-hive)**: Apace Hive provides SQL-like syntax to query data stored in HDFS, HBase, etc. Again like Pig, Hive will convert the high-level HiveQL into low-level MapReduce programs. You will learn how to create tables and do a simple querys using Hive.


