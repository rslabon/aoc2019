from collections import deque

from day9 import execute

with open("resources/day17.txt") as f:
    program = [int(c) for c in f.read().strip().split(",")]


def create_grid(program, input_callback=lambda: 1):
    grid = [[]]
    row = grid[0]
    dust = None

    def handle_output(value):
        nonlocal row, grid, dust
        if value == 35:
            row.append("#")
        elif value == 46:
            row.append(".")
        elif value == 10:
            row = []
            grid.append(row)
        elif 0 <= value < 127:
            row.append(chr(value))
        else:
            dust = value

    execute(program, input_callback, handle_output)
    grid = [row for row in grid if row]
    return grid, dust


def find_sides(row_index, col_index, grid):
    sides = 0
    for rx, cx in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
        r = row_index + rx
        c = col_index + cx
        if 0 <= r < len(grid) - 1 and 0 <= c < len(grid[0]) - 1:
            if grid[r][c] == "#":
                sides += 1
    return sides


def part1():
    grid, _ = create_grid(program)
    alignment = 0
    for row_index, row in enumerate(grid):
        for col_index, col in enumerate(row):
            sides = find_sides(row_index, col_index, grid)
            if sides == 4:
                alignment += row_index * col_index

    assert alignment == 11372


def as_ascii(s):
    return [ord(c) for c in s] + [10]


def find_path(program):
    grid, _ = create_grid(program)
    robot = None
    for row_index, row in enumerate(grid):
        for col_index, col in enumerate(row):
            if col in [">", "<", "^", "v"]:
                robot = row_index, col_index

    robot_dir = grid[robot[0]][robot[1]]
    q = deque([(robot, robot_dir, [])])
    grid[robot[0]][robot[1]] = "#"
    path = None
    while q:
        robot, robot_dir, path = q.popleft()
        robot_row, robot_col = robot
        next_moves = []
        for r, c, next_dir in [(1, 0, "v"), (0, 1, ">"), (-1, 0, "^"), (0, -1, "<")]:
            next_row = robot_row
            next_col = robot_col
            n = 0
            while 0 <= next_row + r < len(grid) \
                    and 0 <= next_col + c < len(grid[0]) \
                    and grid[next_row + r][next_col + c] == "#":
                n += 1
                next_row += r
                next_col += c

            if n > 0:
                next_moves.append((n, next_row, next_col, next_dir))

        for n, next_row, next_col, next_dir in next_moves:
            new_path = path[:]

            if robot_dir == "^" and next_dir == ">":
                new_path.append("R")
            elif robot_dir == ">" and next_dir == "v":
                new_path.append("R")
            elif robot_dir == "v" and next_dir == "<":
                new_path.append("R")
            elif robot_dir == "<" and next_dir == "^":
                new_path.append("R")

            elif robot_dir == "^" and next_dir == "<":
                new_path.append("L")
            elif robot_dir == "<" and next_dir == "v":
                new_path.append("L")
            elif robot_dir == "v" and next_dir == ">":
                new_path.append("L")
            elif robot_dir == ">" and next_dir == "^":
                new_path.append("L")
            else:
                # back moves like > < or ^ v
                continue

            new_path.append(n)
            q.append(((next_row, next_col), next_dir, new_path))

    return path


def find_patterns(s, patterns=[]):
    if len(patterns) > 3:
        return None
    if not s and len(patterns) == 3:
        return patterns

    for i in range(min(5, len(s)), min(19, len(s))):
        p = s[0:i]
        if p[0] not in ["R", "L"] and p[-1] in [",", "R", "L"]:
            continue

        ss = s[:]
        ss = ss.replace(p + ",", "")
        ss = ss.replace(p, "")
        r = find_patterns(ss, patterns + [p])
        if r:
            return r

    return None


def part2():
    path = find_path(program)
    s = ",".join(map(str, path))
    A, B, C = find_patterns(s)
    main = s.replace(A, "A").replace(B, "B").replace(C, "C")

    index = 0
    input_data = []
    input_data += as_ascii(main)
    input_data += as_ascii(A)
    input_data += as_ascii(B)
    input_data += as_ascii(C)
    input_data += as_ascii("n")

    copy_program = program[:]
    copy_program[0] = 2

    def get_input():
        nonlocal input_data, index
        value = input_data[index]
        index += 1
        return value

    _, dust = create_grid(copy_program, get_input)

    assert dust == 1155497


part1()
part2()
