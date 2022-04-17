# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# Press the green button in the gutter to run the script.
from resources.code_bidon import bidon, bidon_validate, bidon_deux, call_fn, bidon_vil, bidon_adder
from correcteur.feedback.errorRepporter import ErrorReporter
from correcteur.feedback.textRepporter import TestRepporter
from correcteur.fuzzing.fuzz import fuzz_explicit_arguments, fuzz
from correcteur.fuzzing.input.int import Int
from correcteur.fuzzing.token.magic_token_finder import find_token
from correcteur.steps.Step import Step
from correcteur.steps.StepsRunner import StepRunner
from correcteur.symbolic.symbolic import analyse_file


# This one is kinda finished
def step_analyse(reporter: ErrorReporter):
    runner = StepRunner(stop_on_first_error=True)
    runner.add_step(Step([lambda: 0], [lambda: 0]))
    runner.add_step(Step([lambda: 0, lambda: 1/0], [lambda: 0, lambda: 0]))
    runner.add_step(Step([lambda: 0], [lambda: 0]))

    runner.compare_codes(reporter)


# This one is not finished at all
def analyse_semantic(reporter: ErrorReporter):
    analyse_file("resources/code_bidon.py", "lol")


# This one is on it's way
def fuzz_it(reporter: ErrorReporter, modu: [str]):
    fuzz_explicit_arguments(reporter, bidon, bidon_validate, [Int(), Int()], modu, runs=1000)


def blind_fuzz(reporter: ErrorReporter, modu: [str]):
    fuzz(reporter, bidon_adder, bidon_validate, modu, runs=1000)


def blind_fuzz_noref(reporter: ErrorReporter, modu: [str]):
    fuzz(reporter, bidon_adder, None, modu, runs=1000)


def token_finder(fn, modu):
    tokens = find_token(fn, modu)

    for token in tokens:
        print("token discovered: {}".format(token))


if __name__ == '__main__':
    reporter = TestRepporter()
    valid_modules = ["resources.code_bidon"]

    blind_fuzz_noref(reporter, valid_modules)

    #token_finder(call_fn, valid_modules)

    #step_analyse(reporter)
    #fuzz_it(reporter, valid_modules)

    for line in reporter.get_output():
        print(line)
