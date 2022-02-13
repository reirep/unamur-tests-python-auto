# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# Press the green button in the gutter to run the script.
from resources.code_bidon import bidon, bidon_validate
from testing.fuzzing.fuzz import fuzz
from testing.fuzzing.input.int import Int
from testing.steps.Step import Step
from testing.steps.StepsRunner import StepRunner
from testing.symbolic.symbolic import analyse_file

from fuzzingbook.Coverage import Coverage


# This one is kinda finished
def step_analyse():
    runner = StepRunner(stop_on_first_error=True)
    runner.add_step(Step([lambda: 0], [lambda: 0]))
    runner.add_step(Step([lambda: 0, lambda: 0], [lambda: 0, lambda: 1/0]))
    runner.add_step(Step([lambda: 0], [lambda: 0]))

    runner.compare_codes()


# This one is not finished at all
def analyse_semantic():
    analyse_file("resources/code_bidon.py", "lol")


# This one is on it's way
def fuzz_it():
    fuzz(bidon, bidon_validate, [Int(), Int()], runs=1000)


if __name__ == '__main__':
    fuzz_it()

    with Coverage() as cov:
        pass
