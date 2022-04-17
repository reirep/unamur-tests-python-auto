from correcteur.fuzzing.input.bool import Bool
from correcteur.fuzzing.input.float import Float
from correcteur.fuzzing.input.int import Int
from correcteur.fuzzing.input.list import List
from correcteur.fuzzing.input.str import Str


def get_type_from_str(name):
    if name == "int":
        return Int()
    if name == "float":
        return Float()
    if name == "bool":
        return Bool()
    if name == "str":
        return Str()

    if name == "List[int]":
        return List(internal_type=Int())
    if name == "List[float]":
        return List(internal_type=Float())
    if name == "List[bool]":
        return List(internal_type=Bool())
    if name == "List[str]":
        return List(internal_type=Str())

    raise NotImplementedError()
