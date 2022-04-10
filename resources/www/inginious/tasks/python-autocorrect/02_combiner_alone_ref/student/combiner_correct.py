# importing the framework & dynamically importing the code of the student
import sys

from correcteur.feedback.textRepporter import TestRepporter
from correcteur.steps.StepsRunner import StepRunner
from correcteur.steps.Step import Step

sys.path.append('./student')

import student_code

# Quick'n'dirty ref code
ref_list = None


def init():
    global ref_list
    ref_list = []


def add(elem):
    global ref_list
    ref_list.append(elem)


def remove():
    global ref_list
    ref_list.pop()


def last():
    global ref_list
    return ref_list[-1]


# Run the fuzzer

reporter = TestRepporter()

runner = StepRunner(stop_on_first_error=True)
runner.add_step(Step(
    [
        init
    ],
    [
        student_code.init
    ],
    max_depth_local=1,
    nice_names=[
        "init"
    ]))

runner.add_step(Step(
    [
        lambda: add(6),
        remove,
        last
    ],
    [
        lambda: student_code.add(6),
        student_code.remove,
        student_code.last
    ],
    max_depth_local=10,
    nice_names=[
        "add",
        "remove",
        "last"
    ]))

runner.compare_codes(reporter)

# grab the results

if len(reporter.get_output()) == 0:
    print("ok")
else:
    print(reporter.get_text_output())
