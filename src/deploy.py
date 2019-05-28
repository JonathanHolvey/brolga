from glob import glob
import os

import docker

"""Handle deployment of pushed Docker images"""
class Deploy:
    def __init__(self, path, logger):
        self.logger = logger
        self.path = path
        self.pattern = os.path.join(path, '**', 'docker-compose.yml')

    """Run all deployments"""
    def run(self, repo, tag):
        image = '{}:{}'.format(repo, tag)

        services = self.get_services(image)
        self.logger.info('Updating services \'{}\' using {}'.format(
            '\', \''.join([service['name'] for service in services]), image))

    """Scan Docker Compose files for matching services"""
    def get_services(self, image):
        self.logger.info('Loading Docker Compose files from {}'.format(self.path))

        compose_files = [docker.Compose(file) for file in glob(self.pattern, recursive=True)]

        services = []
        for file in compose_files:
            for name, service in file.get_property('services').items():
                if service['image'] == image:
                    services.append({'file': file.filepath, 'name': name})

        return services
