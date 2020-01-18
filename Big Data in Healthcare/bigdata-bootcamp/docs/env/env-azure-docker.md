---
---
# Docker in Azure

We could use [Azure](https://azure.microsoft.com) as a virtual machine provider. If you have no enough resource to host our envornment in local, you can also launch an Azure instance, start a docker service inside, and host our docker image.

We can create a Docker on Ubuntu Server in Azure, and then pull image from hub.docker.com.

## Launch an Azure instance

### Option 1: Launch a Pre-installed Docker Host

"Docker on Ubuntu Server" is a container based on Ubuntu Server 16.04 LTS published by Canonical. You can launch a new ”Docker on Ubuntu Server” instance, and you will able to start your docker directly.

1. Open the Portal in Azure at <https://portal.azure.com>
2. Click Virtual Machines on the left sidebar
3. Click “+ ADD” to create a new instance
4. Type “docker” in search box, and select "Docker on Ubuntu Server"
5. Click “Create” on the introduction page
6. Fill your host name, user name, authentication
7. Click Pricing Tier, and choose D2S_V3
8. Click “create” to create the instance

::: tip

The `D2S_V3` is just an example. You may choose anyone fulfill the requirement ( RAM may greater than 8G, CPU should more than 1).

:::

### Option 2: Launch a clear linux

"Docker on Ubuntu Server" is using "[classic deployment](https://docs.microsoft.com/en-us/azure/azure-resource-manager/resource-manager-deployment-model)". It seems like there are too few choise in "classic deployment" now. If you wish to have different option.
Or, if you are more familiar with CentOS, SUSE or some other [distributions](https://en.wikipedia.org/wiki/Linux_distribution), you can simply choose them.

In this case, you could unlocked more options in Azure Instance Type. Whatever your choise is, it is just a docker container, which does not matter the detail in your environment.

1. Open the Portal in Azure at <https://portal.azure.com>
2. Click Virtual Machines on the left sidebar
3. Click “+ ADD” to create a new instance
4. Type “CentOS”, or "Ubuntu" in search box, and select any image you like. For example, I would like to choose "Ubuntu Server 16.04 LTS" here
5. You should able to find a drop down box between "Select a deployment mode" and "Create" which should has 2 options "Resource Manager" and "Classic". Please make sure it is on "Resource Manager"
6. Click “Create” on the introduction page
7. Fill your host name, user name, authentication
8. Click "Ok", and you should see a few options for your virtual machine. For this course, I would suggest you to choose a instance has 8GB or 16GB RAM and 2-4 vCPUs
9. Fill in the rest of the information by yourself, and finally click “create” to create the instance

## Connect to the instance

1. Open the Portal in Azure at <https://portal.azure.com>
2. Click All resources on left sidebar.
3. Select your instances from “Virtual machines (classic)”, “Cloud service” or "Virtual machines" depends on your choise
4. find Public IP addresses in “Overview”
5. Login via command “ssh your-username@public-ip” in *nix or using putty for windows
6. (If you are using option 2), [Install Docker in Linux](/env/env-local-docker-linux.html)

## Start a docker container

Most of the related application are already installed, you can also install other apps with command “apt-get”.

For example:

```bash
sudo apt-get install git tmux
```

And then, start a new docker instance

```bash
sudo docker run -it --privileged=true \
  --cap-add=SYS_ADMIN \
  -m 6144m -h bootcamp.local \
  --name bigbox -p 2222:22 -p 9530:9530 -p 8888:8888\
  -v /:/mnt/host \
  sunlab/bigbox:latest \
  /bin/bash
```

Please refer to [this section](/env/env-local-docker.html#_2-pull-and-run-docker-image) for some detail information of docker.

If you are interested, you may also use [docker-compose](/env/env-docker-compose.html#docker-compose) to manage the service easier.


## Login remotely and the corresponding security issue

To access the service we launched in Azure, we are required to get the corresponding port opened. In default, the ports are closed. A good way to open it is change the rule of filewall. Please refer to [this official document](https://docs.microsoft.com/en-us/azure/virtual-machines/windows/nsg-quickstart-portal) to open the port.

However, since this image was designed to start a easy learning environment, if you keep the ports open to the public, your environment could be hacked easily. You can also making full use of the [SSH port forwarding](https://www.ssh.com/ssh/tunneling/example).

For example, you can create a new terminal, and type a command as follow:

```
ssh -L 2222:localhost:2222 \
    -L 8888:localhost:8888  \
    your-azure-user@your-azure-host
```

This command will connect to your azure VM. In the meantime, It will also forward the network steam from azure:{2222, 8888}. And then, you can visit `localhost:8888` to visit jupiter if you have your jupiter in azure started.




::: tip

1. The spending in Azure is calculated by time usage. Launch a better instance and fully destroy it instance once you finish your job will reduce your time in any dimension
2. You may use [tmux](https://tmux.github.io/) to make your life better

:::
