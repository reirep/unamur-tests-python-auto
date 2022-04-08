from correcteur.steps.exceptions.IllegalAction import IllegalAction
from correcteur.steps.exceptions.IncompatibleRequestForConfig import IncompatibleRequestForConfig


class Step:

    def __init__(self, actions_array_reference, actions_array_tested, min_depth_local=1, max_depth_local=3):
        """
        This object represents a set of operation that can be done at a given step

        :param actions_array_reference: an array of lambda that are the reference actions
        :param actions_array_tested: an array of lambda that are the tested actions
        :param min_depth_local: the minimum number of action of this step that will be executed one after the other
        :param max_depth_local: the maximum number of action of this step that will be executed one after the other
        """
        self.max_depth_local = max_depth_local
        self.min_depth_local = min_depth_local
        self.actions_array_reference = actions_array_reference
        self.actions_array_tested = actions_array_tested

    def get_nbr_possible_actions(self):
        """
        This function will return how many different action this step can execute
        :return:
        """
        return len(self.actions_array_reference)

    def get_actions_list(self, actions):
        """
        This function will take as an input a list of action as referenced by their number

        :param actions: this array of int represent witch actions the function will chain for the
        :return: an array of lambda that, when executed in the right order will execute the actions
            as requested in the input.
            the output is zipped with the first member of each tuple is the reference implementation and
            the second is the tested code.
        """

        if len(actions) < self.min_depth_local or len(actions) > self.max_depth_local:
            raise IncompatibleRequestForConfig

        ref = []
        test = []

        for action in actions:
            if action < 0 or action >= self.get_nbr_possible_actions():
                raise IllegalAction

            ref.append(self.actions_array_reference[action])
            test.append(self.actions_array_tested[action])

        return zip(ref, test)
