# Hook data builder for Docker Hub
def dockerhub(request):
    import json
    payload = json.loads(request.data)
    repo = payload['repository']['repo_name']
    tag = payload['push_data']['tag']
    secret = request.args.get('secret')

    return repo, tag, secret
