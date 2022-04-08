import copy

CONTEXT_SEPARATOR = "."


class Context:
    """
    This class is meant to contain a list of condition needed to end up in the part of the code linked to this context
    """

    def __init__(self, ast, local_context_name, parent_context=None):
        global CONTEXT_SEPARATOR
        self.ast = ast
        if parent_context is not None:
            self.conditions = parent_context.get_conditions_cloned()
            self.context_name = parent_context.get_context_name() + CONTEXT_SEPARATOR + local_context_name
        else:
            self.conditions = []
            self.context_name = local_context_name

    def get_conditions_cloned(self):
        return copy.deepcopy(self.conditions)

    def get_context_name(self):
        return copy.copy(self.context_name)

    def add_condition_inverted(self, condition):
        self.add_condition(condition, inverted=True)

    def add_condition(self, condition, inverted=False):
        print("condition dummy add ", condition)
        # TODO: rework into a real condition encoding
        # a gerer
        # ast.Compare
