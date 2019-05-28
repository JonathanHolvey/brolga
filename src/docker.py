import yaml

class Compose:
    def __init__(self, filepath):
        self.filepath = filepath
        self.data = None

    """Parse the Docker Compose file"""
    def parse(self):
        if self.data is not None:
            return
        try:
            with open(self.filepath, 'r') as stream:
                self.data = yaml.safe_load(stream)
        except yaml.YAMLError as error:
            raise Exception('An error occurred loading the Docker Compose file')

    """Get a root property from the Docker Compose file by its key"""
    def get_property(self, key):
        self.parse()
        return self.data[key]

