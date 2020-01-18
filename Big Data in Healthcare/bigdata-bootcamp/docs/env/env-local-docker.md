---
sidebarDepth: 2
---
# Docker in Local OS

::: tip
For the purpose of the environment normalization, we provide a simple [docker](https://docs.docker.com/) image for you, which contains most of the software required by this course. We also provide a few scripts to install some optional packages.
:::

The whole progress would seem as follow:

1. **Make sure you have enough resource**:
    1. It requires at least 8GB Physical RAM, 16GB or greater would be better
    2. It requires at least 15GB hard disk storage
2. Install a docker environment in local machine
3. Start Docker Service, pull images and create a instance
4. Just rock it!
5. Destroy the containers and images if they are not required anymore

::: warning
Since this docker image integrated a lot of related services for the course, it requires at least 4GB RAM for this virtual machine. If your can not meet the minimum requirement, the system could randomly kill one or a few process due to resource limitation, which causes a lot of strange errors which is even unable to reproduce.

**DON'T TRY TO DO THAT.**

You may try [Azure](/env/env-azure-docker.html) instead.
:::

[[toc]]

## 0. System Environment

You should have enough system resource if you are planning to start a container in your local OS.

You are supposed to reserve at least 4 GB RAM for Docker, and some other memory for the host machine. While, you can still start all the Hadoop related services except [Zeppelin](https://zeppelin.apache.org), even if you only reserve 4GB for the virtual machine.

## 1. Install Docker

Docker is a software technology providing operating-system-level virtualization also known as containers, promoted by the company [Docker, Inc.](docker.com). Docker uses the resource isolation features of the Linux kernel such as cgroups and kernel namespaces, and a union-capable file system such as OverlayFS and others to allow independent "containers" to run within a single Linux instance, avoiding the overhead of starting and maintaining virtual machines (VMs). (from [Wikipedia](https://en.wikipedia.org/wiki/Docker_(software)))

Basically, you can treat docker as a lightweight virtual machine hosted on Linux with a pretty high performance.

The principle of setting up a docker environment is pretty straightforward.

+ IF your operating system is Linux, you are supposed to install docker service directly
+ IF your operating system is mac OS, Windows,  FreeBSD, and so on, you are supposed to install a virtual machine, start a special configured Linux system which hosts a Docker service. You will control the dockers using remote tool

There is an official instruction from [the link](https://docs.docker.com/engine/installation/). You can check the official documentation to get the latest news and some detail explanations.

+ [Install Docker In Linux](/env/env-local-docker-linux.html)
+ [Install Docker In macOS](/env/env-local-docker-macos.html)
+ [Install Docker In Microsoft Windows](/env/env-local-docker-windows.html)

Once the docker installed, you should get a few commands start from docker and able to start your docker service, and launch your docker container.

+ docker - a tool to control docker
+ docker-machine -  a tool that lets you install Docker Engine on virtual hosts, and manage the hosts in remote
+ docker-compose - a tool for defining and running multi-container Docker applications

If we are using VirtualBox + Windows/macOS, the theory is pretty clear: we created a Linux instance in "virtual remote", and control it using docker-machine. If we are supposed to operate the "remote docker service", we are supposed to prepare a set of environment variables. We can list it using command:

```bash
docker-machine env default
```

This is the reason that why do we have to execute the follow command to access the docker.

```bash
eval $(docker-machine env default)
```

::: tip

If you are using docker-machine, you can not reach the port from virtual machine using ip 127.0.0.1 (localhost). As replacement, you should extract the IP using this command:

```bash
$ printenv  | grep "DOCKER_HOST"
DOCKER_HOST=tcp://192.168.99.100:2376
```

And then you should visit `192.168.99.100` instead of `127.0.0.1` to visit the network stream from virtual machine.

:::

If these environment are unsetted, docker will try to connect to the default unix socket file `/var/run/docker.sock`.

As a Docker.app user, this file is: 

``` bash
$ ls -alh /var/run/docker.sock
lrwxr-xr-x  1 root  daemon    55B Feb 10 19:09 /var/run/docker.sock -> /Users/yu/Library/Containers/com.docker.docker/Data/s60
$ ls -al /Users/yu/Library/Containers/com.docker.docker/Data/s60
srwxr-xr-x  1 yu  staff  0 Feb 10 19:09 /Users/yu/Library/Containers/com.docker.docker/Data/s60
```

As a Linux user, the situation is slightly different:

```bash
$ ls -al /var/run/docker.sock
srw-rw---- 1 root root 0 Feb 11 11:35 /var/run/docker.sock
```

::: tip
A Linux user **must** add a "sudo" before command `docker` since he has no access to `docker.sock` as an ordinary user.
:::

## 2. Pull and run Docker image

### (1) Start the container with:

The basic start command should be:

```bash
docker run -it --privileged=true \
  --cap-add=SYS_ADMIN \
  -m 8192m -h bootcamp.local \
  --name bigbox -p 2222:22 -p 9530:9530 -p 8888:8888\
  -v /:/mnt/host \
  sunlab/bigbox:latest \
  /bin/bash
```

In general, the synopsis of `docker run` is 

```bash
docker run [options] image[:tag|@digest] [command] [args]
```

Here is a case study to the options:

> -p host-port:vm-port

This option is used to map the TCP port `vm-port` in the container to port `host-port` on the Docker host.

Currently, `vm-port`s are reserved to:

+ 8888 - Jupyter Notebook
+ 9530 - Zeppelin Notebook

Once you started the Zeppelin service, this service will keep listening port `9530` in docker. You should able to visit this service using `http://127.0.0.1:9530` or `http://DOCKER_HOST_IP:9530`.

This remote IP depends on the Docker Service you are running, which has already described above.

+ If you are using Linux or Docker.app in macOS, you just need to visit "localhost:9530", or other port numbers if you changed `host-port`
+ If you are using VirtualBox + macOS or Windows, you should get the Docker's IP first

> -v, --volume=[host-src:]container-dest[:&lt;options&gt;]

This option is used to bind mount a volume.

Currently, we are using `-v /:/mnt/host`. In this case, we can visit the root of your file system for your host machine. If you are using macOS, `/mnt/host/Users/<yourname>/` would be the `$HOME` of your MacBook. If you are using Windows, you can reach your `C:` disk from `/mnt/host/c` in docker.

Variable `host-src` accepts absolute path only.

> -it

+ -i              : Keep STDIN open even if not attached
+ -t              : Allocate a pseudo-tty

> -h bootcamp.local

Once you enter this docker environment, you can ping this docker environment itself as `bootcamp.local`. This variable is used in some configuration files for Hadoop ecosystems.

> -m 8192m

Memory limit (format: `<number>[<unit>]`). Number is a positive integer. Unit can be one of `b`, `k`, `m`, or `g`.

This docker image requires at least 4G RAM, 8G RAM is recommended. However, if your local Physical Machine has ONLY 8G RAM, you are recommended to reduce this number to 4G.

Local machine is not the same as the remote server. If you are launching a remote server with 8G RAM, you can set this number as 7G.

If you are interested in the detail explanation of the args, please visit [this link](https://docs.docker.com/engine/reference/run/)

### (2) Start all necessary services

In generally, when you are in front of the command line interface, you will meet 2 kinds of prompt.

```bash
# whoami  # this prompt is '#' 
	#indices you are root aka the administrator of this environment now
root
$ whoami # this promot is '$' indices you are a ordinary user now
yu
```

Of course, it is pretty easy to change, you can simply update the environment variable `PS1`.

Assumption: every script is executed by `root`.

```bash
/scripts/start-services.sh
```

This script will help you start a the services for Hadoop ecosystems. You may meet "Connection Refused" exception if you did something else before started these services.

If you wish to host Zeppelin, you should install it first by using the command:

```
/scripts/install-zeppelin.sh
```

and start the service by using command:

```
/scripts/start-zeppelin.sh
```

then, Zeppelin will listen the port `9530`

Note: Please keep all the service are running before installing/starting Zeppelin.


If you wish to host Jupyter, you can start it by using command:

```bash
/scripts/start-jupyter.sh
```

Jupyter will listen the port `8888`

### (3) Stop all services

You can stop services if you want:

```
/scripts/stop-services.sh
```


### (4) Detach or Exit

To detach instance for keeping it up,

```
ctrl + p, ctrl + q
```

To exit,

```
exit
```

### (5) Re-attach

If you detached a instance and want to attach again,
check the `CONTAINER ID` or `NAMES` of it.

```bash
$ docker ps -a
CONTAINER ID        IMAGE                  COMMAND                CREATED             STATUS              PORTS                                                                  NAMES
011547e95ef5        sunlab/bigbox:latest   "/tini -- /bin/bash"   6 hours ago         Up 4 seconds        0.0.0.0:8888->8888/tcp, 0.0.0.0:9530->9530/tcp, 0.0.0.0:2222->22/tcp   bigbox
```

If the "STATUS" column is similar to "Exited (0) 10 hours ago", you are supposed to start the container again.

```bash
$ docker start <CONTAINER ID or NAMES>
```

Then attach it by:

```bash
$ docker attach <CONTAINER ID or NAMES>
```

Every time you restart your container, you are supposed to start all those services again before any HDFS related operations.

### (5) Destroy instance

If you want to permanently remove container

```bash
$ docker rm <CONTAINER ID or NAMES>
```

### (6) Destroy images

If you want to permanently remove images

List images first

```bash
$ docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
sunlab/bigbox       latest              bfd258e00de3        16 hours ago        2.65GB
```

Remove them by REPOSITORY or IMAGE ID using command:

```bash
$ docker rmi <REPOSITORY or IMAGE ID>
```

### (7) Update images

```
$ docker pull sunlab/bigbox
```


### (8) More official documents

Please refer to [this link](https://docs.docker.com/v17.09/engine/userguide/storagedriver/imagesandcontainers/) for the introduction of images, containers, and storage drivers.


### (9) Optional: use docker-compose

[Docker Compose](https://docs.docker.com/compose/) is a tool for defining and running multi-container Docker applications. A simple `docker-compose.yml` could ***simplify*** the parameters, and make the life easier.

Please refer to [this link](/env/env-docker-compose.html#docker-compose) for some further instruction.


## 3. Logs and Diagnosis


### System Configurations

```
## cat /proc/meminfo  | grep Mem ## Current Memory
MemTotal:        8164680 kB ## Note: This value shoud no less than 4GB
MemFree:          175524 kB
MemAvailable:    5113340 kB
## cat /proc/cpuinfo  | grep 'model name' | head -1  ## CPU Brand
model name	: Intel(R) Core(TM) i7-7920HQ CPU @ 3.10GHz
## cat /proc/cpuinfo  | grep 'model name' | wc -l ## CPU Count
4
## df -h ## List Current Hard Disk Usage
Filesystem      Size  Used Avail Use% Mounted on
overlay          32G  4.6G   26G  16% /
tmpfs            64M     0   64M   0% /dev
...
## ps -ef ## List Current Running Process
UID        PID  PPID  C STIME TTY          TIME CMD
root         1     0  0 01:38 pts/0    00:00:00 /tini -- /bin/bash
root         7     1  0 01:38 pts/0    00:00:00 /bin/bash
root        77     1  0 01:43 ?        00:00:00 /usr/sbin/sshd
zookeep+   136     1  0 01:43 ?        00:00:14 /usr/lib/jvm/java-openjdk/bin/java -Dzookeeper.log.dir=/var/log/zookeeper -Dzookeeper.root.logger=INFO,ROLLINGFILE -cp /usr/lib/zookeeper/bin/../build/classes:/
yarn       225     1  0 01:43 ?        00:00:13 /usr/lib/jvm/java/bin/java -Dproc_proxyserver -Xmx1000m -Dhadoop.log.dir=/var/log/hadoop-yarn -Dyarn.log.dir=/var/log/hadoop-yarn -Dhadoop.log.file=yarn-yarn-pr
...
## lsof -i:9530 ## Find the Process Listening to Some Specific Port
COMMAND  PID     USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
java    3165 zeppelin  189u  IPv4 229945      0t0  TCP *:9530 (LISTEN)
```

### Logs

+ **hadoop-hdfs** -- /var/log/hadoop-hdfs/*
+ **hadoop-mapreduce**  -- /var/log/hadoop-mapreduce/*
+ **hadoop-yarn** -- /var/log/hadoop-yarn/*
+ **hbase**  --  /var/log/hbase/*
+ **hive**  -- /var/log/hive/*
+ **spark**  -- /var/log/spark/*
+ **zookeeper** -- /var/log/zookeeper/*
+ **zeppelin** -- /usr/local/zeppelin/logs/*

### Misc.

#### User and Role

```
[root@bootcamp1 /]# su hdfs  ## This command is used to switch your current user to hdfs
					## Note: switch user requires special permission
					## You can not switch back using su root again
bash-4.2$ whoami ## check current user
hdfs
bash-4.2$ exit ## role is a stack, you can quit your role from hdfs to root
[root@bootcamp1 /]#
[root@bootcamp1 /]# sudo -u hdfs whoami ## execute a command 'whoami' using user 'hdfs'
hdfs
[root@bootcamp1 /]#

```

User `hdfs` is the super user in HDFS system. User `root` is the super user in Linux system.

```
[root@bootcamp1 /]# sudo -u hdfs hdfs dfs -mkdir /tmp
```

In this case, user root has no permission to write data in `/`, but it could ask user hdfs to process it. 

#### Relative Path and Absolute Path

An absolute or full path points to the same location in a file system, regardless of the current working directory. To do that, it must include the root directory. [wiki](https://en.wikipedia.org/wiki/Path_(computing)#Absolute_and_relative_paths).

When we are talking about `/mnt/host`, it always pointing to the path `/mnt/host`. However, if the path is not startswith "/", it means to start from "current working path".

In Linux system, you can get your "current working path" using command 

```bash
## pwd
/root
```

In HDFS system, the "current working path" would be `/user/<your-name>`.

A relative path would be the result of `cwd` plus your string.

When we are coding in hadoop, we may required to fill in a location pointing to the path of input files. The synopsis of this path is is 

`[schema://]your-path`

An HDFS path `hdfs:///hw1/test.csv` is combined by `hdfs://` and  `/hw1/test.csv`. There are 3 slashes over there. If you only filled 2 slashes over there (`hdfs://hw1/test.csv`), it is equal to `hdfs:///user/root/hw1/test.csv`, which may not be expected.

Ditto for `file:///path/to/your/local/file.csv`.

#### Other Linux Commands

This environment is based on CentOS 7. This course does not requires you have too much knowledge in Linux, but if you can use some basic commands, that would be better.

If you are interested, please refer to [this link](https://files.fosswire.com/2007/08/fwunixref.pdf) for a Unix/Linux Command Cheat Sheet.

