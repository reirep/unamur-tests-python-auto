import ast
import copy
import inspect
import sys
import textwrap

import astunparse

to_parse = []
magic_token = set()

allowed_modules = []


def find_token(f, modules):
    """
    With the lambda as an input, parse it and try to find ou what are the magi token / expression that it contains
    :param modules: the list of module for witch the parser will recursively try to resolve the encountered function
    :param f: the lambda
    :return: a list of magic tokens
    """
    global allowed_modules

    allowed_modules = modules

    src = __get_src__(f)
    root_token_tree = ast.parse(textwrap.dedent(src)).body
    return __analyse_function_root__(root_token_tree)


def __get_src__(f):
    try:
        return inspect.getsource(f)
    except OSError:
        print("failed to convert back the lambda to code")
        exit(-1)


def __get_fn__(fn_id):
    """
    Will return [] if the function has not been found.
    The role of this code is to resolve the potential fn from a module, not to
    check if the fn is valid
    will return all match. This can lead to confusion and some inefficiency but the context is not
    available from the call thus we shoot wide
    :param fn_id:
    :return:
    """
    global allowed_modules

    res = []

    for module_str in allowed_modules:
        module = sys.modules[module_str]
        if hasattr(module, fn_id):
            res.append(getattr(module, fn_id))

    return res


def __analyse_function_root__(elements):
    global to_parse
    global magic_token

    for element in elements:
        to_parse.append(element)

    while len(to_parse) != 0:
        __parse_element__()

    return magic_token


def __parse_element__():
    global to_parse

    if not to_parse:
        raise ValueError("Nothing to parse")

    current = to_parse.pop()

    # Definition
    if isinstance(current, ast.FunctionDef):
        __parse_element_fn__(current)
    elif isinstance(current, ast.ClassDef):
        pass
    elif isinstance(current, ast.Module):
        __parse_element_module__(current)

    # Import stuff
    elif isinstance(current, ast.Import):
        pass  # Ignored for now
    elif isinstance(current, ast.ImportFrom):
        pass  # Ignored for now

    # Async stuff
    elif isinstance(current, ast.AsyncFor):
        pass  # Ignored for now
    elif isinstance(current, ast.AsyncFunctionDef):
        pass  # Ignored for now
    elif isinstance(current, ast.AsyncWith):
        pass  # Ignored for now

    # Matching
    elif isinstance(current, ast.If):
        __parse_element_if__(current)
    elif isinstance(current, ast.Match):
        __parse_element_match__(current)

    # Boucles
    elif isinstance(current, ast.For):
        pass
    elif isinstance(current, ast.While):
        pass

    # Expressions & assignations
    elif isinstance(current, ast.BinOp):
        __parse_element_binop__(current)
    elif isinstance(current, ast.Compare):
        __parse_element_compare__(current)
    elif isinstance(current, ast.Constant):
        __parse_element_constant__(current)
    elif isinstance(current, ast.Expr):
        __parse_element_expr__(current)
    elif isinstance(current, ast.Assign):
        __parse_element_assign__(current)
    elif isinstance(current, ast.AnnAssign):
        __parse_element_ann_assign__(current)
    elif isinstance(current, ast.AugAssign):
        __parse_element_aug_assign__(current)

    # Flow control
    elif isinstance(current, ast.Call):
        __parse_element_call__(current)
    elif isinstance(current, ast.Lambda):
        __parse_element_lambda__(current)
    elif isinstance(current, ast.Return):
        __parse_element_return__(current)
    elif isinstance(current, ast.Pass):
        pass  # Ignored for now

    # Scoping
    elif isinstance(current, ast.Global):
        pass
    elif isinstance(current, ast.Nonlocal):
        pass
    elif isinstance(current, ast.With):
        pass

    # Errors
    elif isinstance(current, ast.Try):
        __parse_element_try__(current)
    elif isinstance(current, ast.ExceptHandler):
        __parse_element_except__(current)
    elif isinstance(current, ast.Raise):
        pass  # Ignored, this is a state we want to reach, but, as all other it doesn't add any condition to reach it

    # Misc
    elif isinstance(current, ast.Delete):
        __parse_element_delete__(current)
    elif isinstance(current, ast.Subscript):
        __parse_element_subscript__(current)
    elif isinstance(current, ast.Name):
        __parse_element_name__(current)
    elif isinstance(current, type(None)):
        pass  # we don't care about that one
    else:
        print("unhandled pattern: {}".format(type(current)))


def __parse_element_fn__(element):
    global to_parse

    for elem in element.body:
        to_parse.append(elem)


def __parse_element_if__(element):
    global to_parse

    to_parse.append(element.test)

    # parsing the body
    for elem in element.body:
        to_parse.append(elem)

    # parsing the orelse
    for elem in element.orelse:
        to_parse.append(elem)


def __parse_element_match__(current):
    global to_parse

    to_parse.append(current.subject)
    for case in current.cases:
        if isinstance(case.pattern, ast.MatchValue):
            to_parse.append(case.pattern.value)
        elif isinstance(case.pattern, ast.MatchAs):
            to_parse.append(case.pattern.pattern)
        else:
            to_parse.append(case.pattern)

        for b in case.body:
            to_parse.append(b)


def __parse_element_return__(current):
    global to_parse

    to_parse.append(current.value)


def __parse_element_try__(element):
    global to_parse

    for elem in element.body:
        to_parse.append(elem)

    for elem in element.handlers:
        to_parse.append(elem)

    for elem in element.orelse:
        to_parse.append(elem)


def __parse_element_except__(element):
    global to_parse

    for elem in element.body:
        to_parse.append(elem)


def __parse_element_delete__(element):
    global to_parse

    for elem in element.targets:
        to_parse.append(elem)


def __parse_element_assign__(element):
    global to_parse

    to_parse.append(element.value)


def __parse_element_ann_assign__(element):
    global to_parse

    to_parse.append(element.value)
    to_parse.append(element.target)
    to_parse.append(element.annotation)


def __parse_element_aug_assign__(element):
    global to_parse

    to_parse.append(element.value)

    # TODO maybe there is a poss of integrating that int os a static evaluation scheme


def __parse_element_expr__(element):
    global to_parse

    to_parse.append(element.value)


def __parse_element_module__(element):
    global to_parse

    for elem in element.body:
        to_parse.append(elem)


def __parse_element_call__(element):
    global to_parse

    for arg in element.args:
        to_parse.append(arg)

    fns = __get_fn__(element.func.id)

    if not fns:
        return

    for fn in fns:
        src = __get_src__(fn)
        to_parse.append(ast.parse(src))


def __parse_element_lambda__(element):
    global to_parse

    to_parse.append(element.body)
    to_parse.append(element.args)


def __parse_element_constant__(element):
    global magic_token

    magic_token.add(element.value)


def __parse_element_compare__(element):
    global to_parse

    for elem in element.comparators:
        to_parse.append(elem)

    to_parse.append(element.left)

    # TODO: see if the expression is statically evaluable here


def __parse_element_binop__(current):
    global to_parse

    to_parse.append(current.left)
    to_parse.append(current.right)
    # TODO: see if the expression is statically evaluable here


def __parse_element_subscript__(current):
    global to_parse

    to_parse.append(current.slice)
    to_parse.append(current.value)


def __parse_element_name__(current):
    # The content of ast.name is voluntarily ignored, it's not interesting for us in this situation to follow
    # that node
    pass



