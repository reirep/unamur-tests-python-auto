import ast
import inspect
import textwrap
import sys


class TokenFinder:
    def __init__(self, allowed_modules, allowed_type=None):
        if allowed_type is None:
            self.allowed_type = ["int", "bool", "str"]
        else:
            self.allowed_type = allowed_type

        self.to_parse = []
        self.magic_token = set()
        self.allowed_modules = allowed_modules

    @staticmethod
    def __get_src__(f):
        try:
            return inspect.getsource(f)
        except OSError:
            print("failed to convert back the lambda to code")
            exit(-1)

    @staticmethod
    def __get_module__(obj):
        return inspect.getmodule(obj)

    def __get_fn__(self, fn_id):
        """
        Will return [] if the function has not been found.
        The role of this code is to resolve the potential fn from a module, not to
        check if the fn is valid
        will return all match. This can lead to confusion and some inefficiency but the context is not
        available from the call thus we shoot wide
        :param fn_id:
        :return:
        """

        res = []

        for module_str in self.allowed_modules:
            module = sys.modules[module_str]
            if hasattr(module, fn_id):
                res.append(getattr(module, fn_id))

        return res

    def __parse_element__(self):
        current = self.to_parse.pop()

        if type(current).__name__ in self.allowed_type:
            self.magic_token.add(current)

        if not self.__get_module__(current) or self.__get_module__(current).__name__ == "_ast":
            # current is a list / a tupple
            if isinstance(current, (list, tuple)):
                for elem in current:
                    self.to_parse.append(elem)
                return

            if hasattr(current, "__dict__"):
                for field in vars(current):
                    self.to_parse.append(getattr(current, field))

            if isinstance(current, ast.Call):
                fns = self.__get_fn__(current.func.id)
                if not fns:
                    return
                for fn in fns:
                    self.to_parse.append(ast.parse(__get_src__(fn)))

    def __analyse_function_root__(self, elements):
        for element in elements:
            self.to_parse.append(element)

        while len(self.to_parse) != 0:
            self.__parse_element__()

    def find_tokens(self, f):
        src = self.__get_src__(f)
        root_token_tree = ast.parse(textwrap.dedent(src)).body
        self.__analyse_function_root__(root_token_tree)

    def get_tokens(self):
        return self.magic_token
