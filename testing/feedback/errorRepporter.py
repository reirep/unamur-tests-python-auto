from testing.feedback.ErrorLog import ErrorLog


class ErrorReporter:
    def __init__(self):
        self.errors = []

    def add_error(self, error: ErrorLog):
        self.errors.append(error)

    def get_output(self):
        raise NotImplementedError
