from glob import glob
import os

import yaml

"""Handle deployment of pushed Docker images"""
class Deploy:
    def __init__(self, path, logger):
        self.logger = logger
        self.path = path
        self.pattern = os.path.join(path, '**', 'docker-compose.yml')

    """Run all deployments"""
    def run(self, repo, tag):
        image = '{}:{}'.format(repo, tag)
        self.logger.info('Updating services using {}'.format(image))

        services = self.get_services(image)

    """Scan Docker Compose files for matching services"""
    def get_services(self, image):
        self.logger.info('Loading Docker Compose files from {}'.format(self.path))

        files = glob(self.pattern, recursive=True)

        services = []
        for filepath in files:
            services.extend(self.parse_compose_file(filepath))

    """Extract service and image names a from Docker Compose file"""
    def parse_compose_file(self, filepath):
        services = []
        try:
            with open(filepath, 'r') as stream:
                data = yaml.safe_load(stream)
        except yaml.YAMLError as error:
            self.logger.error(error)

        for name, service in data['services'].items():
            services.append({'name': name, 'image': service['image']})

        return services
