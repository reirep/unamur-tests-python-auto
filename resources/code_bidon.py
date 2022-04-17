from typing import List


def lol(a):
    if 666 == a:
        print('ok')
    elif 777 == a:
        print("wooo")
    else:
        print(a * 3)


def lol2(a):
    if 555 == a:
        print('okijeg')
    else:
        print("gpkjehjgb")


def bidon(a, b):
    res = 0
    if a > 10:
        res = a / 2
    elif b < 2:
        res += b * 3
    return (a - b + res) / (11-a)


def bidon_vil(a: int, b: int):
    res = 0
    if a > 10:
        res = a / 2
    elif b < 2:
        res += b * 3
    return (a - b + res) / (11-a)


def bidon_deux(a, b):
    a: int = 2
    bidon_trois(a, b)


def bidon_trois(a, b):
    a: int = 5
    bidon_quatre(a, b)


def bidon_quatre(a, b):
    a: int = 7
    bidon_cinq(a, b)


def bidon_cinq(a, b):
    a: int = 9
    print("ok")


def call_fn(a, b):
    bidon_deux(a, b)


def bidon_adder(a: List[int], b: int):
    if len(a) >= 1:
        return 1/b
    return b + 1


def bidon_validate(a, b, c):
    return a + b == c
