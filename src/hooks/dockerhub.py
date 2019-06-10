import json
import requests

from .base import BaseHook


class Dockerhub(BaseHook):
    """Webhook translator for Dockerhub"""

    def __init__(self):
        self.name = 'Dockerhub'

    def read(self, request):
        payload = json.loads(request.data)
        self.repo = payload['repository']['repo_name']
        self.tag = payload['push_data']['tag']
        self.secret = request.args.get('secret')
        self.callback_url = payload['callback_url']

    def done(self, result):
        """Post status to callback URL"""
        state = 'error' if result.errors else 'success' if result.deployed else 'failure'
        requests.post(self.callback_url, json={'state': state})
