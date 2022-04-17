import random
from correcteur.fuzzing.input.input import Input


class Bool(Input):
    def get_special_cases(self):
        return [True, False]

    def get_random(self):
        bool(random.choice([True, False]))

    def can_mutate(self):
        return False

    def mutate(self, value):
        pass

    def is_valid_type(self, candidate):
        return isinstance(candidate, bool)

    def integrate_by_type(self, candidates):
        pass

