# importing the framework & dynamically importing the code of the student
import sys

from correcteur.feedback.textRepporter import TestRepporter
from correcteur.fuzzing.fuzz import fuzz

sys.path.append('./student')

import student_code

# Run the fuzzer

reporter = TestRepporter()
valid_modules = ["student_code"]
fuzz(reporter, student_code.adder, None, valid_modules, runs=1000)

# grab the results

if len(reporter.get_output()) == 0:
    print("ok")
else:
    print(reporter.get_text_output())
