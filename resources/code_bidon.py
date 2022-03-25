
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


def bidon_validate(a):
    return True
