from enum import Enum


class Result(Enum):
    PASS = 1
    FAIL = 2
    UNAVAILABLE = 3
    TIMEOUT = 4
