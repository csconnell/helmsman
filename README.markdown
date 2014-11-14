![Image of Helmsman](http://s25.postimg.org/43rneebqj/helmsman.png)

Helmsman
==========================

Background
----------

Helmsman is for managing Docker.  At this time it is specifically for viewing and managing a private Docker registry as well as view and manage Docker hosts, including stopping, starting, restarting, and removing containers.  Helmsman is built on using Python Flask and Twitter Bootstrap.


Running Helmsman
----------------

Helmsman can either be run standalone on a host system, or run as a Docker container.

* To run standalone:
  * Make sure your python environment includes both Flask and Requests as well as the YAML-based config module layered-yaml-attrdict-config ('pip install flask requests layered-yaml-attrdict-config')
  * Edit the included config file in config/helmsman config to reflect your environment.  By default it assumes a local registry running on port 5000.
  * Run Helmsman with - 'python bin/run.py'

* To run as a Docker container:
  * Pull the latest Helmsman image
  * Look at the config file config/helmsman.yml config and add one similar (relfecting your environment) somewhere on your docker host.  By default it assumes a local registry running on port 5000 and it has some sample config for Docker hosts.
  * Run - 'docker run -d  --name=helmsman -h [YOUR HOST NAME] -v [HOST DIRECTORY FOR CONFIG FILE]:/opt/docker/helmsman/config depot.dev.lotame.com/helmsman:latest'
  * The container will use the default file if you don't configure one (then you could just run with: 'docker run -d  --name=helmsman -h [YOUR HOST NAME] csconnell/helmsman:latest')
  * Don't forget to expose a port to the host if you need to!

Building the Helmsman Image
---------------------------

You can build your own Helmsman image if you like, with:

* docker build -t [YOUR REPO]/helmsman -rm .


Understanding the Config File
------------------------------

NOTE - The config file has changed to a YAML based file

The first portion of the config just sets up the port and title of the application.  By default the application runs on port 80, and the Dockerfile is written to support that as well.

``` 
helmsman:
  port: 80
  title: Helmsman
```

Helmsman currently has two modules, one for viewing / managing a private registry and one for viewing docker hosts and managing the containers.  These modules can be turned on or off (default is on) using the following configuration:

```
modules:
  - Index_Manager:
    description: Used to manage a private Docker registry.
    enabled: true
    endpoint: repos
    name: Private Registry Manager
  - Host_Manager:
    description: Used to view Docker host information and manage containers.
    enabled: true
    endpoint: hosts
    name: Host Manager
```
Flip the enabled flag from true to false to turn off a module.  You shouldn't need to change anything else.  The endpoint refers to the URL for that module as that gets used dynamically in the home page navigation.

The Host Manager is configured via the docker_hosts block.  Just add a new collection for the new host, and under each item add a host and port.  In the future this may be more dynamic.

```
docker_hosts:
  - dkrdev01:
    host: dkrdev01.dev.mycompany.com
    port: 4243 
  - dkrdev02:
    host: dkrdev02.dev.mycompany.com
    port: 4243
  - dkrdev03:
    host: dkrdev03.dev.mycompany.com
    port: 4243
```

Currently Helmsman only supports viewing a single Registry at a time.  You can see the settings under the *registry* setting.  The settings are pretty self explanatory with the exception of the *strip directory* setting.  That one was introduced as otherwise all of the repositories would show up as 'library/[repo name]', which I didn't like.  This feature allows you to strip that out if your registry is configured the same way and you don't like seeing that.


```
registry:
  protocol: http://
  host: localhost
  port: 5000
  repo_path: /v1/repositories
  json_path: json
  api_version: v1

  # With the private repo, everything shows under "library", this allows us to remove that
  strip_directory: True
```

Change Log
----------

v 1.1.0

* Moved config file to YAML to support more complex configs
* Restructured project to allow more modular based growth, including adding a config object, a base layout, and a run class that support running standalone or with GUnicorn or something similar - this resulted in a change in the launching method, now run bin/run.py
* Added a way to view Docker Host Info and view containers
* Added a way to start, stop, restart, remove containers
* Created a Home screen for Helmsman
 
Future
------

* Better navigation
* Provide a mechanism for creating new containers
* Provide a way to find and clean up dangling images
* Provide a way to see how containers based on a certain image are running in the environment
* Allow a more dynamic configuration or discovery of hosts
* Provide a caching mechanism for some of the host and container information so we don't have to incur so much cost on each page load
* Related to the above, read all host data on first launch but then leverage the cache plus docker events to update the information
* Continued code improvements
* Add more modules!

Screenshots
-----------

![Screenshot of Helmsman](http://s25.postimg.org/4f93r5s6n/Helmsman_screenshot.png)