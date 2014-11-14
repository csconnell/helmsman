from helmsman import app, the_config
from flask import render_template, request, redirect, url_for

@app.route('/', methods=['GET'])
def homepage():
    
    modules = []
    print the_config.modules['Index_Manager'].get('name')
    for module in the_config.data.modules:
        if module.get('enabled') == True:
            modules.append({'Name': module.get('name'),
                            'Description': module.get('description'),
                            'Endpoint': module.get('endpoint')})
        

    print modules
    return render_template('home.html',
                            app_title=the_config.app_title,
                            modules=modules)