# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# Press the green button in the gutter to run the script.
from resources.code_bidon import bidon, bidon_validate, bidon_deux, call_fn
from testing.feedback.errorRepporter import ErrorReporter
from testing.feedback.textRepporter import TestRepporter
from testing.fuzzing.fuzz import fuzz
from testing.fuzzing.input.int import Int
from testing.fuzzing.token.magic_token_finder import find_token
from testing.steps.Step import Step
from testing.steps.StepsRunner import StepRunner
from testing.symbolic.symbolic import analyse_file


# This one is kinda finished
def step_analyse(reporter: ErrorReporter):
    runner = StepRunner(stop_on_first_error=True)
    runner.add_step(Step([lambda: 0], [lambda: 0]))
    runner.add_step(Step([lambda: 0, lambda: 0], [lambda: 0, lambda: 1/0]))
    runner.add_step(Step([lambda: 0], [lambda: 0]))

    runner.compare_codes(reporter)


# This one is not finished at all
def analyse_semantic(reporter: ErrorReporter):
    analyse_file("resources/code_bidon.py", "lol")


# This one is on it's way
def fuzz_it(reporter: ErrorReporter, modu: [str]):
    fuzz(reporter, bidon, bidon_validate, [Int(), Int()], modu, runs=1000)


def token_finder(fn, modu):
    tokens = find_token(fn, modu)

    for token in tokens:
        print("token discovered: {}".format(token))


if __name__ == '__main__':
    valid_modules = ["resources.code_bidon"]

    token_finder(call_fn, valid_modules)
    #exit(0)

    reporter = TestRepporter()

    step_analyse(reporter)
    fuzz_it(reporter, valid_modules)

    for line in reporter.get_output():
        print(line)
