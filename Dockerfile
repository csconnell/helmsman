###############################################################################################
## CSC 10/30/2013
## 
## This image holds a simple project for viewing the library of the repo on
## depot.dev.lotame.com
##
## Build with docker build -t depot.dev.lotame.com/repo-viewer -rm .
##
## Run with something like this:
##
##    docker run -d -name=repo_viewer -p 33912:33912 -v /opt/docker/repo/repositories/library:/opt/docker/repo/repositories/library -v /opt/docker/repo-viewer/config:/opt/docker/repo_viewer/config depot.dev.lotame.com/repo-viewer
##
##  This assumes that the repo at depot.dev.lotame.com has been started with a mount at:
##  /opt/docker/repo/repositories/library
##
##  and that an optional config file for the repo-viewer is mounted at:
##  /opt/docker/repo_viewer/config
##  .. otherwise it uses the default if you don't mount the volume.
##
#############################################################################################

FROM        ubuntu:latest
MAINTAINER  CSConnell "cconnell@lotame.com"

RUN apt-get update
RUN apt-get install -y python-pip gcc g++ ##python-dev

RUN pip install flask requests

ADD static/ /opt/docker/repo_viewer/static/
ADD templates/ /opt/docker/repo_viewer/templates
ADD python_docker_index.py /opt/docker/repo_viewer/python_docker_index.py
ADD config/repo.cfg /opt/docker/repo_viewer/config/repo.cfg

EXPOSE 33912
CMD ["python", "/opt/docker/repo_viewer/python_docker_index.py"]