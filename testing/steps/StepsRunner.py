from testing.steps.Step import Step


class StepRunner:

    def __init__(self, stop_on_first_failure=True, min_depth=1, max_depth=25, save_failed_case_on_exit=True,
                 max_seconds_execution=60):
        self.steps = []
        self.stop_on_first_failure = stop_on_first_failure
        self.min_depth = min_depth
        self.max_depth = max_depth
        self.save_failed_case_on_exit = save_failed_case_on_exit
        self.max_seconds_execution = max_seconds_execution

    def add_step(self, step):
        if not isinstance(step, Step):
            raise ValueError("the input should have been an instance of Step")

        self.steps.append(step)

    def get_step(self, index):
        if index < 0 or index >= len(self.steps):
            raise ValueError("the index does not match any of the available steps")

        return self.steps[index]

    def compare_solutions(self):

        if len(self.steps) == 0:
            raise ValueError("no step toi test")

