from .base import BaseHook


class Generic(BaseHook):
    """Generic webhook translator"""

    def __init__(self):
        self.name = 'generic'

    def read(self, request):
        self.repo = request.args.get('repo')
        self.tag = request.args.get('tag')
        self.secret = request.args.get('secret')
