import math
from collections import defaultdict

data1 = """
......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####
""".strip()

data2 = """
#.#...#.#.
.###....#.
.#....#...
##.#.#.#.#
....#.#.#.
.##..###.#
..#...##..
..##....##
......#...
.####.###.
""".strip()

data3 = """
.#..#..###
####.###.#
....###.#.
..###.##.#
##.##.#.#.
....###..#
..#.#..#.#
#..#.#.###
.##...##.#
.....#.#..
""".strip()

data4 = """
.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##
""".strip()

data5 = """
#.........
...#......
...#..#...
.####....#
..#.#.#...
.....#....
..###.#.##
.......#..
....#...#.
...#..#..#
""".strip()

data6 = """
.#....#####...#..
##...##.#####..##
##...#...#.#####.
..#.....#...###..
..#.#.....#....##
""".strip()


def gcd(a, b):
    while b:
        a, b = b, a % b
    return abs(a)


def step(a, b):
    g = gcd(abs(a), abs(b))
    return a // g, b // g


def find_blocked_asteroids(sx, sy, ax, ay, xmax, ymax):
    dx, dy = ax - sx, ay - sy
    step_x, step_y = step(dx, dy)
    points = []
    x, y = ax, ay
    while 0 <= x <= xmax and 0 <= y <= ymax:
        points.append((x, y))
        x += step_x
        y += step_y

    return set(points[1:])


def find_asteroids(grid):
    width = len(grid[0])
    height = len(grid)
    asteroids = set()
    for y in range(height):
        for x in range(width):
            if grid[y][x] == "#":
                asteroids.add((x, y))

    return asteroids


def detect_asteroids(grid, station):
    width = len(grid[0])
    height = len(grid)
    asteroids = find_asteroids(grid) - {station}

    sx, sy = station
    total_blocked = set()
    for (ax, ay) in asteroids:
        blocked_asteroids = find_blocked_asteroids(sx, sy, ax, ay, width, height)
        total_blocked = total_blocked | blocked_asteroids

    return len(asteroids - total_blocked - {station})


def find_best_station(grid):
    asteroids = find_asteroids(grid)
    max_visible = float("-inf")
    best_station = None
    for station in asteroids:
        visible = detect_asteroids(grid, station)
        if visible > max_visible:
            max_visible = visible
            best_station = station

    return max_visible, best_station


def distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return math.hypot(x2 - x1, y2 - y1)


# .#....###24...#..
# ##...##.13#67..9#
# ##...#...5.8####.
# ..#.....X...###..
# ..#.#.....#....##
def find_angle(laser, asteroid):
    lx, ly = laser
    ax, ay = asteroid

    if lx == ax:
        if ly > ay:
            return 0
        return 180
    if ly == ay:
        if lx < ax:
            return 90
        return 270

    a = distance((lx, ly), (lx, 0))
    b = distance((lx, ly), (ax, ay))
    c = distance((lx, 0), (ax, ay))

    angle_rad = math.acos((a ** 2 + b ** 2 - c ** 2) / (2 * a * b))
    angle_deg = math.degrees(angle_rad)
    if lx > ax:
        return 360 - angle_deg

    return angle_deg


def vaporized_asteroids(x, y, asteroids):
    angle_to_asteroid = defaultdict(set)
    for (ax, ay) in asteroids:
        angle = find_angle((x, y), (ax, ay))
        angle = round(angle, 3)
        angle_to_asteroid[angle].add((distance((x, y), (ax, ay)), (ax, ay)))

    result = []
    for (angle, asteroids) in angle_to_asteroid.items():
        sorted_asteroids = list(sorted(asteroids, key=lambda asteroid: asteroid[0]))
        result.append((angle, sorted_asteroids[0][1]))

    return list(sorted(result, key=lambda i: i[0]))


def part1():
    with open("./resources/day10.txt") as f:
        data = f.read().strip()

    grid = []
    for line in data.splitlines():
        row = []
        for c in line:
            row.append(c)
        grid.append(row)

    max_visible, _ = find_best_station(grid)
    assert max_visible == 260


def part2():
    with open("./resources/day10.txt") as f:
        data = f.read().strip()

    grid = []
    for line in data.splitlines():
        row = []
        for c in line:
            row.append(c)
        grid.append(row)

    max_visible, (sx, sy) = find_best_station(grid)
    asteroids = find_asteroids(grid) - {(sx, sy)}
    nr = 0
    while asteroids:
        for (angle, (ax, ay)) in vaporized_asteroids(sx, sy, asteroids):
            nr += 1
            asteroids = asteroids - {(ax, ay)}
            if nr == 200:
                result = ax * 100 + ay
                assert result == 608
                return

    raise "ERROR!"


part1()
part2()
