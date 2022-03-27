import random
from testing.fuzzing.input.input import Input


class Int(Input):
    def get_special_cases(self):
        return [True, False]

    def get_random(self):
        bool(random.choice([True, False]))

    def can_mutate(self):
        return False

    def mutate(self, value):
        pass

    def integrate_by_type(self, candidates):
        pass

