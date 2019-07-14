from subprocess import run
import yaml


class ComposeFile:
    """Parse a Docker Compose file and provide access to the data within"""

    def __init__(self, file):
        self.file = file
        self.data = None
        self.cli = ComposeCLI(file)

        self.services = [ComposeService(self.file, name, config)
                         for name, config in self.parse('services')]

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

    def active(self):
        """Check if a compose file has created containers"""
        return self.cli.status()

    def update(self, services):
        """Pull images then restart all services"""
        if self.cli.pull([s.name for s in services]):
            self.cli.down()
            self.cli.up()
        return self.cli.status()


class ComposeService:
    """Inspect Docker Compose services"""

    def __init__(self, file, name, config):
        self.file = file
        self.name = name
        self.config = config


class ComposeCLI:
    """Wrapper for the Docker Compose CLI program"""

    def __init__(self, file):
        self.file = file

    def status(self, service=''):
        """Get the status of a service"""
        return len(self._run(['ps', '-q']).splitlines()) > 0

    def up(self, service=''):
        """Start a service"""
        self._run(['up', '-d'])

    def down(self):
        """Stop a service"""
        self._run(['down'])

    def pull(self, services=[]):
        """Check for new images and return True if downloaded"""
        output = self._run(['pull', *services])
        return 'downloaded newer image' in output

    def _run(self, cmd):
        """Run a Docker Compose command"""
        result = run(['docker-compose', '-f', self.file, *cmd],
                     capture_output=True)

        if result.returncode != 0:
            raise Exception(result.stderr)

        return (result.stdout or result.stderr).decode('utf-8').strip()
