import ast
from _ast import FunctionDef

from testing.symbolic.context import Context

# to_parse is pile of context that still needs to be recursively parsed
to_parse = []

# conditions_list is a tuple containing each time two thing: a context name and the conditions needed to get there as an
# array
conditions_list = []


def analyse_file(path, functionFocus):
    # TODO check if the file exists
    with open(path) as f:
        content = f.read()
        analyse_str(content, functionFocus)


def analyse_str(code, functionFocus):
    """
    Try to find values that will make all the branch of a function be explored

    :param code: the input code, as a string
    :param functionFocus: the function the code will focus on
    :return: the list of input to get
    """
    body = ast.parse(code).body
    for definition in body:
        if isinstance(definition, FunctionDef) and definition.name == functionFocus:
            __analyse_function_root__(definition)

    # TODO condition list optimisation I
    # TODO condition list resolution
    # TODO condition list optimisation II
    # TODO condition list convertion
    # TODO return


def __analyse_function_root__(function_definition):
    global to_parse

    to_parse.append(Context(function_definition, function_definition.name))

    while to_parse:
        __parse_element__()


def __parse_element__():
    """
    Will take an element on the to process stack and parse it
    :return: None
    """

    global to_parse
    global conditions_list

    if not to_parse:
        raise ValueError("Nothing to parse")

    current = to_parse.pop()

    # TODO register the current context in conditions_list

    switch = {
        type(ast.FunctionDef): __parse_element_fn__(),
        type(ast.If): __parse_element_if__()
        # Il y a 26 struct __ast.stmt que je vais devoir prendre en compte ici...
    }
    switch.get(type(current.ast))


def __parse_element_fn__():
    # TODO
    pass


def __parse_element_if__():
    # TODO
    pass
