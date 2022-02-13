import copy

from testing.fuzzing.Results import Result


class Seed:
    def __init__(self, values):
        self.score = 0
        self.values = values
        self.result = Result.UNAVAILABLE

    def get_score(self):
        if self.result == Result.PASS:
            return self.score
        return 0

    def set_score(self, score):
        self.score = score

    def get_result(self):
        return self.result

    def set_result(self, result):
        self.result = result

    def get_values(self):
        return copy.deepcopy(self.values)
