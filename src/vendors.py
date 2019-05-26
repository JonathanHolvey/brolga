# Webhook translator for Docker Hub
def dockerhub(payload):
    return {
        'repo': payload['repository']['repo_name'],
        'tag': payload['push_data']['tag'],
    }
