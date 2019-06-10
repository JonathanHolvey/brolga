class BaseHook:
    """Base webhook for extending"""
    repo = None
    tag = None
    secret = None
    name = ''

    def __init__(self):
        """Set hook name"""
        pass

    def read(self, request):
        """Set hook properties from request data"""
        pass

    def done(self, result):
        """Run callback on deployment completion"""
        pass
