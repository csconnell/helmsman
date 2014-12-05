from flask import render_template, request, redirect, url_for
import requests
from helmsman import app, the_config, docker_hosts
import json

base_url = ('%s%s:%s/%s' % (the_config.registry_protocol,
                            the_config.registry_host,
                            the_config.registry_port,
                            the_config.registry_api_version))

app_title = the_config.app_title
module_title = the_config.modules['Index_Manager'].get('name')  #the_config.data.modules.Index_Manager.name

host_and_port = ('%s:%s' % (the_config.registry_host,
                            the_config.registry_port))

# This end point retrieves repo information from the registry remote API
#@app.route('/', methods=['GET'])
@app.route('/repos', methods=['GET'])
def get_repos_web():
    return find_repos()


@app.route('/repos', methods=['DELETE'])
def delete_repo():
    repository = request.args['repository']
    return_code = requests.delete(base_url + '/repositories/' + repository +'/',  allow_redirects=True).text
    print return_code
    return return_code


@app.route('/repos/search', methods=['POST', 'GET'])
def find_repos():

    headers = {'Accept': 'application/json'}
    json_to_return = ''
    criteria  = ''


    if request.method == 'POST':
        criteria = request.form['image_search']
        json_to_return = requests.get(base_url + '/search?q=' + criteria, headers=headers).json()
    else:
        json_to_return = requests.get(base_url + '/search', headers=headers).json()

    repos = []
    for repo in json_to_return['results']:
        tags = []

        tag_request = requests.get('%s/repositories/%s/tags' % (base_url, repo['name']), headers=headers)
        if tag_request.status_code == 404:
            tags.append({'Tag': 'No tags found'})
        else:
            for tag, image_id in tag_request.json().iteritems():
                image_link = base_url + '/images/' + image_id + '/json'
                tags.append({'Tag': tag, 'Image_ID': image_id, 'Image_Link': image_link, 'Short_ID': image_id[0:12]})

        # With the Lotame setup everything shows under library, this allows us to remove that
        if the_config.registry_strip_dir == True:
            repo_name = repo['name'].split('/')[1:][0]

        else:
            repo_name = repo['name']
        repos.append({'Name': repo_name,
                      'Description': repo['description'],
                      'Tags': tags})

    registry_version = get_registry_info()

    return render_template('repo_listing.html',
        repos=repos,
        app_title=app_title,
        module_title=module_title,
        host=host_and_port,
        criteria=criteria,
        registry_version=registry_version)


@app.route('/images/info/<string:image_id>', methods=['GET'])
def get_tag_info(image_id):
    headers = {'Accept': 'application/json'}
    json_to_return = requests.get(base_url + '/images/' + image_id + '/json', headers=headers).text
    return json_to_return


@app.route('/images/tags', methods=['POST'])
def tag_image():
    """Tags an image with the passed tag.  Expects the following parameters:

    Request arguments:
    image_id -- the id of the image to tag
    tag -- the tag name to associate with the image
    """
    headers = {'Accept': 'application/json'}
    image_id = request.form['tag_image_id']
    post_data = '"%s"' % (image_id)
    repository = request.form['tag_repository']
    tag = request.form['tag_name']
    return_code = requests.put(base_url + '/repositories/' + repository + '/tags/' + tag, data=post_data, headers=headers).status_code
    if return_code == requests.codes.ok:
            return redirect(url_for('find_repos'))
    else:
        return "some error" # Obviously we need to handle this better!


@app.route('/images/tags', methods=['DELETE'])
def delete_tag():
    """ This method is used for deleting tags, it expects the following arguments:

    Request arguments:
    repository -- the name of the respository from which to remove the tag
    tag -- the tag to remove
    """
    tag = request.args['tag']
    repository = request.args['repository']
    return_code = requests.delete(base_url + '/repositories/' + repository + '/tags/' + tag).text
    return return_code


def get_registry_info():
    headers = {'Accept': 'application/json'}
    registry_info = requests.get(base_url + '/_ping', headers=headers).headers
    return registry_info['X-Docker-Registry-Version']


@app.route('/images/create_containers', methods=['POST'])
def create_containers():

    image_id = request.form.get('create_tag_image_id')
    host_name = request.form.get('container_host_name')
    container_name = request.form.get('container_name')
    volumes = request.form.get('volumes')
    port_specs = request.form.get('port_specs')
    privileged = request.form.get('privileged')
    host=request.form.get('hosts')
    container_domain_name = request.form.get('container_domain_name')
    start_on_create = request.form.get('start_on_create')


    return docker_hosts.create_container(image_id = image_id,
                                         container_host_name = host_name,
                                         container_domain_name = container_domain_name,
                                         container_name = container_name,
                                         privileged = privileged,
                                         docker_host = host,
                                         port_specs = port_specs,
                                         volumes = volumes,
                                         start_on_create = start_on_create)
    
