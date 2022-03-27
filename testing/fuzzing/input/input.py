class Input:
    def __init__(self):
        pass

    def integrate_by_type(self, candidates):
        """
        Will take a list of candidates as an input and integrate the compatibles one as internal base seeds
        :param candidates: the set of potential candidates
        """
        raise NotImplementedError

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

    def can_mutate(self):
        """
        Will return if the type is able to be mutated
        """
        return True

    def mutate(self, value):
        """
        :param value: the base input
        :return: a new , mutated by a bit, value
        """
        raise NotImplementedError
