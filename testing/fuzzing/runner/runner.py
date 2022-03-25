from testing.fuzzing.Results import Result


class Runner:
    def __init__(self, fn, fn_validate, timeout_seconds, args):
        self.fn = fn
        self.fn_validate = fn_validate
        self.args = args
        self.timeout = timeout_seconds
        self.result = Result.UNAVAILABLE
        self.error = None

    def get_result(self):
        return self.result, self.error

    def get_score(self):
        raise NotImplementedError

    def run(self):
        raise NotImplementedError
