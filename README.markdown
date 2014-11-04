![Image of Helmsman](/static/images/helmsman.png)

Helmsman
==========================

Background
----------

Helmsman is for managing Docker.  At this time it is specifically for viewing and managing a private Docker registry.  Helmsman is built on using Python Flask and Twitter Bootstrap.


Running Helmsman
----------------

Helmsman can either be run standalone on a host system, or run as a Docker container.

* To run standalone:
  * Make sure your python environment includes both Flask and Requests ('pip install flask requests')
  * Edit the included config file in config/helmsman config to reflect your environment.  By default it assumes a local registry running on port 5000.
  * Run Helmsman with - 'python docker_index.py'

* To run as a Docker container:
  * Pull the latest Helmsman image
  * Look at the config file config/helmsman config and add one similar (relfecting your environment) somewhere on your docker host.  By default it assumes a local registry running on port 5000.
  * Run - 'docker run -d  --name=helmsman -h [YOUR HOST NAME] -v [HOST DIRECTORY FOR CONFIG FILE]:/opt/docker/helmsman/config depot.dev.lotame.com/helmsman:latest'
  * The container will use the default file if you don't configure one (then you could just run with: 'docker run -d  --name=helmsman -h [YOUR HOST NAME] depot.dev.lotame.com/helmsman:latest')
  * Don't forget to expose a port to the host if you need to!

Building the Helmsman Image
---------------------------

You can build your own Helmsman image if you like, with:

* docker build -t depot.dev.lotame.com/helmsman -rm .


Understanding the Config File
------------------------------

The first portion of the config just sets up the port and title of the application.  By default the application runs on port 80, and the Dockerfile is written to support that as well.

``` 
[helmsman]
port = 80
title = Helmsman Private Registry Viewer
```

Currently Helmsman only supports viewing a single Registry at a time.  You can see the settings under the *registry* setting.  The settings are pretty self explanatory with the exception of the *strip directory* setting.  That one was introduced as otherwise all of the repositories would show up as 'library/[repo name]', which I didn't like.  This feature allows you to strip that out if your registry is configured the same way and you don't like seeing that.


```
[registry]
protocol = http://
host = localhost
port = 5000
repo_path = /v1/repositories
json_path = json
api_version = v1

# With the private repo, everything shows under "library", this allows us to remove that
strip_directory = True
```

Future
------

* Refactoring - Create a run.py and move application startup outside of docker_index.py.  Also clean up some less than ideal code!
* Create configuration and new screens for viewing docker host information
* Create a home screen for Helmsman so you can see what "modules" exist
* Add more modules!