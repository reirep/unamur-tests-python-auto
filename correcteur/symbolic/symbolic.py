import ast
from _ast import FunctionDef

from correcteur.symbolic.context import Context

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

    while len(to_parse) != 0:
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

    # Definition
    if isinstance(current.ast, ast.FunctionDef):
        __parse_element_fn__(current)
    elif isinstance(current.ast, ast.ClassDef):
        pass

    # Import stuff
    elif isinstance(current.ast, ast.Import):
        pass # Ignored for now
    elif isinstance(current.ast, ast.ImportFrom):
        pass # Ignored for now

    # Async stuff
    elif isinstance(current.ast, ast.AsyncFor):
        pass # Ignored for now
    elif isinstance(current.ast, ast.AsyncFunctionDef):
        pass # Ignored for now
    elif isinstance(current.ast, ast.AsyncWith):
        pass # Ignored for now

    # Matching
    elif isinstance(current.ast, ast.If):
        __parse_element_if__(current)
    elif isinstance(current.ast, ast.Match):
        __parse_element_match__(current)
    elif isinstance(current.ast, ast.Assert):
        __parse_element_assert__(current)

    # Boucles
    elif isinstance(current.ast, ast.For):
        pass
    elif isinstance(current.ast, ast.While):
        pass

    # Expressions & assignations
    elif isinstance(current.ast, ast.Expr):
        __parse_element_expr__(current)
    elif isinstance(current.ast, ast.Assign):
        __parse_element_assign__(current)
    elif isinstance(current.ast, ast.AnnAssign):
        __parse_element_ann_assign__(current)
    elif isinstance(current.ast, ast.AugAssign):
        __parse_element_aug_assign__(current)

    # Flow control
    elif isinstance(current.ast, ast.Break):
        __parse_element_break__(current)
    elif isinstance(current.ast, ast.Continue):
        __parse_element_continue__(current)
    elif isinstance(current.ast, ast.Return):
        __parse_element_return__(current)
    elif isinstance(current.ast, ast.Pass):
        pass # Ignored for now

    # Scoping
    elif isinstance(current.ast, ast.Global):
        pass
    elif isinstance(current.ast, ast.Nonlocal):
        pass
    elif isinstance(current.ast, ast.With):
        pass

    # Errors
    elif isinstance(current.ast, ast.Try):
        __parse_element_try__(current)
    elif isinstance(current.ast, ast.Raise):
        pass # Ignored, this is a state we want to reach, but, as all other it doesn't add any condition to reach it

    # Misc
    elif isinstance(current.ast, ast.Delete):
        __parse_element_delete__(current)

    # DEBUG:
    print("just parsed ", current.get_context_name())

    #TODO here add the context that has just been analysed to the conditions_list


def __parse_element_fn__(context):
    global to_parse

    for elem in context.ast.body:
        context_child = Context(elem, type(elem).__name__, context)
        to_parse.append(context_child)


def __parse_element_if__(context):
    global to_parse

    # parsing the body
    for elem in context.ast.body:
        ctx = Context(elem, "true."+type(elem).__name__, context)
        # saving the test
        ctx.add_condition(context.ast.test)
        to_parse.append(ctx)

    # parsing the orelse
    for elem in context.ast.orelse:
        ctx = Context(elem, "false."+type(elem).__name__, context)
        # saving the opposite test
        ctx.add_condition_inverted(context.ast.test)
        to_parse.append(ctx)


def __parse_element_match__(current):
    # TODO
    pass


def __parse_element_assert__(current):
    # TODO
    pass


def __parse_element_break__(current):
    # TODO
    pass


def __parse_element_continue__(current):
    # TODO
    pass


def __parse_element_return__(current):
    # TODO
    pass


def __parse_element_try__(current):
    # TODO
    pass


def __parse_element_delete__(current):
    # TODO
    pass


def __parse_element_assign__(context):
    # TODO
    pass


def __parse_element_ann_assign__(context):
    # TODO
    pass


def __parse_element_aug_assign__(context):
    # TODO
    pass


def __parse_element_expr__(context):
    # TODO (this is a function call)
    pass

