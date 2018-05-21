# Docker

## Docker Commands

### docker run
* create and run a container from image
* Can attach persisted storage
* args
    * -p <docker-host-port>:<container-port> (map container port to host port)
    * In windows it will be docker machine port
    * In linux machine it will be port of linux machine
    * --memory <maximum_allowed_memory> (—memory 2G (2 GB memory is allowed))
    * --cpu-quota <quora>
    * --rm (cleanup container after usage)

`docker run --detach -p 3306:3306 -ti mysql / bin/bash` (open specific port to host machine and forward it to container)`

`docker ps` (active containers)

`docker ps -a` (show all container)

`docker start / stop <docker-id>`

`docker attach --detach-keys="ctrl-x” <docker-id>` (use this key to exit container without stopping it)

`docker top <docker-id or docker-name>` (lists the processes running on container)

`docker build -t <name>:<tag> <DockerFile directory location>` (build a docker image from DockerFile)

`docker rmi <image name / id>` (remove a image)

`docker port <docker port 3c9b6a1f67d2>` (gives mapped port)

`docker run --rm -ti -p 45678:45678 -p 45679:45679 --name echo-server ubuntu:14.04 bash` (Delete docker container after stop)

## Docker Container Networking

container can connect to host machine with host machine IP address.

Container can connect to other container through host machine IP address or by container IP address because containers are in same private network.

### Network connection between containers:
* Use `--link <CONTAINER_NAME_TO_BE_LINKED>` while running a container to use this container name instead of IP address of container.

e.g.:

`docker run -ti --rm --name server ubuntu:14.04 bash`     (server)

`docker run --rm -ti --link server --name client ubuntu:14.04 bash` (here client can use `ping server` instead of IP address)


## Docker Volumes


Can share volume either from host machine or from other container.
* `docker run -ti -v /Users/himanshu.sahu/Desktop/golang:/data --name golang-dir-dc ubuntu /bin/bash`  (persistence storage)
* args:
    * `-v <HOST_DIR>:<CONTAINER_DIR>` (volume from host, persisted)
    * `-v <CONTAINER_DIR>` (create a volume dir in container, non persisted)
    * `--volumes-from <CONTAINER_NAME>` (it will share same volume as the container passed, non-persisted)
    * Shared volume will exist till no container is using it, even if container which created the volume dies.

## Docker Private Network

Create a private network: `docker network <NETWORK_NAME>`

You can connect to any network using net parameter:
* `docker run --rm -ti --name server --net example-docker-network ubuntu:14.04 /bin/bash`
* To access other container in same network we don’t need to link the containers but for the sake of simplicity we should do it.
* Should limit access to one host only by `-p 127.0.0.1:1234:1234/tcp` (forward traffic to 1234 port if request is coming from host 1234 port only)
* This is how private container / services are created.

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

`docker tag <IMAGE_ID> <NAME_OF_IMAGE>:<VERSION_TO_PUSH>`

`docker push <NAME_OF_NEW_IMAGE>:<VERSION_TO_PUSH>`











