
class Input:
    def __init__(self):
        pass

    def get_special_cases(self):
        """
        :return: an array of seed for this type of runner that represent base special cases
        """
        return []

    def get_random(self):
        """
        :return: a new, completely random seed for this input
        """
        raise NotImplementedError

    def mutate(self, value):
        """
        :param value: the base input
        :return: a new , mutated by a bit, value
        """
        raise NotImplementedError
