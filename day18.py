import heapq
from collections import deque

data = """
########################
#f.D.E.e.C.b.A.@.a.B.c.#
######################.#
#d.....................#
########################
""".strip()

data = """
########################
#...............b.C.D.f#
#.######################
#.....@.a.B.c.d.A.e.F.g#
########################
""".strip()

data = """
########################
#@..............ac.GI.b#
###d#e#f################
###A#B#C################
###g#h#i################
########################
""".strip()

data = """
#################
#i.G..c...e..H.p#
########.########
#j.A..b...f..D.o#
########@########
#k.E..a...g..B.n#
########.########
#l.F..d...h..C.m#
#################
""".strip()

with open("resources/day18.txt") as f:
    data = f.read().strip()

grid = []
entrance = None
door_keys = {}
doors = {}
for row_index, line in enumerate(data.split("\n")):
    row = []
    grid.append(row)
    for column_index, value in enumerate(line):
        row.append(value)
        if value == "@":
            entrance = (row_index, column_index)
        if 97 <= ord(value) <= 122:
            door_keys[value] = (row_index, column_index)
            # keys[(row_index, column_index)] = value
        if 65 <= ord(value) <= 90:
            doors[value] = (row_index, column_index)
            # doors[(row_index, column_index)] = value


def print_grid(grid):
    for row in grid:
        for column in row:
            print(column, end="")
        print()


cache = {}


def nearest_keys(grid, door_keys, doors, position, collected_door_keys=set()):
    cache_key = (position, tuple(collected_door_keys))
    if cache_key in cache:
        return cache[cache_key]

    seen = set()
    q = deque([(position, 0)])
    result = set()

    while q:
        current_position, steps = q.popleft()
        if current_position in seen:
            continue
        seen.add(current_position)

        r, c = current_position
        for nr, nc in [(r + 0, c + 1), (r + 1, c + 0), (r - 1, c + 0), (r + 0, c - 1)]:
            if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]):
                if (nr, nc) in seen:
                    continue
                if grid[nr][nc] != "#":
                    not_collected_key = grid[nr][nc] in door_keys and grid[nr][nc] not in collected_door_keys
                    if not_collected_key:
                        result.add((grid[nr][nc], (nr, nc), steps + 1))
                        continue

                    door_without_key = grid[nr][nc] in doors and grid[nr][nc].lower() not in collected_door_keys
                    if door_without_key:
                        continue

                    q.append(((nr, nc), steps + 1))

    cache[cache_key] = result
    return result


def part1():
    q = [(0, 0, entrance, 0, set())]
    heapq.heapify(q)
    min_steps = float("inf")
    seen = set()

    while q:
        _, _, position, steps, collected_door_keys = heapq.heappop(q)

        if (position, steps, tuple(collected_door_keys)) in seen:
            continue
        seen.add((position, steps, tuple(collected_door_keys)))

        if steps >= min_steps:
            continue

        if collected_door_keys == door_keys.keys():
            min_steps = min(steps, min_steps)
            continue

        nkeys = nearest_keys(grid, door_keys, doors, position, collected_door_keys)
        for name, key_position, key_steps in nkeys:
            new_collected = collected_door_keys | {name}
            next_steps = steps + key_steps
            heapq.heappush(q, (-len(new_collected), next_steps, key_position, next_steps, new_collected))

    assert min_steps == 4830


part1()
