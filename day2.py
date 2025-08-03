from networkx.algorithms.isomorphism.matchhelpers import tmpdoc

line = "1,9,10,3,2,3,11,0,99,30,40,50"

with open("./resources/day2.txt") as f:
    line = f.read().strip()


def parse(line):
    return [int(x) for x in line.split(",")]


def execute(program):
    ip = 0
    while 0 <= ip < len(program):
        opcode = program[ip]
        if opcode == 99:
            break
        elif opcode == 1:
            A = program[program[ip + 1]]
            B = program[program[ip + 2]]
            program[program[ip + 3]] = A + B
        elif opcode == 2:
            A = program[program[ip + 1]]
            B = program[program[ip + 2]]
            program[program[ip + 3]] = A * B
        else:
            raise RuntimeError(f"Unknown opcode {opcode}")

        ip += 4

    # print(",".join(map(str, program)))
    return program[0]


def part1():
    program = parse(line)
    program[1] = 12
    program[2] = 2
    print(execute(program))


def part2():
    program = parse(line)
    noun = None
    verb = None
    for i in range(0, 100):
        for j in range(0, 100):
            tmp = program[:]
            tmp[1] = i
            tmp[2] = j
            result = execute(tmp)
            if result == 19690720:
                noun = i
                verb = j
                break

    print(100 * noun + verb)


part1()
part2()
