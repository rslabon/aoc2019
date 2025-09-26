import queue
import threading
from itertools import permutations

from day5 import execute

with open("./resources/day7.txt") as f:
    program = [int(c) for c in f.read().strip().split(",")]


def amplifier(program, input_queue, output_queue):
    execute(program[:], lambda: input_queue.get(), lambda v: output_queue.put(v))
    input_queue.task_done()


def compute_thruster_signal(program, phase, loop=False):
    qa = queue.Queue()
    qa.put(phase[0])
    qa.put(0)
    qb = queue.Queue()
    qb.put(phase[1])
    qc = queue.Queue()
    qc.put(phase[2])
    qd = queue.Queue()
    qd.put(phase[3])
    qe = queue.Queue()
    qe.put(phase[4])

    final = queue.Queue()
    if loop:
        final = qa

    A = threading.Thread(target=amplifier, args=(program, qa, qb), daemon=True)
    B = threading.Thread(target=amplifier, args=(program, qb, qc), daemon=True)
    C = threading.Thread(target=amplifier, args=(program, qc, qd), daemon=True)
    D = threading.Thread(target=amplifier, args=(program, qd, qe), daemon=True)
    E = threading.Thread(target=amplifier, args=(program, qe, final), daemon=True)

    for t in [A, B, C, D, E]:
        t.start()
    for t in [A, B, C, D, E]:
        t.join()

    value = final.get()
    final.task_done()

    return value


def part1():
    max_thruster_signal = float("-inf")
    for phase in permutations([0, 1, 2, 3, 4], 5):
        thruster_signal = compute_thruster_signal(program, phase)
        max_thruster_signal = max(max_thruster_signal, thruster_signal)

    print(max_thruster_signal)


def part2():
    max_thruster_signal = float("-inf")
    for phase in permutations([5, 6, 7, 8, 9], 5):
        thruster_signal = compute_thruster_signal(program, phase, True)
        max_thruster_signal = max(max_thruster_signal, thruster_signal)

    print(max_thruster_signal)


part1()
part2()
