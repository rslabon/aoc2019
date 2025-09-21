with open("./resources/day5.txt") as f:
    line = f.read().strip()

program = [int(c) for c in line.split(",")]


def parse_opcode(value):
    sv = str(value)
    mode3 = 0
    mode2 = 0
    mode1 = 0
    if 1 <= len(sv) <= 2:
        value = int(sv)
    elif len(sv) == 3:
        mode1 = int(sv[0])
        value = int(sv[1::])
    elif len(sv) == 4:
        mode2 = int(sv[0])
        mode1 = int(sv[1])
        value = int(sv[2::])
    elif len(sv) == 5:
        mode3 = int(sv[0])
        mode2 = int(sv[1])
        mode1 = int(sv[2])
        value = int(sv[3::])
    else:
        raise Exception("Invalid opcode value!")

    return mode3, mode2, mode1, value


def execute(program, input):
    ip = 0
    output = None
    while 0 <= ip < len(program):
        mode3, mode2, mode1, opcode = parse_opcode(program[ip])
        if opcode == 99:
            break
        elif opcode == 1:
            A = program[program[ip + 1]] if mode1 == 0 else program[ip + 1]
            B = program[program[ip + 2]] if mode2 == 0 else program[ip + 2]
            program[program[ip + 3]] = A + B
            ip += 4
        elif opcode == 2:
            A = program[program[ip + 1]] if mode1 == 0 else program[ip + 1]
            B = program[program[ip + 2]] if mode2 == 0 else program[ip + 2]
            program[program[ip + 3]] = A * B
            ip += 4

        # Opcode 3 takes a single integer as input and saves it to the position given by its only parameter. For example, the instruction 3,50 would take an input value and store it at address 50.
        elif opcode == 3:
            A = program[ip + 1]
            program[A] = input
            ip += 2

        # Opcode 4 outputs the value of its only parameter. For example, the instruction 4,50 would output the value at address 50.
        elif opcode == 4:
            A = program[program[ip + 1]] if mode1 == 0 else program[ip + 1]
            output = A
            ip += 2

        # Opcode 5 is jump-if-true: if the first parameter is non-zero, it sets the instruction pointer to the value from the second parameter. Otherwise, it does nothing.
        elif opcode == 5:
            A = program[program[ip + 1]] if mode1 == 0 else program[ip + 1]
            B = program[program[ip + 2]] if mode2 == 0 else program[ip + 2]
            if A != 0:
                ip = B
            else:
                ip += 3

        # Opcode 6 is jump-if-false: if the first parameter is zero, it sets the instruction pointer to the value from the second parameter. Otherwise, it does nothing.
        elif opcode == 6:
            A = program[program[ip + 1]] if mode1 == 0 else program[ip + 1]
            B = program[program[ip + 2]] if mode2 == 0 else program[ip + 2]
            if A == 0:
                ip = B
            else:
                ip += 3

        # Opcode 7 is less than: if the first parameter is less than the second parameter, it stores 1 in the position given by the third parameter. Otherwise, it stores 0.
        elif opcode == 7:
            A = program[program[ip + 1]] if mode1 == 0 else program[ip + 1]
            B = program[program[ip + 2]] if mode2 == 0 else program[ip + 2]
            C = program[ip + 3]
            if A < B:
                program[C] = 1
            else:
                program[C] = 0
            ip += 4

        # Opcode 8 is equals: if the first parameter is equal to the second parameter, it stores 1 in the position given by the third parameter. Otherwise, it stores 0.
        elif opcode == 8:
            A = program[program[ip + 1]] if mode1 == 0 else program[ip + 1]
            B = program[program[ip + 2]] if mode2 == 0 else program[ip + 2]
            C = program[ip + 3]
            if A == B:
                program[C] = 1
            else:
                program[C] = 0
            ip += 4

        else:
            raise RuntimeError(f"Unknown opcode {opcode}")

    return output


def part1():
    print(execute(program, 1))


def part2():
    print(execute(program, 5))


part1()
part2()
