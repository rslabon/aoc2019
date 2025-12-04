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
    points = set()
    rows = []
    for y in range(height):
        row = []
        offset = 0 if len(rows) == 0 else rows[-1][0][0]
        for x in range(offset, width):
            v = check_position(x, y)
            if v == 1:
                row.append((x, y))
                points.add((x, y))
            elif v == 0 and len(row) > 0:
                break
        if row:
            rows.append(row)
    return rows, points


def part1():
    _, points = scan(50, 50)
    assert len(points) == 189


def find_square(square_size, rows, points):
    for row in rows:
        if len(row) < square_size:
            continue
        for (x, y) in row:
            if (x + square_size - 1, y) in points \
                    and (x, y + square_size - 1) in points \
                    and (x + square_size - 1, y + square_size - 1) in points:
                return (x, y)

    return None


def part2():
    size = 1200
    square = 100
    rows, points = scan(size, size)
    (x, y) = find_square(square, rows, points)
    result = x * 10_000 + y
    assert result == 7621042


part1()
part2()
