from flask import Flask

from reverse_proxy_app import ReverseProxyApp
from config import Configuration


# initialize the flask app
app = Flask(__name__)

# Use the ReverseProxyApp to allow use of a prefix supplied by the server
# See ReverseProxyApp.py
app.wsgi_app = ReverseProxyApp(app.wsgi_app)

# We need a secret key
app.secret_key = 'A0ZCs71C/Mk71C!Bl02C!Jm06CWX/,?RT'

# Set up the configuration
the_config = Configuration()

# Get our views and models
from helmsman import docker_index, home, docker_hosts

# Allows running from GUnicorn uWSGI, etc.
# It can still also be run from run.py without this interfering.
if __name__ == '__main__':
    app.run()
