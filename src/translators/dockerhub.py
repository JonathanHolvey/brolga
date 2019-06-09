import json


class Dockerhub:
    """Webhook translator for Dockerhub"""

    def __init__(self):
        self.name = 'Dockerhub'

    def readhook(self, request):
        payload = json.loads(request.data)
        repo = payload['repository']['repo_name']
        tag = payload['push_data']['tag']
        secret = request.args.get('secret')

        return repo, tag, secret
