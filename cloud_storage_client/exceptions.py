class IncorrectCredentialsException(Exception):
    def __init__(self, code, *args, **kwargs):
        self.id = code
        Exception.__init__(self, *args, **kwargs)


class NotFoundException(Exception):
    def __init__(self, code, *args, **kwargs):
        self.id = 404


class UploadException(Exception):
    def __init__(self, code, *args, **kwargs):
        self.id = code
        Exception.__init__(self, *args, **kwargs)