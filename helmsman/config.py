import lya

#from ConfigParser import SafeConfigParser


#parser = SafeConfigParser()

class Configuration:
    """

    """
    app_title = ''
    helmsman_port = 80
    registry_host = ''
    registry_port = 5000
    registry_protocol = ''
    registry_api_version = 0
    registry_json_path = "json"
    registry_strip_dir = True
    modules = {}
    data = lya.AttrDict

    def __init__(self):
        """
        Initialize our Configuration
        """

        config = lya.AttrDict.from_yaml('/opt/docker/helmsman/config/helmsman.yml')
        self.data = config
        self.app_title = config.helmsman.title
        self.helmsman_port = config.helmsman.port
        self.registry_host = config.registry.host
        self.registry_port = config.registry.port
        self.registry_protocol = config.registry.protocol
        self.registry_api_version = config.registry.api_version
        self.registry_json_path = config.registry.json_path
        self.registry_strip_dir = config.registry.strip_directory
        for a_module in config.modules:
            name = a_module.items()[0][0]
            self.modules[name] = a_module


        #for host in config.docker_hosts:
        #
        #    print '%s:%s' % (host.get('host'), host.get('port'))
