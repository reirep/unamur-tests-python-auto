import random

from correcteur.fuzzing.input.input import Input


def __get_rand_index__(array):
    if not array or len(array) == 0:
        return None
    if len(array) == 1:
        return 0
    return random.randint(0, len(array)-1)


class List(Input):

    def __init__(self, internal_type: Input, min_len: int = 0, max_len : int = 10, additional_special=None):
        super().__init__()
        self.internal = internal_type
        self.min = min_len
        self.max = max_len
        self.specials = []

        if additional_special:
            for additional in additional_special:
                self.specials.append(additional)

    def integrate_by_type(self, candidates):
        for candidate in candidates:
            if type(candidate) is list:
                if self.__check_content__(candidate):
                    self.specials.append(candidate)

    def is_valid_type(self, candidate):
        if not isinstance(candidate, list):
            return False
        return self.__check_content__(candidate)

    def get_random(self):
        res = [None] * random.randint(self.min, self.max)
        for i in range(len(res)):
            res[i] = self.internal.get_random()
        return res

    def get_special_cases(self):
        return [[]]

    def mutate(self, value):
        if bool(random.getrandbits(1)):
            if len(value) > 0:
                value.insert(__get_rand_index__(value), self.internal.get_random())
                return value
            else:
                value = [self.internal.get_random()]
                return value

        if len(value) > 0 and bool(random.getrandbits(1)):
            index = __get_rand_index__(value)
            value[index] = self.internal.mutate(value[index])

        if len(value) > 0 and bool(random.getrandbits(1)):
            value.pop(__get_rand_index__(value))

    def __check_content__(self, array):
        if not array:
            return False
        for elem in array:
            if not self.internal.is_valid_type(elem):
                return False
        return True

