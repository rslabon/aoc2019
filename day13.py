from day5 import execute

with open("./resources/day13.txt") as f:
    program = [int(c) for c in f.read().strip().split(",")]


def play():
    data = program[:]
    data[0] = 2
    buffer = []
    score = 0
    ball = None
    paddle = None

    def get_input():
        nonlocal ball, paddle
        if ball and paddle:
            if paddle[0] < ball[0]:
                return 1
            if paddle[0] > ball[0]:
                return -1
        return 0

    def handle_output(v):
        nonlocal ball, paddle, buffer, score
        buffer.append(v)
        if len(buffer) == 3:
            x = buffer[0]
            y = buffer[1]
            id = buffer[2]
            if x == -1 and y == 0:
                score = max(score, id)

            buffer = []
            if id == 3:
                paddle = (x, y)
            if id == 4:
                ball = (x, y)

    execute(data, get_input, handle_output)
    return score


def part1():
    output = []
    execute(program, lambda: 1, lambda v: output.append(v))
    result = 0
    for i in range(0, len(output), 3):
        id = output[i + 2]
        if id == 2:
            result += 1

    assert result == 205


def part2():
    score = play()
    assert score == 10292


part1()
part2()
