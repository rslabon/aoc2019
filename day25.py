from day17 import as_ascii
from day5 import execute

with open("resources/day25.txt") as f:
    program = [int(c) for c in f.read().strip().split(",")]

buffer = []


def get_input():
    global buffer
    if not buffer:
        buffer += as_ascii(input())
    return buffer.pop(0)


def handle_output(value):
    if value == 10:
        print()
    else:
        print(chr(value), end="")


execute(program, get_input, handle_output)
