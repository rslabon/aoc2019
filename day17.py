from day9 import execute

with open("resources/day17.txt") as f:
    program = [int(c) for c in f.read().strip().split(",")]

grid = [[]]
row = grid[0]


def handle_output(value):
    global row, grid
    # 35 means #, 46 means ., 10 starts a new line of output below the current one, and so on.
    if value == 35:
        row.append("#")
    if value == 46:
        row.append(".")
    if value == 10:
        row = []
        grid.append(row)


execute(program, lambda: 1, handle_output)
grid = [row for row in grid if row]


def part1():
    alignment = 0
    for row_index, row in enumerate(grid):
        for col_index, col in enumerate(row):
            sides = 0
            for rx, cx in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                r = row_index + rx
                c = col_index + cx
                if 0 <= r < len(grid) - 1 and 0 <= c < len(grid[0]) - 1:
                    if grid[r][c] == "#":
                        sides += 1

            if sides == 4:
                alignment += row_index * col_index

    assert alignment == 11372


part1()
