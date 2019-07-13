from glob import glob
import os
import re

import docker


class Deploy:
    """Handle deployment of pushed Docker images"""

    def __init__(self, path, logger):
        self.logger = logger
        self.path = path

    def run(self, hook):
        """Update all matching images in Docker Compose files"""
        image = '{}:{}'.format(hook.repo, hook.tag)
        compose_files = self.get_files()
        result = DeployResult()

        for file in compose_files:
            folder = self.get_path(file.file)

            # Check that a serivce is using the image
            services = [s for s in file.services if s.config.get('image') == image]
            if not services or not file.active():
                continue

            self.logger.info('Updating {} {} {} in {} using {}'.format(
                len(services), 'service' if len(services) == 1 else 'services',
                ', '.join([s.name for s in services]), folder, image))
            try:
                file.update(services)
                result.success(services)
                self.logger.info('Finished updating {}'.format(folder))
            except Exception as error:
                result.error(services)
                self.logger.warning('Could not update {}. {}'.format(folder, error))

        if not result.matched():
            self.logger.info('No active services using {}'.format(image))

        hook.done(result)

    def get_files(self):
        """Scan folder for matching Docker Compose files"""
        self.logger.info('Loading Docker Compose files from {}'.format(self.path))

        filenames = ['docker-compose.yml', 'docker-compose.yaml']
        patterns = [os.path.join(self.path, '**', f) for f in filenames]

        return [docker.ComposeFile(f) for p in patterns for f in glob(p, recursive=True)]

    def get_path(self, file):
        """Get the relative folder path for the specified Docker Compose file"""
        folder = os.path.dirname(file)

        pattern = r'^' + self.path + os.sep
        return re.sub(pattern, '', folder)


class DeployResult:
    """Accumilate the status of deployed services"""

    failed = []
    deployed = []

    def error(self, services):
        """Mark services as failed"""
        self.failed.extend(services)

    def success(self, services):
        """Mark services as deployed"""
        self.deployed.extend(services)

    def matched(self):
        """Check if any services were marked"""
        return self.failed or self.deployed
