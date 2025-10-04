from day5 import execute

with open("./resources/day9.txt") as f:
    program = [int(c) for c in f.read().strip().split(",")]


def part1():
    assert execute(program, lambda: 1, lambda v: v) == 2932210790


def part2():
    assert execute(program, lambda: 2, lambda v: v) == 73144


part1()
part2()
