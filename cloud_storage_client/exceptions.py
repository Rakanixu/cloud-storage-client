

class IncorrectCredentialsException(Exception):
    def __init__(self, code, *args, **kwargs):
        self.id = code
        Exception.__init__(self, *args, **kwargs)
