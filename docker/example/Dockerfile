FROM alpine:3.4
RUN apk update
RUN apk add python3 bash
RUN python3 --version && pip3 --version
RUN mkdir code
ADD requirements.txt code/requirements.txt
ADD server.py code/server.py
RUN pip3 install -r code/requirements.txt
CMD python3 code/server.py