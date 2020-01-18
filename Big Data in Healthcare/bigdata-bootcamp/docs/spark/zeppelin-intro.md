---
---
# How to start Zeppelin

::: tip Learning Objectives

- Learn how to work with Zeppelin Notebook.

:::

::: warning

You can skip this section, if you use your locally installed Zeppelin

:::

## 1. Run provided Docker image

Please prepare your docker environment and refer to [this section](/env/env-local-docker.html#_2-pull-and-run-docker-image) to start your zeppelin service.

### Shared Folder

You can use shared folder between your local OS and the virtual environment on Docker.
This shared folder can be used to get data from your local and/or to save data without losing it after you exit/destroy your virtual environment.
Use `-v` option to make shared folder from an existing local folder and a folder in virtual environment:

> -v <local_folder:vm_folder>

You should use absolute path for `vm_folder`, but it does not need to be an existing folder. For example, if want to use `~/Data/` in my local OS as shared folder connected with `/sample_data/` in VM, I can start a container as following:

```bash
docker run -it --privileged=true \
  --cap-add=SYS_ADMIN \
  -m 8192m -h bootcamp1.docker \
  --name bigbox -p 2222:22 -p 9530:9530 -p 8888:8888\
  -v /path/to/Data/:/sample_data/ \
  sunlab/bigbox:latest \
  /bin/bash
```

## 2. Start Zeppelin service and create HDFS folder

If you have not started Zeppelin service,

```bash
/scripts/start-zeppelin.sh
```

We need to create a HDFS folder for the user `zeppelin` as:

```bash
sudo su - hdfs # switch to user 'hdfs'
hdfs dfs -mkdir -p /user/zeppelin # create folder in hdfs
hdfs dfs -chown zeppelin /user/zeppelin #  change the folder owner
exit
```

You can check whether it has been created or not by using:

```bash
hdfs dfs -ls /user/
```

## 3. Open Zeppelin Notebook in your browser

Once you have started Zeppelin service and have created HDFS folder for Zeppelin, you can access Zeppelin Notebook by using your local web browser.

Open your web browser, and type in the address:
`host-ip:port-for-zeppelin`
For example,
`192.168.99.100:9530` since the IP address assigned to my Docker container is `192.168.99.100` as it is shown above, and the port number assigned to Zeppelin service is `9530` as default in our Docker image.

Once you navigate to that IP address with the port number, you will see the front page of Zeppelin like:
![zeppelin-frontpage](./images/zeppelin/frontpage.png)

Let's move to do a simple tutorial in the next section.
