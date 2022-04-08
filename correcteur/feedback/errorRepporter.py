from correcteur.feedback.ErrorLog import ErrorLog


class ErrorReporter:
    def __init__(self):
        self.errors = []

    def add_error(self, error: ErrorLog):
        self.errors.append(error)

    def get_output(self) -> [str]:
        raise NotImplementedError

    def get_text_output(self) -> str:
        res = ""

        if len(self.get_output()) != 0:
            for line in self.get_output():
                res += line
                res += "<br/>"
        return res
