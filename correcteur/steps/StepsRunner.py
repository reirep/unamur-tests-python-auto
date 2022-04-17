from correcteur.feedback.ErrorLog import ErrorLog
from correcteur.feedback.errorRepporter import ErrorReporter
from correcteur.steps.Step import Step
from correcteur.steps.exceptions.EndOfParse import EndOfParse


class StepRunner:

    def __init__(self, stop_on_first_failure=True, min_depth=1, max_depth=25, save_failed_case_on_exit=True,
                 max_seconds_execution=60, stop_on_first_error=False, allowed_errors=[]):
        self.steps = []
        self.stop_on_first_failure = stop_on_first_failure
        self.min_depth = min_depth
        self.max_depth = max_depth
        self.save_failed_case_on_exit = save_failed_case_on_exit
        self.max_seconds_execution = max_seconds_execution
        self.stop_on_first_error = stop_on_first_error
        self.allowed_errors = allowed_errors

    def add_step(self, step):
        """
        This will add a step to the current runner. THe added step will be placed after the previously
        defined ones
        :param step: the step that is going to be added
        """
        if not isinstance(step, Step):
            raise ValueError("the input should have been an instance of Step")

        self.steps.append(step)

    def get_step(self, index) -> Step:
        """
        Allow to fetch a given step
        :param index: the index of the step, indexed from 0
        :return: the step asked
        :raise ValueError: if the step asked for is not a legal one
        """
        if index < 0 or index >= len(self.steps):
            raise ValueError("the index does not match any of the available steps")

        return self.steps[index]

    def __exception_allowed__(self, e: Exception) -> bool:
        if not self.allowed_errors:
            return False

        for ex in self.allowed_errors:
            if isinstance(e, ex):
                return True

        return False

    @staticmethod
    def __unique_element__(array, element):
        for elem in array:
            if elem != element:
                return False
        return True

    def __exploration_rollback__(self, actions):
        """
        Will remove the last action and increment the one before that
        :param actions:
        :return:
        """
        while True:
            if not actions:
                raise EndOfParse("end of parse")

            if self.__unique_element__(actions[-1], self.steps[len(actions) - 1].get_nbr_possible_actions() - 1):
                if len(actions[-1]) == self.steps[len(actions) - 1].max_depth_local:
                    actions = actions[:-1]
                    continue
                actions[-1] = [0] * (len(actions[-1]) + 1)
                break

            for i in range(len(actions[-1]) - 1, -1, -1):
                if actions[-1][i] == self.steps[len(actions) - 1].get_nbr_possible_actions() - 1:
                    actions[-1][i] = 0
                else:
                    actions[-1][i] += 1
                    break

            break

        while len(actions) != len(self.steps):
            actions.append([0] * self.steps[len(actions)].min_depth_local)

        return actions

    def __generate_combinations__(self):
        """
        This function will yield the possible combinations of actions as an array of array
        The first case is the actions for the first step, etc ...
        :yield: the various possible combination of actions
        """
        if len(self.steps) == 0:
            raise ValueError("no step to test")

        # Currently, a dumb-as-a-rock bfs

        # Init
        actions = []
        while len(actions) != len(self.steps):
            actions.append([0] * self.steps[len(actions)].min_depth_local)

        # Parsing
        while True:
            yield actions

            # rollback; we have too much steps
            try:
                actions = self.__exploration_rollback__(actions)
            except EndOfParse:
                break

    def __actions_to_nice_name__(self, actions) -> str:
        res = ""

        for setIndex in range(len(actions)):
            step = self.get_step(setIndex)
            for actionIndex in range(len(actions[setIndex])):
                current = step.get_action_name(actions[setIndex][actionIndex])
                if not current:
                    return str(actions)
                if setIndex != 0 or actionIndex != 0:
                    res += " -> "
                res += current

        return res

    def compare_codes(self, reporter: ErrorReporter):

        for actions in self.__generate_combinations__():
            # build the execution fns we are going have this time
            fns = []
            for index in range(0, len(actions)):
                if not actions[index]:
                    fns.append([])
                    continue
                fns.append(self.steps[index].get_actions_list(actions[index]))

            # Execute the fns here and compare
            for step in fns:
                for action in step:
                    ref_return = None
                    ref_except = None

                    test_return = None
                    test_except = None

                    if action[0]:
                        try:
                            ref_return = action[0]()
                        except Exception as e:
                            ref_except = e

                    try:
                        test_return = action[1]()
                    except Exception as e:
                        test_except = e

                    if action[0]:
                        if not ref_except and self.__exception_allowed__(test_except):
                            return

                        if type(ref_except).__name__ != type(test_except).__name__:

                            if self.__exception_allowed__(test_except):
                                continue

                            if isinstance(test_except, Exception):
                                reporter.add_error(ErrorLog("combination runner", test_except,
                                                            "the tested code broke (appels: {})".format(
                                                                self.__actions_to_nice_name__(actions))))
                            elif isinstance(ref_except, Exception):
                                reporter.add_error(ErrorLog("combination runner", ref_except,
                                                            "the tested code did not raise an error when the ref code "
                                                            "did (appels: {})".format(
                                                                self.__actions_to_nice_name__(actions))))

                            if self.stop_on_first_error:
                                return
                            else:
                                continue

                        if ref_return != test_return:
                            reporter.add_error(ErrorLog("combination runner", None,
                                                        "the return of the reference code and the tested code differ "
                                                        "(ref: {} - test: {}) (appels: {})".format(ref_return,
                                                                                                   test_return,
                                                                                                   self.__actions_to_nice_name__(
                                                                                                       actions))))
                            if self.stop_on_first_error:
                                return
                    else:
                        if test_except and not self.__exception_allowed__(test_except):
                            reporter.add_error(
                                ErrorLog("combination runner", test_except, "the tested code did throw an error"))
