from collections import Counter


def has_duplicate(n):
    sn = str(n)
    i = 0
    while i < len(sn):
        if sn[i] == sn[i - 1]:
            return True
        i += 1
    return False


def is_increasing(n):
    sn = str(n)
    i = 1
    while i < len(sn):
        if sn[i] < sn[i - 1]:
            return False
        i += 1
    return True


def part1(lower_limit, upper_limit):
    c = 0
    for n in range(lower_limit, upper_limit + 1):
        if is_increasing(n) and has_duplicate(n):
            c += 1
    return c


def part2(lower_limit, upper_limit):
    c = 0
    for n in range(lower_limit, upper_limit + 1):
        counter = Counter(str(n))
        if is_increasing(n) and 2 in counter.values():
            c += 1
    return c


print(part1(124075, 580769))
print(part2(124075, 580769))
