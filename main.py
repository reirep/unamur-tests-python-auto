# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# Press the green button in the gutter to run the script.
from testing.steps.Step import Step
from testing.steps.StepsRunner import StepRunner

if __name__ == '__main__':
    runner = StepRunner()
    runner.add_step(Step([lambda x: x], [lambda x: x]))
    runner.add_step(Step([lambda x: x, lambda x: x], [lambda x: x, lambda x: x]))
    runner.add_step(Step([lambda x: x], [lambda x: x]))

    for poss in runner.__generate_combinations__():
        print(poss)
