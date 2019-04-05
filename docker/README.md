# Docker

## Docker Commands

### running a container

create and run a container from image.

* arguments
    * `-p <docker-host-port>:<container-port>/protocol{udp/tcp} `(maps container port to host port)
        * multiple ports can be specified.
        * In windows it will be docker machine port.
        * In linux machine it will be port of linux machine.
    * `--memory <maximum_allowed_memory>` (—memory 2G)
    * `--rm` cleanup container after usage
    * `-ti` interactive terminal
    * `-d` or `--detach` detach container after start
    * `--name` unique container name or else docker will assign random name

```shell
$ docker run -ti --rm -d -p 3306:3306 --name mysql-server mysql /bin/bash
```

### docker main process
every docker container have a main process and container stops when that process exits. e.g.

```shell
$ docker run --rm -ti ubuntu-with-my-file:1.0.0 sleep 5
```
this will stop container after 3 second becasue `/bin/sh -c sleep 5` is it's main process.

### containers commands

* show all containers
    ```shell
    $ docker container ls -a
    ```

* show running containers
    ```shell
    $ docker container ls
    ```

* show last exited containers (only one containers)
    ```shell
    $ docker ps -l
    ```

* start stop containers
    ```shell
    $ docker start/stop <container-id>
    ```

* attach a running docker container
    ```shell
    $ docker attach --detach-keys='ctrl-x' <container-id>
    ```
    use `ctrl-x` this key to exit container without stopping it.

* lists the processes running on container
    ```shell
    $ docker top <container-id>
    ```

* remove an image
    ```shell
    $ docker rmi <image-name>:<version>
    ```

* list mapped port of a container
    ```shell
    $ docker port <container-id>
    ```

`docker build -t <name>:<tag> <DockerFile directory location>` (build a docker image from DockerFile)

## Docker Container Networking

* docker container can connect to host machine with host machine IP address.
* container can have private networks.
* you cab group your containers into `private networks`.

#### docker's default private network

If we don't specify the network while running the container, all the container will be in same private network - `docker's default virtual network`. In this case server need to expose ports to host machine and client will have to connect to host machine in order to communicate with server container.

e.g.

server docker container - 

```shell
$ docker run --rm -ti -p 45679:45678 --name echo-server ubuntu:14.04 bash
```

client docker container -
```shell
docker run --rm -ti --name echo-client ubuntu:14.04 bash
```

Although, server container's port 45678 is mapped to host's 45679 port, client container can communicate to the server by just connecting to the 45679 port of host machine and request will be forwared to server container.

#### container linking (unidirectional)

client container can connect to server container by linking its to itself. when docker starts a container, it creates a entry of linked container in `/etc/hosts` file of the client container and then client container can connect to server container by it's name or container id. **But this communucation is unidirectional**. Only container which is linked to another container will be able to communicate.

e.g.

server container -
```shell
$ docker run -ti --rm --name server ubuntu:14.04 bash
root@9eac1c4d69ff:/# nc -lp 1234
hello
```

client container -
```shell
$ docker run -ti --rm --link server --name client ubuntu:14.04 bash
root@0b1400c2c0e9:/# cat /etc/hosts
127.0.0.1	localhost
.....
172.17.0.2	server 9eac1c4d69ff
172.17.0.3	0b1400c2c0e9
root@0b1400c2c0e9:/# nc -l server 1234
hello
```

Drawback
* if server gets reconfigured, or it's ip address changes, client will not be able to connect to server. Hence, this networking is not recommended.

#### Docker Private Network

You can create a private network in docker host and containers can be configured to run within speified private virtual network. This network have builtin nameserver that resolves the links. So if ip gets reconfigured, nameserver entries will automatically get updated without restarting any of the container.

* Create a private network
    ```shell
    $ docker network create <network_name>
    ```

* running a container with virtual network
    ```shell
    $ docker run -ti --rm --name server --net=private-network ubuntu:14.04 bash
    ```

#### IP address binding to your services

service that listen locally by default are only available in the container.

to allow connection to your server from outside of container, you need to use bind address `0.0.0.0` inside the container.

also limit the docker to accept connection from host only.

You can connect to any network using net parameter:
* `docker run --rm -ti --name server --net example-docker-network ubuntu:14.04 /bin/bash`
* To access other container in same network we don’t need to link the containers but for the sake of simplicity we should do it.
* Should limit access to one host only by `-p 127.0.0.1:1234:1234/tcp` (forward traffic to 1234 port if request is coming from host 1234 port only)
* This is how private container / services are created.


## Docker Volumes
these are virtual disk to store and share data

Can share volume either from host machine or from other container.

1. persisted volumes

```shell
$ docker run --rm -ti -v /Users/himanshu.sahu/docker_shared_dir:/shared_dir ubuntu:14.04 bash
```

2. ephemeral volumes
* `docker run -ti -v /Users/himanshu.sahu/Desktop/golang:/data --name golang-dir-dc ubuntu /bin/bash`  (persistence storage)
* args:
    * `-v <HOST_DIR>:<CONTAINER_DIR>` (volume from host, persisted)
    * `-v <CONTAINER_DIR>` (create a volume dir in container, non persisted)
    * `--volumes-from <CONTAINER_NAME>` (it will share same volume as the container passed, non-persisted)
    * Shared volume will exist till no container is using it, even if container which created the volume dies.



## Execute processes / commands inside container

### docker exec
* Starts another process in an existing container
* Can’t add port, volume etc
* When type `exit`, it will exit from the container without stopping  it,

e.g.:

`docker exec -ti 99842730dedd /bin/bash`

`docker exec -ti  99842730dedd ifconfig | grep inet | head -1`

`docker exec -ti  -w <WORKING_DIRECTORY_INSIDE_CONTAINER> <docker port 3c9b6a1f67d2> <COMMAND_STRING>`

## Creating and publishing Images from Existing Container / Images

### From Existing Container create an image:

#### docker commit
* create an images from current container state
* Edit / create the tag of docker image
* Publish the image

`docker commit -a <AUTHOR_NAME> -m <COMMIT_MESSAGE> <CONTAINER_ID> <NAME_OF_NEW_IMAGE>:<VERSION>`

Pushing the imager to hub:

#### Pushing in existing hub
1. **Step 1:** Create a tag, either from container or directly from image
2. **Step 2:** push the image to hub
3. You can push only image not the containers

https://docs.docker.com/v17.12/docker-cloud/builds/push-images/














