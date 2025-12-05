import re
from collections import defaultdict, deque

data = """
         A           
         A           
  #######.#########  
  #######.........#  
  #######.#######.#  
  #######.#######.#  
  #######.#######.#  
  #####  B    ###.#  
BC...##  C    ###.#  
  ##.##       ###.#  
  ##...DE  F  ###.#  
  #####    G  ###.#  
  #########.#####.#  
DE..#######...###.#  
  #.#########.###.#  
FG..#########.....#  
  ###########.#####  
             Z       
             Z       
"""

data = """
                   A               
                   A               
  #################.#############  
  #.#...#...................#.#.#  
  #.#.#.###.###.###.#########.#.#  
  #.#.#.......#...#.....#.#.#...#  
  #.#########.###.#####.#.#.###.#  
  #.............#.#.....#.......#  
  ###.###########.###.#####.#.#.#  
  #.....#        A   C    #.#.#.#  
  #######        S   P    #####.#  
  #.#...#                 #......VT
  #.#.#.#                 #.#####  
  #...#.#               YN....#.#  
  #.###.#                 #####.#  
DI....#.#                 #.....#  
  #####.#                 #.###.#  
ZZ......#               QG....#..AS
  ###.###                 #######  
JO..#.#.#                 #.....#  
  #.#.#.#                 ###.#.#  
  #...#..DI             BU....#..LF
  #####.#                 #.#####  
YN......#               VT..#....QG
  #.###.#                 #.###.#  
  #.#...#                 #.....#  
  ###.###    J L     J    #.#.###  
  #.....#    O F     P    #.#...#  
  #.###.#####.#.#####.#####.###.#  
  #...#.#.#...#.....#.....#.#...#  
  #.#####.###.###.#.#.#########.#  
  #...#.#.....#...#.#.#.#.....#.#  
  #.###.#####.###.###.#.#.#######  
  #.#.........#...#.............#  
  #########.###.###.#############  
           B   J   C               
           U   P   P               
"""

with open('resources/day20.txt') as f:
    data = f.read()

lines = [line for line in data.split("\n") if line]


def find_passages(lines):
    passages = set()
    for row, line in enumerate(lines):
        for column, char in enumerate(line):
            if char == ".":
                passages.add((row, column))

    return passages


def find_teleports(lines):
    portals = []
    for row, line in enumerate(lines):
        for i in range(len(line)):
            chars = line[i:i + 2]
            match = re.findall(r"\w{2}", chars)
            if match:
                if i > 0:
                    if line[i - 1] == ".":
                        portals.append((chars, (row, i - 1)))
                if i + 2 < len(line):
                    if line[i + 2] == ".":
                        portals.append((chars, (row, i + 2)))

    rotated_lines = []
    for c in range(len(lines[1])):
        line = ""
        for r in range(len(lines)):
            line += lines[r][c]
        rotated_lines.append(line)

    for row, line in enumerate(rotated_lines):
        for i in range(len(line)):
            chars = line[i:i + 2]
            match = re.findall(r"\w{2}", chars)
            if match:
                if i > 0:
                    if line[i - 1] == ".":
                        portals.append((chars, (i - 1, row)))
                if i + 2 < len(line):
                    if line[i + 2] == ".":
                        portals.append((chars, (i + 2, row)))

    portals_by_name = defaultdict(list)
    for name, position in portals:
        portals_by_name[name].append(position)

    position_teleports = {}
    for positions in portals_by_name.values():
        if len(positions) == 1:
            continue

        position_teleports[positions[0]] = positions[1]
        position_teleports[positions[1]] = positions[0]

    return position_teleports, portals_by_name


def part1():
    passages = find_passages(lines)
    position_teleports, portals_by_name = find_teleports(lines)
    start = portals_by_name["AA"][0]
    target = portals_by_name["ZZ"][0]
    min_steps = float("inf")

    q = deque([(start, set(), 0, [])])

    while q:
        position, seen, steps, path = q.popleft()
        if position == target:
            min_steps = min(min_steps, steps)
            continue
        if position in seen:
            continue

        path.append(position)
        seen.add(position)
        portals = []
        if position in position_teleports:
            portals.append(position_teleports[position])

        px, py = position
        for next_position in [(px + 0, py + 1), (px + 0, py - 1), (px + 1, py + 0), (px - 1, py + 0)] + portals:
            if next_position not in passages:
                continue
            if next_position in seen:
                continue
            q.append((next_position, set(seen), steps + 1, path[:]))

    assert min_steps == 656


part1()
