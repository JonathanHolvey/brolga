class Hook:
    """A container for translated webhook data"""

    def __init__(self, repo, tag, secret):
        self.repo = repo
        self.tag = tag
        self.secret = secret
