import random

from testing.fuzzing.input.input import Input


class Str(Input):
    def __init__(self, additional_special=None, char_min=32, char_max=126, max_size=100):
        Input.__init__(self)
        self.min_char = char_min
        self.max_char = char_max
        self.max_size = max_size
        self.specials = [""]
        for special in additional_special:
            self.specials.append(special)

    def get_special_cases(self):
        return self.specials

    def get_random(self):
        res = ""
        for i in range(self.max_size):
            res += str(random.randint(self.min_char, self.max_char))
        return res

    def __delete_char__(self, string):
        index = random.randint(0, len(string)-1)
        return string[:index] + string[index+1:]

    def __add_char__(self, string):
        index = random.randint(0, len(string)-1)
        return string[:index] + str(random.randint(self.min_char, self.max_char)) + string[index+1:]

    def __edit_char__(self, string):
        index = random.randint(0, len(string)-1)
        string[index] = str(random.randint(self.min_char, self.max_char))

    def mutate(self, value):
        modifiers = []

        if len(value) != 0:
            modifiers.append(self.__delete_char__)
            modifiers.append(self.__edit_char__)
        if len(value) < self.max_size:
            modifiers.append(self.__add_char__)

        return modifiers[random.randint(0, len(modifiers)-1)](value)

