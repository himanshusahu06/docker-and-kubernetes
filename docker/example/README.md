Build the image from docker file.

`docker build -t <IMAGE_NAME>:<TAG> .`

Run the container from image

`docker run -ti -d -p 8000:5000 <IMAGE_NAME>:<TAG>`

```shell
curl localhost:8000/hello
```