from glob import glob
import os
import re

import docker


class Deploy:
    """Handle deployment of pushed Docker images"""

    def __init__(self, path, logger):
        self.logger = logger
        self.path = path

    def run(self, repo, tag):
        """Run all deployments"""
        image = '{}:{}'.format(repo, tag)

        services = self.get_services(image)
        self.logger.info('Updating services {} using {}'.format(
            ', '.join(["'{}'".format(self.get_id(s)) for s in services]), image))

    def get_services(self, image):
        """Scan Docker Compose files for matching services"""
        self.logger.info('Loading Docker Compose files from {}'.format(self.path))

        filenames = ['docker-compose.yml', 'docker-compose.yaml']
        patterns = [os.path.join(self.path, '**', f) for f in filenames]

        files = [f for p in patterns for f in glob(p, recursive=True)]

        return [s for f in files for s in docker.ComposeFile(f).services()
                if s.config.get('image') == image]

    def get_id(self, service):
        """Create an ID from the compose file path and service name"""
        folder = os.path.dirname(service.file)
        service_id = os.path.join(folder, service.name)

        pattern = r'^' + self.path + os.sep
        return re.sub(pattern, '', service_id)
