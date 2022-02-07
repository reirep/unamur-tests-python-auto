from testing.steps.Step import Step
from testing.steps.exceptions.EndOfParse import EndOfParse


class StepRunner:

    def __init__(self, stop_on_first_failure=True, min_depth=1, max_depth=25, save_failed_case_on_exit=True,
                 max_seconds_execution=60, stop_on_first_error=False):
        self.steps = []
        self.stop_on_first_failure = stop_on_first_failure
        self.min_depth = min_depth
        self.max_depth = max_depth
        self.save_failed_case_on_exit = save_failed_case_on_exit
        self.max_seconds_execution = max_seconds_execution
        self.stop_on_first_error=stop_on_first_error

    def add_step(self, step):
        """
        This will add a step to hte current runner. THe added step will be placed after the previously
        defined ones
        :param step: the step that is going to be added
        """
        if not isinstance(step, Step):
            raise ValueError("the input should have been an instance of Step")

        self.steps.append(step)

    def get_step(self, index):
        """
        Allow to fetch a given step
        :param index: the index of the step, indexed from 0
        :return: the step asked
        :raise ValueError: if the step asked for is not a legal one
        """
        if index < 0 or index >= len(self.steps):
            raise ValueError("the index does not match any of the available steps")

        return self.steps[index]

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

            if self.__unique_element__(actions[-1], self.steps[len(actions)-1].get_nbr_possible_actions()-1):
                if len(actions[-1]) == self.steps[len(actions)-1].max_depth_local:
                    actions = actions[:-1]
                    continue
                actions[-1] = [0] * (len(actions[-1]) + 1)
                break

            for i in range(len(actions[-1])-1, -1, -1):
                if actions[-1][i] == self.steps[len(actions)-1].get_nbr_possible_actions()-1:
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

    def compare_codes(self):

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
                    ref_except = False
                    test_except = False

                    try:
                        action[0]()
                    except Exception:
                        ref_except = True

                    try:
                        action[1]()
                    except Exception:
                        test_except = True

                    if ref_except != test_except:
                        if test_except:
                            print("Found a way to make the student code break", actions)
                        elif ref_except:
                            print("the tested code did not raised an error when the ref code did", actions)

                        if self.stop_on_first_error:
                            return




