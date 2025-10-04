from collections import defaultdict
from operator import ifloordiv

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


def read_parameter(memory, mode, offset, relative_base):
    if mode == 0:
        return memory[memory[offset]]
    elif mode == 1:
        return memory[offset]
    elif mode == 2:
        return memory[relative_base + memory[offset]]
    else:
        raise Exception("Invalid mode!")


def execute(program, input_callback, output_callback):
    ip = 0
    output = None
    relative_base = 0
    memory = defaultdict(lambda: 0)
    for offset, instruction in enumerate(program):
        memory[offset] = instruction

    while 0 <= ip < len(program):
        mode3, mode2, mode1, opcode = parse_opcode(memory[ip])
        if opcode == 99:
            break
        elif opcode == 1:
            A = read_parameter(memory, mode1, ip + 1, relative_base)
            B = read_parameter(memory, mode2, ip + 2, relative_base)
            C = memory[ip + 3] if mode3 == 0 else relative_base + memory[ip + 3]
            memory[C] = A + B
            ip += 4
        elif opcode == 2:
            A = read_parameter(memory, mode1, ip + 1, relative_base)
            B = read_parameter(memory, mode2, ip + 2, relative_base)
            C = memory[ip + 3] if mode3 == 0 else relative_base + memory[ip + 3]
            memory[C] = A * B
            ip += 4

        # Opcode 3 takes a single integer as input and saves it to the position given by its only parameter. For example, the instruction 3,50 would take an input value and store it at address 50.
        elif opcode == 3:
            A = memory[ip + 1] if mode1 == 0 else relative_base + memory[ip + 1]
            memory[A] = input_callback()
            ip += 2

        # Opcode 4 outputs the value of its only parameter. For example, the instruction 4,50 would output the value at address 50.
        elif opcode == 4:
            A = read_parameter(memory, mode1, ip + 1, relative_base)
            output = A
            output_callback(output)
            ip += 2

        # Opcode 5 is jump-if-true: if the first parameter is non-zero, it sets the instruction pointer to the value from the second parameter. Otherwise, it does nothing.
        elif opcode == 5:
            A = read_parameter(memory, mode1, ip + 1, relative_base)
            B = read_parameter(memory, mode2, ip + 2, relative_base)
            if A != 0:
                ip = B
            else:
                ip += 3

        # Opcode 6 is jump-if-false: if the first parameter is zero, it sets the instruction pointer to the value from the second parameter. Otherwise, it does nothing.
        elif opcode == 6:
            A = read_parameter(memory, mode1, ip + 1, relative_base)
            B = read_parameter(memory, mode2, ip + 2, relative_base)
            if A == 0:
                ip = B
            else:
                ip += 3

        # Opcode 7 is less than: if the first parameter is less than the second parameter, it stores 1 in the position given by the third parameter. Otherwise, it stores 0.
        elif opcode == 7:
            A = read_parameter(memory, mode1, ip + 1, relative_base)
            B = read_parameter(memory, mode2, ip + 2, relative_base)
            C = memory[ip + 3] if mode3 == 0 else relative_base + memory[ip + 3]
            if A < B:
                memory[C] = 1
            else:
                memory[C] = 0
            ip += 4

        # Opcode 8 is equals: if the first parameter is equal to the second parameter, it stores 1 in the position given by the third parameter. Otherwise, it stores 0.
        elif opcode == 8:
            A = read_parameter(memory, mode1, ip + 1, relative_base)
            B = read_parameter(memory, mode2, ip + 2, relative_base)
            C = memory[ip + 3] if mode3 == 0 else relative_base + memory[ip + 3]
            if A == B:
                memory[C] = 1
            else:
                memory[C] = 0
            ip += 4

        # Opcode 9 adjusts the relative base by the value of its only parameter. The relative base increases (or decreases, if the value is negative) by the value of the parameter.
        elif opcode == 9:
            relative_base += read_parameter(memory, mode1, ip + 1, relative_base)
            ip += 2
        else:
            raise RuntimeError(f"Unknown opcode {opcode}")

    return output


def part1():
    assert execute(program, lambda: 1, lambda v: v) == 7839346


def part2():
    assert execute(program, lambda: 5, lambda v: v) == 447803


part1()
part2()
