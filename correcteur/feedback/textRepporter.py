from correcteur.feedback.errorRepporter import ErrorReporter


class TestRepporter(ErrorReporter):

    def get_output(self) -> [str]:
        res = []
        for error in self.errors:
            res.append(
                "[{method}] The error \"{error}\" has been triggered with the inputs {input} ({msg})".format(
                    error=error.error, method=error.methode, input=error.inputs, msg=error.message))
        return res
