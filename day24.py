data = """
....#
#..#.
#..##
..#..
#....
""".strip()

with open("resources/day24.txt") as f:
    data = f.read().strip()


def parse_grid(data):
    grid = {}
    for row, line in enumerate(data.split("\n")):
        for col, value in enumerate(line):
            grid[(row, col)] = value

    return grid


def step(grid, width, height):
    new_grid = {}
    for row in range(height):
        for col in range(width):
            bugs = 0
            spaces = 0
            for (r, c) in [(row + 0, col + 1), (row + 0, col - 1), (row + 1, col + 0), (row - 1, col + 0)]:
                if (r, c) not in grid:
                    continue

                if grid[(r, c)] == "#":
                    bugs += 1
                if grid[(r, c)] == ".":
                    spaces += 1

            if grid[(row, col)] == "#" and bugs != 1:
                new_grid[(row, col)] = "."
            elif grid[(row, col)] == "." and 1 <= bugs <= 2:
                new_grid[(row, col)] = "#"
            else:
                new_grid[(row, col)] = grid[(row, col)]

    return new_grid


def print_grid(grid, width, height):
    for row in range(height):
        for col in range(width):
            print(grid[(row, col)], end="")
        print()
    print()


def part1():
    grid = parse_grid(data)
    seen = {tuple(grid.items())}
    size = 5
    while True:
        grid = step(grid, size, size)
        if tuple(grid.items()) in seen:
            print_grid(grid, size, size)
            biodiversity_rating = 0
            for (row, col), value in grid.items():
                if value == "#":
                    biodiversity_rating += 2 ** (row * size + col)
            print(biodiversity_rating)
            break
        seen.add(tuple(grid.items()))


part1()
