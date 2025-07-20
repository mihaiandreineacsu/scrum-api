# Define a custom exception class
class PositionException(Exception):
    def __init__(self, message, status_code, error):
        super().__init__(message)
        self.status_code = status_code
        self.error = error
