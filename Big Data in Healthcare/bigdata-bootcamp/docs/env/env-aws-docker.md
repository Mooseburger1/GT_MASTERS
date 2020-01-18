---
---
# Docker in AWS EC2

We developed a [Docker image](https://hub.docker.com/r/sunlab/bigdata/) which pre-installed all modules in this bootcamp. You can directly use it in your own environment if you have docker. This page describes how to launch an EC2 instance on AWS and run docker container within it.

## Launch an AWS EC2 instance

1.   Open the Amazon EC2 console at <https://console.aws.amazon.com/ec2/>
2.   From the Amazon EC2 console dashboard, click **AMIs** on left sidebar.
3.   Switch **Region** to *N. Virginia* if you are in other regions.
4.   Choose *Public Images* in dropdown below launch and search for `ami-59d4f433`.
5. Select the image and click the blue _Launch_ button.
6. On the **Choose an Instance Type** page, select the hardware configuration and size of the instance to launch.
Choose the type _m4.xlarge_, with 4 vCPUs and 16GB memory, then click “Next: Configuration Instance Details”.
7. On the **Configure Instance Details** page, just keep the default settings.
8.  On the **Add Storage** page, you can specify storage size for your disk. Use the default 30GB.
9. On the **Tag Instance** page, specify tags for your instance by providing key value combinations if you need.
10.  On the **Configure Security Group** page, define firewall rules for your instance. We suggest you'd better keep the default setting unless you are sure what you are doing.
11. On the **Review Instance Launch** page, check the details of your instance and click _Launch_.
12. In the **Select an existing key pair or create a new key pair** dialog box. If you don’t have an existing key pair, choose **create a new key pair**. Enter a name for the key pair (e.g. bdhKeyPair) and click “Download Key Pair”. This key pair will be used to connect to your instance. Then on the same dialog box, choose Choose an existing key pair, and select the one you just created. 
13.  Finally, click “Launch Instances”. You can view your instances by clicking **Instances** on the left navigation bar. 

## Connect to the instance

After your instance is fully launched, you can connect to it using SSH client. Right click on the instance and click **connect** then AWS will show you instructions about connecting on various platform. `ssh` command will be used for `*nix` platform and Putty will be used for windows.

## Start a docker container

A pre-configured container with all necessary module installed is available for you to directly use. Navigate to `~/lab/docker` and `vagrant up` will launch a container like below

```bash
Last login: Mon Jan 25 03:29:38 2016 from lawn-128-61-36-142.lawn.gatech.edu

       __|  __|_  )
       _|  (     /   Amazon Linux AMI
      ___|\___|___|

https://aws.amazon.com/amazon-linux-ami/2015.09-release-notes/
20 package(s) needed for security, out of 38 available
Run "sudo yum update" to apply all updates.
[ec2-user@ip-172-31-23-158 ~]$ cd lab/docker/
[ec2-user@ip-172-31-23-158 docker]$ vagrant up
Bringing machine 'bootcamp1' up with 'docker' provider...
==> bootcamp1: Creating the container...
    bootcamp1:   Name: docker_bootcamp1_1453695135
    bootcamp1:  Image: sunlab/bigdata:0.04
    bootcamp1: Volume: /home/ec2-user/lab/bigdata-bootcamp:/home/ec2-user/bigdata-bootcamp
    bootcamp1: Volume: /home/ec2-user/lab/scripts:/home/ec2-user/bigdata-scripts
    bootcamp1: Volume: /home/ec2-user/lab/docker:/vagrant
    bootcamp1:
    bootcamp1: Container created: cc2f518631e86a11
==> bootcamp1: Starting container...
==> bootcamp1: Provisioners will not be run since container doesn't support SSH.
[ec2-user@ip-172-31-23-158 docker]$ vagrant ssh
Last login: Thu Jan 21 20:59:15 2016 from ip-172-17-0-1.ec2.internal
[ec2-user@bootcamp1 ~]$
```

Then start all hadoop related service by

```bash
[ec2-user@bootcamp1 ~]$ bigdata-scripts/start-all.sh
JMX enabled by default
Using config: /etc/zookeeper/conf/zoo.cfg
Starting zookeeper ... STARTED
starting proxyserver, logging to /var/log/hadoop-yarn/yarn-yarn-proxyserver-bootcamp.local.out
Started Hadoop proxyserver:                                [  OK  ]
starting namenode, logging to /var/log/hadoop-hdfs/hadoop-hdfs-namenode-bootcamp.local.out
Started Hadoop namenode:                                   [  OK  ]
starting datanode, logging to /var/log/hadoop-hdfs/hadoop-hdfs-datanode-bootcamp.local.out
Started Hadoop datanode (hadoop-hdfs-datanode):            [  OK  ]
starting resourcemanager, logging to /var/log/hadoop-yarn/yarn-yarn-resourcemanager-bootcamp.local.out
Started Hadoop resourcemanager:                            [  OK  ]
starting historyserver, logging to /var/log/hadoop-mapreduce/mapred-mapred-historyserver-bootcamp.local.out
Started Hadoop historyserver:                              [  OK  ]
starting nodemanager, logging to /var/log/hadoop-yarn/yarn-yarn-nodemanager-bootcamp.local.out
Started Hadoop nodemanager:                                [  OK  ]
Starting Spark worker (spark-worker):                      [  OK  ]
Starting Spark master (spark-master):                      [  OK  ]
Starting Hadoop HBase regionserver daemon: starting regionserver, logging to /var/log/hbase/hbase-hbase-regionserver-bootcamp.local.out
hbase-regionserver.
starting master, logging to /var/log/hbase/hbase-hbase-master-bootcamp.local.out
Started HBase master daemon (hbase-master):                [  OK  ]
starting thrift, logging to /var/log/hbase/hbase-hbase-thrift-bootcamp.local.out
Started HBase thrift daemon (hbase-thrift):                [  OK  ]
[ec2-user@bootcamp1 ~]$
```

## Termination

You can terminate a docker by `vagrant destroy --force` in `~/lab/docker/`.

## Limitations

After a docker container exit, you may loose data stored within it. You can map folder from AWS EC2 instance with Docker container for persistent data saving.