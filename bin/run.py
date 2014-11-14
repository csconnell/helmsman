#!flask/bin/python
import os
from helmsman import app, the_config

port = int(os.environ.get('PORT', the_config.helmsman_port))
app.debug = True
app.run(host='0.0.0.0', port=port)