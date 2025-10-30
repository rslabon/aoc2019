from collections import defaultdict
from enum import Enum

from day5 import execute

with open("./resources/day11.txt") as f:
    program = [int(c) for c in f.read().strip().split(",")]


class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


def left_turn(direction, x, y):
    if direction == Direction.UP:
        return Direction.LEFT, x - 1, y
    if direction == Direction.DOWN:
        return Direction.RIGHT, x + 1, y
    if direction == Direction.LEFT:
        return Direction.DOWN, x, y + 1
    if direction == Direction.RIGHT:
        return Direction.UP, x, y - 1
    raise ValueError("Invalid direction")


def right_turn(direction, x, y):
    if direction == Direction.UP:
        return Direction.RIGHT, x + 1, y
    if direction == Direction.DOWN:
        return Direction.LEFT, x - 1, y
    if direction == Direction.LEFT:
        return Direction.UP, x, y - 1
    if direction == Direction.RIGHT:
        return Direction.DOWN, x, y + 1
    raise ValueError("Invalid direction")


def paint_panels(start_color):
    panels = defaultdict(lambda: 0)
    panels[(0, 0)] = start_color
    direction = Direction.UP
    x, y = 0, 0
    output_nr = 0

    def get_input():
        return panels[(x, y)]

    def handle_output(value):
        nonlocal output_nr
        nonlocal direction
        nonlocal x
        nonlocal y

        output_nr += 1
        if output_nr == 1:
            panels[(x, y)] = value
        else:
            if value == 0:
                direction, x, y = left_turn(direction, x, y)
            elif value == 1:
                direction, x, y = right_turn(direction, x, y)

        output_nr %= 2

    execute(program, get_input, handle_output)
    return panels


def part1():
    panels = paint_panels(0)
    result = len(panels.keys())
    assert result == 2219


def part2():
    panels = paint_panels(1)

    xs = [k[0] for k in panels.keys()]
    ys = [k[0] for k in panels.keys()]
    min_x = min(xs)
    max_x = max(xs)
    min_y = min(ys)
    max_y = max(ys)

    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            print("  " if panels[(x, y)] == 0 else "[]", end="")
        print()


part1()
part2()
