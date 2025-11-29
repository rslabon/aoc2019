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


def part2():
    path = find_path(program)
    # print(path)

    # analyzed path manually

    # [A,B,A,B,C,A,B,C,A,C]
    # A: R,6,L,10,R,8
    # B: R,8,R,12,L,8,L,8
    # C: L,10,R,6,R,6,L,8

    index = 0
    input_data = []
    input_data += as_ascii("A,B,A,B,C,A,B,C,A,C")
    input_data += as_ascii("R,6,L,10,R,8")
    input_data += as_ascii("R,8,R,12,L,8,L,8")
    input_data += as_ascii("L,10,R,6,R,6,L,8")
    input_data += as_ascii("n")

    copy_program = program[:]
    copy_program[0] = 2

    def get_input():
        nonlocal input_data, index
        value = input_data[index]
        index += 1
        return value

    _, dust = create_grid(copy_program, get_input)
    print(dust)


part1()
part2()
