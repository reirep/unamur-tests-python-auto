import ast
import inspect
import textwrap

from testing.feedback.ErrorLog import ErrorLog
from testing.feedback.errorRepporter import ErrorReporter
from testing.fuzzing.exceptions.FunctionNotAnotatedError import FunctionNotAnotatedError
from testing.fuzzing.exceptions.SourceReversingError import SourceReversingError
from testing.fuzzing.fuzzer import Fuzzer
from testing.fuzzing.input.bool import Bool
from testing.fuzzing.input.int import Int
from testing.fuzzing.input.str import Str
from testing.fuzzing.token.magic_token_finder import find_token


def fuzz_explicit_arguments(reporter: ErrorReporter, fn, fn_validate, inputs, valid_modules, timeout_execution=1, runs=10000):
    """
    :param valid_modules: the list of modules that will be recursively parsed for magic tokens
    :param reporter: the error reporter that is going to be used to bring back up the errors
    :param fn: the function to test
    :param fn_validate: the function that given the output of fn will return true if the output is ok
    :param inputs: an array of object extending the input object representing the args of the function
    :param timeout_execution: each execution of the function will be done under a timeout in seconds, if it exceeds it,
        it will be considered a fail
    :param runs: max number of time the function may be run / tested
    :return: None
    """

    # find all the magic token and add them to the base inputs
    candidates = find_token(fn, valid_modules)
    for candidate in find_token(fn_validate, valid_modules):
        candidates.add(candidate)

    for input_type in inputs:
        input_type.integrate_by_type(candidates)

    # create the runner with the function given and start it
    r = Fuzzer(fn, fn_validate, inputs, runs, timeout_execution)
    r.run()
    input_fail = r.get_errors_seeds()

    for i in input_fail:
        reporter.add_error(ErrorLog("fuzzer", i[1], "the fuzzer broke the code with those inputs", i[0]))


def fuzz(reporter: ErrorReporter, fn, fn_validate, valid_modules, timeout_execution=1, runs=10000):
    types = __get_annoted_type__(fn)
    return fuzz_explicit_arguments(reporter, fn, fn_validate, types, valid_modules, timeout_execution, runs)


def __get_annoted_type__(fn):
    src = None
    try:
        src = inspect.getsource(fn)
    except OSError:
        raise SourceReversingError()

    res = []

    for arg in ast.parse(textwrap.dedent(src)).body[0].args.args:
        if not arg.annotation:
            raise FunctionNotAnotatedError()

        res.append(__get_type_from_str(arg.annotation.id))

    return res


def __get_type_from_str(name):
    if name == "int":
        return Int()
    if name == "bool":
        return Bool()
    if name == "str":
        return Str()
    raise NotImplementedError()
