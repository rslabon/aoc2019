from collections import defaultdict
from collections import deque

lines = """
COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
""".strip().splitlines()

lines = """
COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
K)YOU
I)SAN
""".strip().splitlines()

with open("./resources/day6.txt") as f:
    lines = f.read().strip().splitlines()

lines = [line.split(")") for line in lines]


class Digraph(object):

    def __init__(self):
        self.edges = defaultdict(list)
        self.nodes = set()

    def add_edge(self, n1, n2):
        self.nodes.add(n1)
        self.nodes.add(n2)
        self.edges[n1].append(n2)

    def length_path_to_root(self, n):
        total = 0
        for p in self.edges[n]:
            total += 1
            total += self.length_path_to_root(p)

        return total


def part1():
    g = Digraph()
    for n1, n2 in lines:
        g.add_edge(n2, n1)

    total = 0
    for n in g.nodes:
        orbits = g.length_path_to_root(n)
        total += orbits

    print(total)


def part2():
    g = Digraph()
    for n1, n2 in lines:
        g.add_edge(n1, n2)
        g.add_edge(n2, n1)

    q = deque(["YOU"])
    dist = {"YOU": None}

    while q:
        n = q.popleft()
        if n == "SAN":
            break
        for o in g.edges[n]:
            if o not in dist:
                q.append(o)
                dist[o] = n

    n = dist["SAN"]
    transfers = 0
    while n:
        if n == "YOU":
            break
        transfers += 1
        n = dist[n]

    print(transfers - 1)


part1()
part2()
