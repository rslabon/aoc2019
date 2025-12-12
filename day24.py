from collections import defaultdict, Counter

data = """
....#
#..#.
#..##
..#..
#....
""".strip()

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


def is_empty(grid):
    return "#" not in grid.values()


def infinite_step(grid_provider, level, width, height):
    if is_empty(grid_provider[level]) and is_empty(grid_provider[level - 1]) and is_empty(grid_provider[level + 1]):
        return None

    new_grid = defaultdict(lambda: "?")
    for row in range(height):
        for col in range(width):
            bugs = 0
            spaces = 0
            if (row, col) == (height // 2, width // 2):
                continue
            for (r, c, dir) in [(row + 0, col + 1, "right"),
                                (row + 0, col - 1, "left"),
                                (row + 1, col + 0, "down"),
                                (row - 1, col + 0, "up")]:
                if (r, c) == (height // 2, width // 2):
                    if dir == "left":
                        for i in range(height):
                            value = grid_provider[level + 1][(i, width - 1)]
                            if value == "#":
                                bugs += 1
                            if value == ".":
                                spaces += 1
                    elif dir == "right":
                        for i in range(height):
                            value = grid_provider[level + 1][(i, 0)]
                            if value == "#":
                                bugs += 1
                            if value == ".":
                                spaces += 1
                    elif dir == "up":
                        for i in range(width):
                            value = grid_provider[level + 1][(height - 1, i)]
                            if value == "#":
                                bugs += 1
                            if value == ".":
                                spaces += 1
                    elif dir == "down":
                        for i in range(width):
                            value = grid_provider[level + 1][(0, i)]
                            if value == "#":
                                bugs += 1
                            if value == ".":
                                spaces += 1
                elif (r, c) not in grid_provider[level]:
                    if r < 0:
                        value = grid_provider[level - 1][((height // 2) - 1, width // 2)]
                        if value == "#":
                            bugs += 1
                        if value == ".":
                            spaces += 1
                    elif r >= height:
                        value = grid_provider[level - 1][((height // 2) + 1, width // 2)]
                        if value == "#":
                            bugs += 1
                        if value == ".":
                            spaces += 1
                    elif c < 0:
                        value = grid_provider[level - 1][(height // 2, (width // 2) - 1)]
                        if value == "#":
                            bugs += 1
                        if value == ".":
                            spaces += 1
                    elif c >= width:
                        value = grid_provider[level - 1][(height // 2, (width // 2) + 1)]
                        if value == "#":
                            bugs += 1
                        if value == ".":
                            spaces += 1
                elif grid_provider[level][(r, c)] == "#":
                    bugs += 1
                elif grid_provider[level][(r, c)] == ".":
                    spaces += 1

            if grid_provider[level][(row, col)] == "#" and bugs != 1:
                new_grid[(row, col)] = "."
            elif grid_provider[level][(row, col)] == "." and 1 <= bugs <= 2:
                new_grid[(row, col)] = "#"
            else:
                new_grid[(row, col)] = grid_provider[level][(row, col)]

    return new_grid


def part1():
    grid = parse_grid(data)
    seen = {tuple(grid.items())}
    size = 5
    while True:
        grid = step(grid, size, size)
        if tuple(grid.items()) in seen:
            biodiversity_rating = 0
            for (row, col), value in grid.items():
                if value == "#":
                    biodiversity_rating += 2 ** (row * size + col)
            print(biodiversity_rating)
            break
        seen.add(tuple(grid.items()))


def part2():
    grid = parse_grid(data)
    grid_provider = defaultdict(lambda: defaultdict(lambda: "."))
    grid_provider[0] = grid
    size = 5
    min_level = float("inf")
    max_level = float("-inf")
    for i in range(200):
        new_grid_provider = defaultdict(lambda: defaultdict(lambda: "."))
        new_grid = infinite_step(grid_provider, 0, size, size)
        new_grid_provider[0] = new_grid
        for l in range(1, 100000000000):
            new_grid = infinite_step(grid_provider, -l, size, size)
            if new_grid is None:
                break
            new_grid_provider[-l] = new_grid
            min_level = min(min_level, -l)
        for l in range(1, 100000000000):
            new_grid = infinite_step(grid_provider, l, size, size)
            if new_grid is None:
                break
            new_grid_provider[l] = new_grid
            max_level = max(max_level, l)

        grid_provider = new_grid_provider

    bugs = 0
    for i in range(min_level, max_level + 1):
        bugs += Counter(grid_provider[i].values())["#"]
    print(bugs)


part1()
part2()
