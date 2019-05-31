from subprocess import run
import yaml


class ComposeFile:
    """Parse a Docker Compose file and provide access to the data within"""

    def __init__(self, file):
        self.file = file
        self.data = None

    def parse(self, key):
        """Parse a root property into an array of tuples"""
        self._read()
        return self.data[key].items()

    def _read(self):
        """Load the compose file into a dictionary"""
        if self.data is not None:
            return
        try:
            with open(self.file, 'r') as stream:
                self.data = yaml.safe_load(stream)
        except yaml.YAMLError:
            raise Exception('An error occurred loading the Docker Compose file')

    def services(self):
        """Return an array of service objects"""
        return [ComposeService(self.file, name, config)
                for name, config in self.parse('services')]


class ComposeService:
    """Inspect and control Docker Compose services"""

    def __init__(self, file, name, config):
        self.cli = ComposeCLI(file, name)
        self.file = file
        self.name = name
        self.config = config

    def update(self):
        if not self.cli.status():
            raise Exception('The service is not running')


class ComposeCLI:
    """Wrapper for the Docker Compose CLI program"""

    def __init__(self, file, name):
        self.file = file
        self.name = name

    def status(self):
        """Get the status of a service"""
        count = len(self._run(['ps', '-q']))
        if count > 1:
            raise Exception('Ambiguous service when checking status')

        return count == 1

    def up(self):
        """Start a service"""
        return self._run(['up', '-d'])

    def down(self):
        """Stop a service"""
        return self._run(['down'])

    def pull(self):
        """Pull an image for a service"""
        return self._run(['pull'])

    def _run(self, cmd):
        """Run a Docker Compose command"""
        result = run(['docker-compose', '-f', self.file, *cmd, self.name],
                     capture_output=True)

        if result.returncode != 0:
            raise Exception(result.stderr)

        return result.stdout.decode('utf-8').strip().splitlines()
