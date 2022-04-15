# importing the framework & dynamically importing the code of the student
import sys

from correcteur.feedback.textRepporter import TestRepporter
from correcteur.steps.StepsRunner import StepRunner
from correcteur.steps.Step import Step

sys.path.append('./student')

import student_code
# Run the fuzzer

reporter = TestRepporter()

runner = StepRunner(stop_on_first_error=True)
runner.add_step(Step(
    [
        student_code.init
    ],
    None,
    max_depth_local=1,
    nice_names=[
        "init"
    ]))

runner.add_step(Step(
    [
        lambda: student_code.add(6),
        student_code.remove,
        student_code.last
    ],
    None,
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
