from helmsman import app, the_config
from flask import render_template, request, redirect, url_for, jsonify
import requests
from datetime import date


app_title = the_config.app_title
module_title = the_config.modules['Host_Manager'].get('name') #the_config.data.modules.Host_Manager.name


@app.route('/hosts', methods=['GET'])
def get_docker_hosts():

    host_collection = []
    headers = {'Accept': 'application/json'}
    for host in the_config.data.docker_hosts:
        base_url = ('http://%s:%s' % ( host.get('host') ,host.get('port') ))

        host_info = requests.get(base_url + '/info', headers=headers).json()
        host_version = requests.get(base_url + '/version', headers=headers).json()
        active_containers = len(requests.get(base_url + '/containers/json', headers=headers).json())
        total_images = len(requests.get(base_url + '/images/json?all=1', headers=headers).json())
        host_collection.append({'Host': host.get('host'),
                                'Host_Info': host_info,
                                'Version_Info': host_version,
                                'Running_Containers': active_containers,
                                'Total_Images': total_images})

    return render_template('docker_hosts.html',
                           hosts=host_collection,
                           app_title=app_title,
                           module_title=module_title)


@app.route('/hosts/<string:the_host>/containers/active', methods=['GET'])
def get_active_containers(the_host):
    headers = {'Accept': 'application/json'}

    containers = []
    for a_host in the_config.data.docker_hosts:
        if (a_host.get('host') == the_host):
            base_url = ('http://%s:%s' % ( a_host.get('host') ,a_host.get('port') ))

    active_containers = requests.get(base_url + '/containers/json', headers=headers).json()

    # Do some transformation work on the JSON here before passing it on
    for container in active_containers:
        containers.append({'Names': container['Names'],
                           'Status': container['Status'],
                           'Created': date.fromtimestamp(container['Created']),
                           'Image': container['Image'],
                           'Ports': container['Ports'],
                           'Command': container['Command'],
                           'Id': container['Id'][0:12]})

    return render_template('containers.html',
                           host=the_host,
                           containers=containers,
                           app_title=app_title,
                           module_title=module_title,
                           scope='Active')


@app.route('/hosts/<string:the_host>/containers/all', methods=['GET'])
def get_all_containers(the_host):
    headers = {'Accept': 'application/json'}

    containers = []
    for a_host in the_config.data.docker_hosts:
        if (a_host.get('host') == the_host):
            base_url = ('http://%s:%s' % ( a_host.get('host') ,a_host.get('port') ))

    all_containers = requests.get(base_url + '/containers/json?all=1', headers=headers).json()

    # Do some transformation work on the JSON here before passing it on
    for container in all_containers:
        containers.append({'Names': container['Names'],
                           'Status': container['Status'],
                           'Created': date.fromtimestamp(container['Created']),
                           'Image': container['Image'],
                           'Ports': container['Ports'],
                           'Command': container['Command'],
                           'Id': container['Id'][0:12]})

    return render_template('containers.html',
                           host=the_host,
                           containers=containers,
                           app_title=app_title,
                           module_title=module_title,
                           scope='All')


@app.route('/hosts/<string:the_host>/containers/<string:container_id>/start', methods=['POST'])
def start_container(the_host, container_id):
    
    for a_host in the_config.data.docker_hosts:
        if (a_host.get('host') == the_host):
            base_url = ('http://%s:%s' % ( a_host.get('host') ,a_host.get('port') ))

    return_code = requests.post(base_url + '/containers/' + container_id + '/start').text
    return 'Container Started'


@app.route('/hosts/<string:the_host>/containers/<string:container_id>/stop', methods=['POST'])
def stop_container(the_host, container_id):
    for a_host in the_config.data.docker_hosts:
        if (a_host.get('host') == the_host):
            base_url = ('http://%s:%s' % ( a_host.get('host') ,a_host.get('port') ))

    return_code = requests.post(base_url + '/containers/' + container_id + '/stop').text
    return 'Container Stopped'


@app.route('/hosts/<string:the_host>/containers/<string:container_id>/remove', methods=['DELETE'])
def remove_container(the_host, container_id):

    for a_host in the_config.data.docker_hosts:
        if (a_host.get('host') == the_host):
            base_url = ('http://%s:%s' % ( a_host.get('host') ,a_host.get('port') ))

    return_code = requests.delete(base_url + '/containers/' + container_id).text
    return ' Container Removed'


@app.route('/hosts/<string:the_host>/containers/<string:container_id>/restart', methods=['POST'])
def restart_container(the_host, container_id):
    for a_host in the_config.data.docker_hosts:
        if (a_host.get('host') == the_host):
            base_url = ('http://%s:%s' % ( a_host.get('host') ,a_host.get('port') ))

    return_code = requests.post(base_url + '/containers/' + container_id + '/restart').text
    return 'Container Stopped'
