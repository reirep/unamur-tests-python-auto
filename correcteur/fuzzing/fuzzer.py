import copy
import random

from correcteur.feedback.errorRepporter import ErrorReporter
from correcteur.fuzzing.Results import Result
from correcteur.fuzzing.runner.line_runner import LineRunner
from correcteur.fuzzing.seed import Seed


def __create_base_seeds__(inputs):
    """
    this fn will create the combination af all the given input as arrays
    :param inputs: a bunch of object extending Input
    :return: the combinations of all specials cases as arrays
    """
    res = []

    for input_type in inputs:
        new_values = input_type.get_special_cases()

        if not res:
            for special_case in new_values:
                res.append([special_case])
            continue

        updated_res = []

        for line in res:
            for value in new_values:
                new_line = copy.deepcopy(line)
                new_line.append(value)
                updated_res.append(new_line)

        res = updated_res

    return res


def __convert_array_to_seeds__(arrays):
    res = []
    for array in arrays:
        res.append(Seed(array))
    return res


class Fuzzer:
    def __init__(self, fn, fn_validate, inputs, max_runs, timeout_execution):
        self.fn = fn
        self.fn_validate = fn_validate
        self.inputs = inputs
        self.timeout_execution = timeout_execution
        self.max_runs = max_runs

        self.runs = 0
        self.seeds = __convert_array_to_seeds__(__create_base_seeds__(inputs))

    def run_once(self, seed):
        r = LineRunner(self.fn, self.fn_validate,  self.timeout_execution, seed.get_values())
        r.run()
        seed.score = r.get_result()
        seed.set_score(r.get_score())
        seed.set_result(r.get_result())

    def run(self):
        # run all the seeds once
        for seed in self.seeds:
            self.run_once(seed)
            self.runs += 1

        # self.seeds.sort(reverse=True, key=lambda s: s.get_score())

        # continue to run for as long there is execution time left by mutating the top seeds
        while self.runs <= self.max_runs:
            # select one, the better the score the most chance it has to be selected
            weight = []
            for seed in self.seeds:
                weight.append(seed.get_score())

            selected_seed = random.choices(self.seeds, weights=weight)[0]

            # mutate the selected
            new_values = selected_seed.get_values()

            for i in range(len(new_values)):
                if self.inputs[i].can_mutate():
                    new_values[i] = self.inputs[i].mutate(new_values[i])
                else:
                    new_values[i] = new_values[i]

            # run it
            new_seed = Seed(new_values)

            self.run_once(new_seed)

            # insert it in the bunch of seeds we have

            self.seeds.append(new_seed)

            self.runs += 1

    def get_errors_seeds(self):
        res = []
        for seed in self.seeds:
            if seed.get_result() == Result.FAIL:
                res.append((seed.get_values(), seed.error))
        return res
