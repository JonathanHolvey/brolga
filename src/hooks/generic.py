from .base import BaseHook


class Generic(BaseHook):
    """Generic webhook handler"""

    def __init__(self):
        self.name = 'generic'

    def read(self, request):
        self.repo = request.args['repo']
        self.tag = request.args['tag']
        self.key = request.args['key']
