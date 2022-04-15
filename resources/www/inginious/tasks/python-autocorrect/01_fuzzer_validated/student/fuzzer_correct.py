# importing the framework & dynamically importing the code of the student
import sys

from correcteur.feedback.textRepporter import TestRepporter
from correcteur.fuzzing.fuzz import fuzz

sys.path.append('./student')

import student_code

# Reference function

def adder_validate(a:int, b:int, res:int):
    return res == a + b

# Run the fuzzer

reporter = TestRepporter()
valid_modules = ["student_code"]
fuzz(reporter, student_code.adder, adder_validate, valid_modules, runs=1000)

# grab the results

if len(reporter.get_output()) == 0:
    print("ok")
else:
    print(reporter.get_text_output())
