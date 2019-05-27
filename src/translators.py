# Hook data builder for Docker Hub
def dockerhub(data, args):
    import json
    payload = json.loads(data)
    return {
        'repo': payload['repository']['repo_name'],
        'tag': payload['push_data']['tag'],
        'secret': args.get('secret'),
    }
