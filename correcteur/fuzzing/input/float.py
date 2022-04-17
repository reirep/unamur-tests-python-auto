import random
import sys

from correcteur.fuzzing.input.input import Input


class Float(Input):

    def __init__(self, min_val=-sys.maxsize, max_val=sys.maxsize, mutation_range=10, additional_special=None):
        Input.__init__(self)
        if additional_special is None:
            additional_special = []
        self.min = min_val
        self.max = max_val
        self.specials = [0.0]
        self.mutation_range = mutation_range
        if additional_special:
            for additional in additional_special:
                self.specials.append(additional)

    def get_special_cases(self):
        return self.specials

    def mutate(self, value):
        return value + random.uniform(-self.mutation_range, self.mutation_range)

    def get_random(self):
        return random.uniform(-sys.maxsize, sys.maxsize)

    def is_valid_type(self, candidate):
        return isinstance(candidate, float)

    def integrate_by_type(self, candidates):
        for candidate in candidates:
            if isinstance(candidate, float):
                self.specials.append(candidate)
