import sys

from fuzzingbook.Coverage import Coverage

from testing.fuzzing.Results import Result
from testing.fuzzing.exceptions.TimeoutException import TimeoutException
from testing.fuzzing.runner.runner import Runner


# Copied and modified from the fuzzing book
class CoverageCustom:
    def __init__(self):
        self._trace = []
        self.original_trace_function = None

    def traceit(self, frame, event, arg):
        if self.original_trace_function is not None:
            self.original_trace_function(frame, event, arg)

        if event == "line":
            function_name = frame.f_code.co_name
            lineno = frame.f_lineno
            if function_name != '__exit__':
                self._trace.append((function_name, lineno))

        return self.traceit

    def __enter__(self):
        self.original_trace_function = sys.gettrace()
        sys.settrace(self.traceit)
        return self

    def __exit__(self, exc_type, exc_value, tb):
        sys.settrace(self.original_trace_function)
        return None

    def trace(self):
        return self._trace

    def coverage(self):
        return set(self.trace())


class LineRunner(Runner):
    def __init__(self, fn, fn_validate, timeout_seconds, args):
        super().__init__(fn, fn_validate, timeout_seconds, args)
        self.coverage = 0

    def get_score(self):
        return self.coverage

    def run(self):
        try:
            with Coverage() as cov:
                res = self.fn(*self.args)
            self.coverage = len(cov.coverage())

            if self.fn_validate(res):
                self.result = Result.PASS
            else:
                self.result = Result.FAIL
                self.error = Exception("the given output was not valid")
        except TimeoutException:
            self.result = Result.TIMEOUT
            self.coverage = 0
        except Exception as e:
            self.result = Result.FAIL
            self.error = e
