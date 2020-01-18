---
sidebarDepth: 2
---
# Docker Compose

::: tip
This is an optional section. Docker Compose is just a utility, which does **NOT** affect the functionality of the docker image and our course.

You can simply ignore it if you believe the docker commands are enough.
:::

[Docker Compose](https://docs.docker.com/compose/) is a tool for defining and running multi-container Docker applications. We can write a simple `docker-compose.yml` file as configure file, and launch a docker container as a service easily.

This means you can fix all your parameters in your configure file, and start/stop them using more biref commands.

## Official Guides

+ [Compose Overview](https://docs.docker.com/compose/overview/)
+ [Install Compose](https://docs.docker.com/compose/install/)
+ [Getting Started](https://docs.docker.com/compose/gettingstarted/)
+ [Compose command-line reference](https://docs.docker.com/compose/reference/)
+ [Compose file version 3 reference](https://docs.docker.com/compose/compose-file/)
  + [Compose file structure and examples](https://docs.docker.com/compose/compose-file/#compose-file-structure-and-examples)
+ [Environment file](https://docs.docker.com/compose/env-file/)

## Install Docker Compose

If you are a Windows/macOS user, the `docker-compose` should installed with your docker application.

If this command is missing in your machine

```bash
# docker-compose
-bash: docker-compose: command not found
```

It is also pretty easy.

Please visit the [Docker Compose Release Page](https://github.com/docker/compose/releases), following the guide and download the latest binary release.

## Create A `docker-compose.yml`

You can go to an empty folder in somewhere, and create a text file named as `docker-compose.yml`. The content may as follow:

```yaml
version: '3'

services:
  bootcamp:
    image: sunlab/bigbox:latest
    hostname: bootcamp
    domainname: local
    restart: "no"
    volumes:
    # Volumes section defined the mappings between host machine and
    # virtual machine.
    # ":" split each element into 2 parts
    # the left part is the folder in host machine
    # the right part is the folder in virtual machine
    # docker-compose support relative path
    # Please refer to
    # https://docs.docker.com/compose/compose-file/#volumes
    # for more detail if you are interested
      - ./data/logs:/var/log
      - ./data/host:/mnt/host
    environment:
      - CONTAINER=docker
    # /scripts/entrypoint.sh will start all the services
    # and then finally listen to port 22.
    command: [ "/scripts/entrypoint.sh" ]
    ports:
    # Ports section defined a few rules and forward the network
    # stream between host machine and vm.
    # As the rules in volumes section
    # The left part is for your host machine.
    # This means you can visit localhost:2333
    # and then get the response from the app
    # listening port 22 in docker container 
      - "2333:22"
      - "7077:7077" # spark
      - "4040:4040"
      - "4041:4041"
      - "8888:8888"
      # - "8983:8983" # for solr
```

[Here](https://github.com/yuikns/bigbox/tree/master/example) is a example.

## Basic Operation

Similar to other parts. If you are a linux user, you should always add an 'sudo' before the command `docker-compose`.

### Up and Down, Start and Stop. How to control the virtual environment

If you wish to create and start the container(s).

```bash
docker-compose up
```

This command will search the configure file `docker-compose.yml` or `docker-compose.yaml` in current folder, and start the corresponding services.

It will pull the image described in the yml file if there is no local cache. Otherwise it will create a container through local image.

In this case, if you close the terminal, the service may be stopped but not destroyed.

You an pass a parameter `-d`. This parameter indices the docker-compose will run the containers in the background after started.

Please type the following command for more introduction.

```bash
docker-compose help up
```

If you wish to clearly terminate everything. You may type

```bash
docker-compose down
```

This command will stops containers and removes containers, networks, volumes, and images created by `up`.

Everything inside the container are vanished.

If you have a container created. You may use `docker-compose start/stop/restart` to start/stop/restart the service. The container will stay over there

### Run, Exec and SSH. How to access the environment

```bash
docker-compose run bootcamp bash
```

`run` will launch a brand new container based on the configuration. `bootcamp` is name of the service in the config. This may useful in debugging or somewhere else, but may not fit for this course.

```bash
docker-compose exec bootcamp bash
```

`exec` will reuse the container and execute a specific command. The command is `bash` in this case. You should make sure the service is already started before typing this command.

You can also access the environment through [SSH](https://www.openssh.com/).

We have also initialized the SSH RSA Keys [here](https://github.com/yuikns/bigbox/tree/master/config/ssh).

```bash
curl https://raw.githubusercontent.com/yuikns/bigbox/master/config/ssh/id_rsa -o bigbox-private-key
chmod 0600 bigbox-private-key # prevent error: Permissions 0644 for './bigbox-private-key' are too open.
ssh -p 2333 -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -i bigbox-private-key root@127.0.0.1
```

If you are running your docker compose in remote. This identity file may unsafe. You can generate a pair by yourself.

```bash
[root@bootcamp ~]# rm -rf ~/.ssh/
[root@bootcamp ~]# ssh-keygen
Generating public/private rsa key pair.
Enter file in which to save the key (/root/.ssh/id_rsa):
Created directory '/root/.ssh'.
Enter passphrase (empty for no passphrase): # type enter here
Enter same passphrase again: # type enter here again
Your identification has been saved in /root/.ssh/id_rsa.
Your public key has been saved in /root/.ssh/id_rsa.pub.
The key fingerprint is:
SHA256:2NYgKW6bCmLvFPAug868hXBAIW6PhWlJeRK6LeYCHJ0 root@bootcamp.local
The key's randomart image is:
+---[RSA 2048]----+
|.=+              |
|*o=..  .         |
|oXoE. o .        |
|++B. . + o       |
|=+o+o . S .      |
|*oo..o .         |
|=* +o            |
|B.*.             |
| =+o             |
+----[SHA256]-----+
[root@bootcamp ~]# cd .ssh/
[root@bootcamp .ssh]# cp id_rsa.pub authorized_keys
[root@bootcamp .ssh]# chmod 0600 authorized_keys
[root@bootcamp .ssh]# ls -alh
total 20K
drwx------ 2 root root 4.0K Jun 20 08:42 .
dr-xr-x--- 1 root root 4.0K Jun 20 08:41 ..
-rw------- 1 root root  401 Jun 20 08:42 authorized_keys
-rw------- 1 root root 1.7K Jun 20 08:41 id_rsa
-rw-r--r-- 1 root root  401 Jun 20 08:41 id_rsa.pub
```

You may copy the `id_rsa` file to local as your key file.

### Logs

#### Logs for Hadoop Ecosystem

You may noticed, the sample `docker-compose.yml` mapped the folder from `/var/log` in vm to `./data/logs` in physical machine. You may simply check the files in your folder `./data/logs`.

#### Logs from docker container

You may trace it using command:

```bash
docker-compose logs -f --tail=100
```
