from helmsman import app, the_config
from flask import render_template, request, redirect, url_for, jsonify
import requests
from datetime import date
import json


app_title = the_config.app_title
module_title = the_config.modules['Host_Manager'].get('name') #the_config.data.modules.Host_Manager.name

@app.route('/hosts', methods=['GET'])
def get_docker_host_list():
    host_collection = []
    #headers = {'Accept': 'application/json'}
    for host in the_config.data.docker_hosts:
        host_collection.append({'Host': host.get('host')})

    print host_collection
    #return jsonify(host_collection)
    return json.dumps(host_collection)


@app.route('/hosts/info', methods=['GET'])
def get_docker_hosts_info():

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


#def create_container(the_data):
def create_container(docker_host,
                     container_host_name,
                     container_domain_name,
                     image_id,
                     container_name,
                     volumes,
                     port_specs,
                     privileged=False,
                     start_on_create=False):

    #ports = {}
    #for port_spec in port_specs.split('\n'):
        #pos = port_spec.index(':')
        #port_def.append()
        #ports[port_spec[:pos]] = port_spec[pos + 1:]
    #    ports['ports'] = port_spec

    volume_list = {}
    for volume in volumes.split('\n'):
        pos = volume.index(':')
        volume_list[volume[:pos]] = volume[pos + 1:]


    post_data = {'Hostname': container_host_name,
                 'Domainname': container_domain_name,
                 'Image': image_id,
                 'Volumes': volume_list}
    #             'ExposedPorts': ports}

    print post_data

    for a_host in the_config.data.docker_hosts:
        if (a_host.get('host') == docker_host):
            base_url = ('http://%s:%s' % ( a_host.get('host') ,a_host.get('port') ))

    param_data = 'name=%s' % container_name

    # Get the configuration information
    response = requests.post(base_url + '/containers/create', json=post_data, params=param_data)


    if ( response.status_code in [200, 201] ) and ( start_on_create == 'on'):
        start_container(docker_host, response.json()['Id'])
        
        return 'Created Container - %s' % response.json()
    elif not start_on_create == 'on':
        return 'Created container but did not start it - %s' % response.text
    else:
        return 'Did not create container - %s' % response.text
    

    