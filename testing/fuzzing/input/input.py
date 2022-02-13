
class Input:
    def __init__(self):
        pass

    def get_special_cases(self):
        """
        :return: an array of seed for this type of runner that represent base special cases
        """
        return []

    def get_random(self):
        raise NotImplementedError

    def mutate(self, value):
        raise NotImplementedError
