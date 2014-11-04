###############################################################################################
## CSC 10/29/2014
## 
## This image holds a simple project for viewing a private repo
##
## Build with docker build -t depot.dev.lotame.com/helmsman -rm .
##
## Run with something like this:
##
##    docker run -d -name=helmsman -p 80:80  -v /opt/docker/helsman/config:/opt/docker/helmsman/config depot.dev.lotame.com/helmsman
##
## Currently the Helmsman config file holds the location of the private registry.
##
## An optional config file for the repo-viewer is mounted at:
##
##    /opt/docker/helmsman/config
##  
## .. otherwise it uses the default if you don't mount the volume.
##
#############################################################################################

FROM        ubuntu:latest
MAINTAINER  CSConnell "cconnell@lotame.com"

# This next line is for whenever eithe Comment or Description is supported by docker build
#COMMENT	Helsman is a Docker management tool initially used for managing private repositories.

RUN apt-get update
RUN apt-get install -y python-pip gcc g++

RUN pip install flask requests

ADD static/ /opt/docker/helmsman/static/
ADD templates/ /opt/docker/helmsman/templates
ADD docker_index.py /opt/docker/helmsman/docker_index.py
ADD config/helmsman.cfg /opt/docker/helmsman/config/helmsman.cfg

EXPOSE 80
CMD ["python", "/opt/docker/helmsman/docker_index.py"]