from enum import Enum, auto


class Constraints(Enum):
    Equal = auto()
    Different = auto()
    LessThan = auto()
    MoreThan = auto()
    LessOrEqualThan = auto()
    MoreOrEqualThan = auto()


class Member(Enum):
    Constant = auto()
    Identifier = auto()
    Call = auto()


class MonoCondition:
    """
    represent a condition that is one thing, eg: a raw bool, one var
    """
    pass


class BiCondition:
    """
    represent a condition that is two things, eg: an inverted raw bool, one var and a not, ...
    """
    pass


class TriCondition:
    """
    represent a condition that is three things, eg: a comparison, ...
    """
    pass
