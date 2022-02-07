# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# Press the green button in the gutter to run the script.
from testing.steps.Step import Step
from testing.steps.StepsRunner import StepRunner
from testing.symbolic.symbolic import analyse_file

if __name__ == '__main__':
    analyse_file("resources/code_bidon.py", "lol")


def step_analyse():
    runner = StepRunner(stop_on_first_error=True)
    runner.add_step(Step([lambda: 0], [lambda: 0]))
    runner.add_step(Step([lambda: 0, lambda: 0], [lambda: 0, lambda: 1/0]))
    runner.add_step(Step([lambda: 0], [lambda: 0]))

    runner.compare_codes()
