
class BadURLException(Exception):
    def __init__(self, message):
        super().__init__(f'URL is not valid: {message}')