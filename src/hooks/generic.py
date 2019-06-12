from .base import BaseHook


class Generic(BaseHook):
    """Generic webhook handler"""

    def __init__(self):
        self.name = 'generic'

    def read(self, request):
        self.repo = request.args.get('repo')
        self.tag = request.args.get('tag')
        self.key = request.args.get('key')
