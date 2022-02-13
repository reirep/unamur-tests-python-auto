import random
import sys

from testing.fuzzing.input.input import Input


class Int(Input):

    def __init__(self, min_val=-sys.maxsize, max_val=sys.maxsize, mutation_range=10):
        Input.__init__(self)
        self.min = min_val
        self.max = max_val
        self.mutation_range = mutation_range

    def get_special_cases(self):
        return [0, self.min, self.max]

    def mutate(self, value):
        return value + random.randint(-self.mutation_range, self.mutation_range)

    def get_random(self):
        return random.randint(-sys.maxsize, sys.maxsize)
