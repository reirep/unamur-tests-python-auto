import ast
import inspect
import textwrap

import astunparse

from correcteur.feedback.ErrorLog import ErrorLog
from correcteur.feedback.errorRepporter import ErrorReporter
from correcteur.fuzzing.exceptions.FunctionNotAnotatedError import FunctionNotAnotatedError
from correcteur.fuzzing.exceptions.SourceReversingError import SourceReversingError
from correcteur.fuzzing.fuzzer import Fuzzer
from correcteur.fuzzing.input.gen_from_str import get_type_from_str
from correcteur.fuzzing.token.universal_magic_token_finder import TokenFinder


def fuzz_explicit_arguments(reporter: ErrorReporter, fn, fn_validate, inputs, valid_modules, timeout_execution=1,
                            runs=10000, stop_on_first_error=True):
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
    parser = TokenFinder(valid_modules)

    parser.find_tokens(fn)
    if fn_validate:
        parser.find_tokens(fn_validate)

    for input_type in inputs:
        input_type.integrate_by_type(parser.get_tokens())

    # create the runner with the function given and start it
    r = Fuzzer(fn, fn_validate, inputs, runs, timeout_execution, stop_on_first_error)
    r.run()
    input_fail = r.get_errors_seeds()

    for i in input_fail:
        reporter.add_error(ErrorLog("fuzzer", i[1], "the fuzzer broke the code  (inputs: {})".format(i[0])))


def fuzz(reporter: ErrorReporter, fn, fn_validate, valid_modules, timeout_execution=1, runs=10000):
    types = __get_annotated_type__(fn)
    return fuzz_explicit_arguments(reporter, fn, fn_validate, types, valid_modules, timeout_execution, runs)


def __get_annotated_type__(fn):
    src = None
    try:
        src = inspect.getsource(fn)
    except OSError:
        raise SourceReversingError()

    res = []

    for arg in ast.parse(textwrap.dedent(src)).body[0].args.args:
        if not arg.annotation:
            raise FunctionNotAnotatedError()

        type_str = astunparse.unparse(arg).split(':')[1].strip()
        res.append(get_type_from_str(type_str))

    return res
