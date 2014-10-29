import os
from ConfigParser import SafeConfigParser
from flask import Flask, render_template, request, redirect, url_for
import requests

parser = SafeConfigParser()
app = Flask(__name__)

parser.read('/opt/docker/repo_viewer/config/repo.cfg')
base_url = parser.get('repo', 'protocol')  \
    + parser.get('repo', 'host') + ':' \
    + parser.get('repo', 'port') + '/' \
    + parser.get('repo', 'api_version')

app_title = parser.get('index', 'title')
host_and_port = parser.get('repo', 'host') + ':' \
    + parser.get('repo', 'port')


# This end point retrieves repo information from the registry remote API
@app.route('/', methods=['GET'])
@app.route('/repos', methods=['GET'])
def get_repos_web():
    return find_repos()


@app.route('/repos', methods=['DELETE'])
def delete_repo():
    repository = request.args['repository']
    return_code = requests.delete(base_url + '/repositories/' + repository +'/',  allow_redirects=True).text
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

        #tag_request = requests.get(base_url + '/repositories/' + repo['name'] + '/tags', headers=headers)
        tag_request = requests.get('%s/repositories/%s/tags' % (base_url, repo['name']), headers=headers)
        if tag_request.status_code == 404:
            tags.append({'Tag': 'No tags found'})
        else:
            for tag, image_id in tag_request.json().iteritems():
                image_link = base_url + '/images/' + image_id + '/json'
                tags.append({'Tag': tag, 'Image_ID': image_id, 'Image_Link': image_link, 'Short_ID': image_id[0:12]})

        # With the Lotame setup everything shows under library, this allows us to remove that
        if parser.getboolean('repo', 'strip_directory') == True:
            repo_name = repo['name'].split('/')[1:][0]

        else:
            repo_name = repo['name']
        repos.append({'Name': repo_name,
                      'Description': repo['description'],
                      'Tags': tags})
    return render_template('repo_listing.html', repos=repos, app_title=app_title, host=host_and_port, criteria=criteria)


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


if __name__ == '__main__':

    port = int(os.environ.get('PORT', parser.get('index', 'port')))
    app.debug = True
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.run(host='0.0.0.0', port=port)

##
## Notes - this is for a local registry with no namespace
## /search is for getting the list of repos
## /search/q=[search term] is for getting repos that meet the search
## /repositories/[repo name]/tags is for retrieving tags on a repo
## /images/[image id]/json will get you the data for an image
## /images/[image id]/ancestry will get you the lineage for the image
## PUT /v1/repositories/(namespace)/(repository)/tags/(tag*) is for setting a tag
## DELETE /v1/repositories/(namespace)/(repository)/tags/(tag*) is for deleting a tag
## DELETE /v1/repositories/(namespace)/(repository)/ is for deleting a repo