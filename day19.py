from collections import Counter

from day5 import execute

with open("resources/day19.txt") as f:
    program = [int(c) for c in f.read().strip().split(",")]


def check_position(x, y):
    data = [x, y]
    i = -1
    output = None

    def get_input():
        nonlocal i, data
        i += 1
        return data[i]

    def handle_output(value):
        nonlocal output
        output = value

    execute(program, get_input, handle_output)
    return output


def scan(width, height):
    grid = {}
    for y in range(height):
        for x in range(width):
            grid[(x, y)] = check_position(x, y)
    return grid


def part1():
    grid = scan(50, 50)
    affected_points = Counter(grid.values())[1]
    assert affected_points == 189


part1()
