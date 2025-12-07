from functools import reduce

from day17 import as_ascii
from day5 import execute

with open("resources/day21.txt") as f:
    program = [int(c) for c in f.read().strip().split(",")]


def run(lines):
    ascii_lines = list(map(as_ascii, lines))
    ascii_lines = reduce(lambda x, y: x + y, ascii_lines, [])
    index = -1

    def get_input():
        nonlocal index
        index += 1
        return ascii_lines[index]

    def handle_output(value):
        if 0 <= value < 127:
            if value == 10:
                print()
            else:
                print(chr(value), end="")
        else:
            print("hull damage", value)

    execute(program[:], get_input, handle_output)


def part1():
    # (not A or not B or not C) and D
    run([
        "NOT A J",
        "NOT B T",
        "OR T J",
        "NOT C T",
        "OR T J",
        "AND D J",
        "WALK"
    ])


def part2():
    # (not A or not B or not C or not D or not E or not F or not G or not H) and I
    # simplify to (not A or not B or not C) and D and (E or H)
    run([
        "NOT A J",
        "NOT B T",
        "OR T J",
        "NOT C T",
        "OR T J",
        "AND D J",
        "NOT E T",
        "NOT T T",
        "OR H T",
        "AND T J",
        "RUN"
    ])


part1()
part2()
