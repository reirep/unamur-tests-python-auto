from correcteur.feedback.errorRepporter import ErrorReporter


class TestRepporter(ErrorReporter):

    def get_output(self) -> [str]:
        res = []
        for error in self.errors:
            res.append(
                "[{method}] {msg} (Error: \"{error}\")".format(
                    error=error.error, method=error.methode, msg=error.message))
        return res
