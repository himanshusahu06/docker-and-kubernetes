# docker compose

1. compose images
    
    go to the directoy where docker-compose.yaml file is present and then run -
    ```shell
    $ docker-compose build
    ```

2. run all the container
    ```shell
    $ docker-compose up
    ```

3. create and run the container
    ```shell
    $ docker-compose up --force-recreate
    ```

4. verify the python server.
    ```shell
    $ curl http://localhost:5000/users?user=hsahu
    ```

5. get into the container.
    ```shell
    $ docker exec -ti {container-id} bash
    ```
