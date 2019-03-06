# base image
FROM ubuntu:14.04
# image metadata
LABEL maintainer="himanshusahu24@gmail.com"
# RUN - runs the command line, wait for it to finish and saves the result
RUN sudo apt-get -y update
RUN sudo apt-get -y install python3 python3-pip
RUN python3 --version && pip3 --version
RUN mkdir code && mkdir -p /home/
# ADD - add local files, add content of tar archives
# download the content from URL and store it at desired location
ADD requirements.txt code/requirements.txt
ADD server.py code/server.py
RUN pip3 install -r code/requirements.txt
# ENV - sets the environment variables during build and when running the result
ENV INTERNAL_DB_SERVER_PORT 1478
# The WORKDIR instruction sets the working directory for any RUN, CMD, ENTRYPOINT, COPY
# and ADD instructions that follow it in the Dockerfile.If the WORKDIR doesn’t exist,
# it will be created even if it’s not used in any subsequent Dockerfile instruction.
WORKDIR /home/
CMD python3 /code/server.py
# since we specify the WORKDIR as /home/. bash's working directory will be /home/