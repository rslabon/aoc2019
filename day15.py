import random
from collections import deque

from day9 import execute

with open("./resources/day15.txt") as f:
    program = [int(c) for c in f.read().strip().split(",")]

pos = (0, 0)
dir = 1
target = None
grid = {pos: 1}


def get_next_pos(dir, pos):
    x, y = pos
    if dir == 1:
        return x, y - 1
    if dir == 2:
        return x, y + 1
    if dir == 3:
        return x - 1, y
    if dir == 4:
        return x + 1, y

    raise "invalid direction!"


def print_grid():
    xs = [x for x, y in grid.keys()]
    ys = [y for x, y in grid.keys()]
    xmin = min(xs)
    xmax = max(xs)
    ymin = min(ys)
    ymax = max(ys)
    for y in range(ymin - 2, ymax + 2):
        for x in range(xmin - 2, xmax + 2):
            if (x, y) == (0, 0):
                print("S", end="")
            elif (x, y) == target:
                print("T", end="")
            elif (x, y) == pos:
                print("D", end="")
            elif (x, y) == get_next_pos(dir, pos):
                print("*", end="")
            elif (x, y) not in grid:
                print(" ", end="")
            elif grid[(x, y)] == 0:
                print("#", end="")
            elif grid[(x, y)] == 1:
                print(".", end="")
        print()


def movement():
    global dir
    return dir


def random_direction():
    d = [1, 2, 3, 4]
    random.shuffle(d)
    return d[0]


def has_finished():
    for p, v in grid.items():
        if v == 1 or v == 2:
            for d in [1, 2, 3, 4]:
                if get_next_pos(d, p) not in grid:
                    return False

    return True


class END(Exception):
    pass


def status(value):
    global dir, pos, target
    next_pos = get_next_pos(dir, pos)
    grid[next_pos] = value

    if has_finished():
        raise END()

    if value == 0:
        for d in [1, 2, 3, 4]:
            next_pos = get_next_pos(d, pos)
            if next_pos not in grid:
                dir = d
                return

        dir = random_direction()
    else:
        pos = next_pos
        if value == 2:
            target = pos

        for d in [1, 2, 3, 4]:
            next_pos = get_next_pos(d, pos)
            if next_pos not in grid:
                dir = d
                return

        dir = random_direction()


def fill_grid():
    try:
        execute(program, movement, status)
    except END:
        return


def part1():
    fill_grid()
    print_grid()
    q = deque([(1, (0, 0), 0)])
    seen = set()
    movements = None

    while q:
        dir, pos, n = q.popleft()
        if (dir, pos) in seen:
            continue
        if pos == target:
            movements = n
            break

        seen.add((dir, pos))
        for d in [1, 2, 3, 4]:
            next_pos = get_next_pos(d, pos)
            if next_pos in grid and grid[next_pos] != 0:
                q.append((d, next_pos, n + 1))

    assert movements == 282


part1()
