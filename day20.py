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

# data = """
#                    A
#                    A
#   #################.#############
#   #.#...#...................#.#.#
#   #.#.#.###.###.###.#########.#.#
#   #.#.#.......#...#.....#.#.#...#
#   #.#########.###.#####.#.#.###.#
#   #.............#.#.....#.......#
#   ###.###########.###.#####.#.#.#
#   #.....#        A   C    #.#.#.#
#   #######        S   P    #####.#
#   #.#...#                 #......VT
#   #.#.#.#                 #.#####
#   #...#.#               YN....#.#
#   #.###.#                 #####.#
# DI....#.#                 #.....#
#   #####.#                 #.###.#
# ZZ......#               QG....#..AS
#   ###.###                 #######
# JO..#.#.#                 #.....#
#   #.#.#.#                 ###.#.#
#   #...#..DI             BU....#..LF
#   #####.#                 #.#####
# YN......#               VT..#....QG
#   #.###.#                 #.###.#
#   #.#...#                 #.....#
#   ###.###    J L     J    #.#.###
#   #.....#    O F     P    #.#...#
#   #.###.#####.#.#####.#####.###.#
#   #...#.#.#...#.....#.....#.#...#
#   #.#####.###.###.#.#.#########.#
#   #...#.#.....#...#.#.#.#.....#.#
#   #.###.#####.###.###.#.#.#######
#   #.#.........#...#.............#
#   #########.###.###.#############
#            B   J   C
#            U   P   P
# """

data = """
             Z L X W       C                 
             Z P Q B       K                 
  ###########.#.#.#.#######.###############  
  #...#.......#.#.......#.#.......#.#.#...#  
  ###.#.#.#.#.#.#.#.###.#.#.#######.#.#.###  
  #.#...#.#.#...#.#.#...#...#...#.#.......#  
  #.###.#######.###.###.#.###.###.#.#######  
  #...#.......#.#...#...#.............#...#  
  #.#########.#######.#.#######.#######.###  
  #...#.#    F       R I       Z    #.#.#.#  
  #.###.#    D       E C       H    #.#.#.#  
  #.#...#                           #...#.#  
  #.###.#                           #.###.#  
  #.#....OA                       WB..#.#..ZH
  #.###.#                           #.#.#.#  
CJ......#                           #.....#  
  #######                           #######  
  #.#....CK                         #......IC
  #.###.#                           #.###.#  
  #.....#                           #...#.#  
  ###.###                           #.#.#.#  
XF....#.#                         RF..#.#.#  
  #####.#                           #######  
  #......CJ                       NM..#...#  
  ###.#.#                           #.###.#  
RE....#.#                           #......RF
  ###.###        X   X       L      #.#.#.#  
  #.....#        F   Q       P      #.#.#.#  
  ###.###########.###.#######.#########.###  
  #.....#...#.....#.......#...#.....#.#...#  
  #####.#.###.#######.#######.###.###.#.#.#  
  #.......#.......#.#.#.#.#...#...#...#.#.#  
  #####.###.#####.#.#.#.#.###.###.#.###.###  
  #.......#.....#.#...#...............#...#  
  #############.#.#.###.###################  
               A O F   N                     
               A A D   M                     
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


def is_inner_portal(line, column):
    before = False
    for c in range(0, column):
        if line[c] in [".", "#"]:
            before = True

    after = False
    for c in range(column + 1, len(line)):
        if line[c] in [".", "#"]:
            after = True

    return "inner" if before and after else "outer"


def find_teleports(lines):
    portals = []
    for row, line in enumerate(lines):
        for i in range(len(line)):
            chars = line[i:i + 2]
            match = re.findall(r"\w{2}", chars)
            if match:
                if i > 0:
                    if line[i - 1] == ".":
                        portals.append((chars, is_inner_portal(line, i), (row, i - 1)))
                if i + 2 < len(line):
                    if line[i + 2] == ".":
                        portals.append((chars, is_inner_portal(line, i), (row, i + 2)))

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
                        portals.append((chars, is_inner_portal(line, i), (i - 1, row)))
                if i + 2 < len(line):
                    if line[i + 2] == ".":
                        portals.append((chars, is_inner_portal(line, i), (i + 2, row)))

    portals_by_name = defaultdict(list)
    for name, type, position in portals:
        portals_by_name[name].append(position)

    portals_type = {}
    for name, type, position in portals:
        portals_type[position] = type

    portals_name = {}
    for name, type, position in portals:
        portals_name[position] = name

    position_teleports = {}
    for positions in portals_by_name.values():
        if len(positions) == 1:
            continue

        position_teleports[positions[0]] = positions[1]
        position_teleports[positions[1]] = positions[0]

    return position_teleports, portals_by_name, portals_type, portals_name


def part1():
    passages = find_passages(lines)
    position_teleports, portals_by_name, _, _ = find_teleports(lines)
    start = portals_by_name["AA"][0]
    target = portals_by_name["ZZ"][0]
    min_steps = float("inf")

    q = deque([(start, set(), 0)])

    while q:
        position, seen, steps = q.popleft()
        if position == target:
            min_steps = min(min_steps, steps)
            continue
        if position in seen:
            continue

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
            q.append((next_position, set(seen), steps + 1))

    assert min_steps == 656


def is_blocked(level, portals_name, portals_type, passages, to_position, from_position):
    if to_position not in passages:
        return True
    if to_position not in portals_name:
        return False
    if from_position not in portals_name:
        return False
    to_type = portals_type[to_position]
    from_type = portals_type[from_position]
    if level == 0:
        name = portals_name[to_position]
        if name not in ["AA", "ZZ"] and from_type == "outer" and to_type == "inner":
            return True
        else:
            return False
    else:
        name = portals_name[to_position]
        if name in ["AA", "ZZ"]:
            return True
        else:
            return False


def part2():
    passages = find_passages(lines)
    position_teleports, portals_by_name, portals_type, portals_name = find_teleports(lines)
    start = portals_by_name["AA"][0]
    target = portals_by_name["ZZ"][0]
    min_steps = 8000
    q = deque([(start, 0, set(), 0)])

    while q:
        position, level, seen, steps = q.popleft()
        if steps > min_steps:
            continue

        if level < 0:
            continue
        if position == target and level == 0:
            min_steps = steps
            break
        if (position, level) in seen:
            continue

        seen.add((position, level))

        portals = []
        if position in position_teleports:
            if not is_blocked(level, portals_name, portals_type, passages, position_teleports[position], position):
                portals.append(position_teleports[position])

        px, py = position
        for next_position in [(px + 0, py + 1), (px + 0, py - 1), (px + 1, py + 0), (px - 1, py + 0)] + portals:
            if is_blocked(level, portals_name, portals_type, passages, next_position, position):
                continue
            elif level == 0 and next_position in portals_name and portals_name[next_position] in ["AA", "ZZ"]:
                if (next_position, level) in seen:
                    continue
                q.append((next_position, level, set(seen), steps + 1))
            elif position in portals_name and next_position in portals_name:
                from_portal = portals_type[position]
                to_type = portals_type[next_position]
                if from_portal == "inner" and to_type == "outer":
                    if (next_position, level + 1) in seen:
                        continue
                    q.append((next_position, level + 1, {(position, level)}, steps + 1))
                if from_portal == "outer" and to_type == "inner":
                    if (next_position, level - 1) in seen:
                        continue
                    q.append((next_position, level - 1, {(position, level)}, steps + 1))
            else:
                if (next_position, level) in seen:
                    continue
                q.append((next_position, level, set(seen), steps + 1))

    assert min_steps == 7114


part1()
part2()
