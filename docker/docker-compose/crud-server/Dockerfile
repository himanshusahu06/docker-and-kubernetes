# multstage build
FROM ubuntu:18.04 as pip-installer-image
RUN apt-get -y update
RUN apt-get install -y python3.6 python3-pip
RUN mkdir /nutanix-src
RUN echo ${PWD}
ADD ./requirements.txt /nutanix-src
RUN pip3 install -r /nutanix-src/requirements.txt && rm -rf /nutanix-src/requirements.txt

FROM ubuntu:18.04 as final-image
RUN apt-get -y update
RUN apt-get install -y sudo python3.6 netcat
RUN mkdir /nutanix-services /nutanix-services-logs
COPY --from=pip-installer-image /usr/local/lib/python3.6 /usr/local/lib/python3.6/
ADD ./crud-server.py /nutanix-services
CMD python3.6 /nutanix-services/crud-server.py > /nutanix-services-logs/server.log

# if multi project build is not used then image size will increase drastically as much as 498MB
#
# my-custom-image-multistage       1.0.0               9aa1f06251be        6 minutes ago       152MB  <-- multistage build
# my-custom-image                  1.0.0               9bf2868d00a2        38 minutes ago      498MB  <--- normal build
# ubuntu                           18.04               47b19964fb50        4 weeks ago         88.1MB
# alpine                           latest              caf27325b298        5 weeks ago         5.53MB
#