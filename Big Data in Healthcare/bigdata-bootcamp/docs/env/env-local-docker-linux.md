---
---
# Install Docker In Linux

## Install Docker on RHEL/CentOS/Fedora

+ [Get Docker CE for CentOS](https://docs.docker.com/install/linux/docker-ce/centos/)
+ [Get Docker CE for Fedora](https://docs.docker.com/engine/installation/linux/docker-ce/fedora/)

In brief, after updated your system, you can simply type the follow commands:

```bash
sudo yum install docker-ce -y # install docker package
sudo service  docker start # start docker service
chkconfig docker on # start up automatically
```

### FAQ

1. If your SELinux and BTRFS are on working, you may meet an error message as follow:

```bash
# systemctl status docker.service -l
...
SELinux is not supported with the BTRFS graph driver!
...
```

Modify /etc/sysconfig/docker as follow:

```bash
# Modify these options if you want to change the way the docker daemon runs
#OPTIONS='--selinux-enabled'
OPTIONS=''
...
```

Restart your docker service

2. Storage Issue:

Error message found in /var/log/upstart/docker.log

```
[graphdriver] using prior storage driver \"btrfs\"...
```

Just delete directory /var/lib/docker and restart docker service

## Install Docker on Ubuntu/Debian

+ [Get Docker CE for Ubuntu](https://docs.docker.com/engine/installation/linux/docker-ce/ubuntu/)
+ [Get Docker CE for Debian](https://docs.docker.com/engine/installation/linux/docker-ce/debian/)

Generally, you are supposed to add the repository, and then

```bash
sudo apt-get install docker-ce
```

Both Debian Series and RHEL Series can be controlled by

```bash
sudo service docker start # stop, restart, ...
```

Once you started your service, you would find a socket file `/var/run/docker.sock`, and then you would able to execute your docker commands.
