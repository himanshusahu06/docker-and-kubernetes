# Dockerfile

1. Build the docker image from dockerfile.
    ```shell
    docker build -t python-server:latest .
    ```

2. Run the container from image.
    ```shell
    $ export PYTHON_SERVER_PORT=5000
    $ docker run -d -p 8000:$PYTHON_SERVER_PORT -e PYTHON_SERVER_PORT=$PYTHON_SERVER_PORT python-server:latest
    ```

3. verify the python server.
    ```shell
    $ curl localhost:8000/hello
    Google.com
    ```

4. get into the container.
    ```shell
    $ docker exec -ti {container-id} bash
    ```

## Docker ENTRYPOINT vs CMD

### Entrypoint

*Entrypoint sets the command and parameters that will be executed first when a container is run.*

Any command line arguments passed to `docker run <image>` will be appended to the entrypoint command, and will override all elements specified using CMD. For example, `docker run <image> bash` will add the command argument bash to the end of the entrypoint.

#### Overriding Entrypoint
You can override entrypoint instructions using the `docker run --entrypoint`

### Cmd

The main purpose of a CMD is to provide defaults when executing a container. These will be executed after the entrypoint.

For example, if you ran `docker run <image>`, then the commands and parameters specified by CMD in your Dockerfiles would be executed.

In Dockerfiles, you can define CMD defaults that include an executable. For example:

`CMD ["executable","param1","param2"]`

If they omit the executable, you must specify an ENTRYPOINT instruction as well.

`CMD ["param1","param2"]` (as default parameters to ENTRYPOINT)

### NOTE: 
* There can only be one CMD instruction in a Dockerfile. If you list more than one CMD, then only the last CMD will take effect.
* Docker has a default entrypoint which is `/bin/sh -c` but does not have a default command.
* When you run docker like this: `docker run -ti ubuntu bash` the entrypoint is the default /`bin/sh -c`, the image is `ubuntu` and the command is `bash`.. i.e., the actual thing that gets executed is `/bin/sh -c bash`. The command is run via the entrypoint, so docker command is just paramater to the entrypoint.

## Reference
[Dockerfile reference](https://docs.docker.com/engine/reference/builder/)

[what-is-the-difference-between-cmd-and-entrypoint-in-a-dockerfile](https://stackoverflow.com/questions/21553353/what-is-the-difference-between-cmd-and-entrypoint-in-a-dockerfile)

Must read - [Multi stage docker build](https://blog.alexellis.io/mutli-stage-docker-builds/)