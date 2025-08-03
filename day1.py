import functools

with open("./resources/day1.txt") as f:
    lines = f.read().strip().splitlines()

mass = []
for line in lines:
    mass.append(int(line))


@functools.cache
def fuel(n):
    return int(n / 3) - 2


@functools.cache
def total_fuel(n):
    if n <= 0:
        return 0
    r = fuel(n) + total_fuel(fuel(n))
    if r < 0:
        return 0
    else:
        return r


def part1():
    total = sum([fuel(m) for m in mass])
    print(total)


def part2():
    total = sum([total_fuel(m) for m in mass])
    print(total)


part1()
part2()
