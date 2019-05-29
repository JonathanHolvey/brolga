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
        self.file = file
        self.name = name
        self.config = config
