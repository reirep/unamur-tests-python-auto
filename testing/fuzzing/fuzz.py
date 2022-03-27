from testing.feedback.ErrorLog import ErrorLog
from testing.feedback.errorRepporter import ErrorReporter
from testing.fuzzing.fuzzer import Fuzzer
from testing.fuzzing.token.magic_token_finder import find_token


def fuzz(reporter: ErrorReporter, fn, fn_validate, inputs, timeout_execution=1, runs=10000):
    """
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
    candidates = find_token(fn)
    candidates.add(find_token(fn_validate))

    for input_type in inputs:
        input_type.integrate_by_type(candidates)


    # create the runner with the function given and start it
    r = Fuzzer(fn, fn_validate, inputs, runs, timeout_execution)
    r.run()
    input_fail = r.get_errors_seeds()

    for i in input_fail:
        reporter.add_error(ErrorLog("fuzzer", i[1], "the fuzzer broke the code with those inputs", i[0]))
