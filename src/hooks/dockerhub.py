from .base import BaseHook
import json


class Dockerhub(BaseHook):
    """Webhook translator for Dockerhub"""

    def __init__(self):
        self.name = 'Dockerhub'

    def read(self, request):
        payload = json.loads(request.data)
        self.repo = payload['repository']['repo_name']
        self.tag = payload['push_data']['tag']
        self.secret = request.args.get('secret')
